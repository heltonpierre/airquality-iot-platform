#!/usr/bin/env python3
# mqtt_to_zabbix.py
# Bridge MQTT → Zabbix (auto-onboarding + raw JSON to trapper + inventory from meta)
# Author: Helton-focused helper
#
# Requirements:
#   pip install paho-mqtt requests python-dotenv
#
# Usage:
#   python mqtt_to_zabbix.py
#
# Notes:
# - Subscribes to: airq/devices/+/telemetry and airq/devices/+/meta
# - On first sighting of a device (by deviceId), creates a Host in Zabbix,
#   attaches the provided template, and sets hostgroup. Then sends raw JSON
#   telemetry to a Text trapper item key (default: sensor.raw.json).
# - "meta" messages (retained) are used to fill Host inventory: lat/lon, model, fw.
#
# Security:
# - Prefer running this on the MQTT Gateway host, with TLS to broker and HTTPS to Zabbix (verify SSL).

import os
import re
import json
import time
import queue
import signal
import logging
import threading
import subprocess
from typing import Dict, Any, Optional

import requests
from paho.mqtt import client as mqtt

# ---------------------------
# Configuration (env vars)
# ---------------------------
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASS = os.getenv("MQTT_PASS", "")
MQTT_TLS = os.getenv("MQTT_TLS", "false").lower() == "true"
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "mqtt-to-zabbix")
MQTT_TELEMETRY_TOPIC = os.getenv("MQTT_TELEMETRY_TOPIC", "airq/devices/+/telemetry")
MQTT_META_TOPIC = os.getenv("MQTT_META_TOPIC", "airq/devices/+/meta")

ZBX_SERVER = os.getenv("ZBX_SERVER", "127.0.0.1")  # zabbix_server or proxy address
ZBX_API_URL = os.getenv("ZBX_API_URL", "http://127.0.0.1/api_jsonrpc.php")
ZBX_USER = os.getenv("ZBX_USER", "Admin")
ZBX_PASS = os.getenv("ZBX_PASS", "zabbix")
ZBX_TEMPLATE_NAME = os.getenv("ZBX_TEMPLATE_NAME", "Template IoT AirQ (JSON Raw)")
ZBX_HOSTGROUP_NAME = os.getenv("ZBX_HOSTGROUP_NAME", "IoT / AirQ")
ZBX_RAW_ITEM_KEY = os.getenv("ZBX_RAW_ITEM_KEY", "sensor.raw.json")

# For HTTPS verification (if using TLS on API). Set to path of CA bundle or "false" to skip.
ZBX_VERIFY_TLS = os.getenv("ZBX_VERIFY_TLS", "true").lower()
if ZBX_VERIFY_TLS in ("false", "0", "no"):
    ZBX_VERIFY_TLS = False
elif ZBX_VERIFY_TLS in ("true", "1", "yes"):
    ZBX_VERIFY_TLS = True

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO),
                    format="%(asctime)s %(levelname)s %(message)s")

# Regex to extract deviceId from topic: airq/devices/{deviceId}/telemetry|meta
TOPIC_RE = re.compile(r"^airq/devices/(?P<deviceId>[^/]+)/(?P<stream>telemetry|meta)$")

# In-memory caches
known_hosts = set()          # deviceId strings confirmed existing in Zabbix
meta_cache: Dict[str, Dict] = {}  # last seen meta per device for inventory updates

# Simple work queue to decouple MQTT thread from Zabbix operations
work_q: "queue.Queue[Dict[str, Any]]" = queue.Queue(maxsize=10000)

# ---------------------------
# Zabbix API helpers
# ---------------------------
class ZabbixAPI:
    def __init__(self, url: str, user: str, password: str, verify=True):
        self.url = url
        self.user = user
        self.password = password
        self.verify = verify
        self.token: Optional[str] = None
        self._id = 0

    def _rpc(self, method: str, params: Dict[str, Any]) -> Any:
        self._id += 1
        payload = {"jsonrpc": "2.0", "method": method, "params": params, "auth": self.token, "id": self._id}
        r = requests.post(self.url, json=payload, verify=self.verify, timeout=15)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise RuntimeError(f"Zabbix API error {data['error']}")
        return data["result"]

    def login(self):
        self._id += 1
        payload = {"jsonrpc": "2.0", "method": "user.login",
                   "params": {"user": self.user, "password": self.password},
                   "id": self._id, "auth": None}
        r = requests.post(self.url, json=payload, verify=self.verify, timeout=15)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise RuntimeError(f"Zabbix API login error {data['error']}")
        self.token = data["result"]
        logging.info("Zabbix API: authenticated")

    def get_or_create_hostgroup(self, name: str) -> str:
        res = self._rpc("hostgroup.get", {"filter": {"name": [name]}})
        if res:
            return res[0]["groupid"]
        res = self._rpc("hostgroup.create", {"name": name})
        return res["groupids"][0]

    def get_template_id(self, name: str) -> Optional[str]:
        res = self._rpc("template.get", {"filter": {"host": [name]}})
        if res:
            return res[0]["templateid"]
        return None

    def get_host(self, host: str) -> Optional[Dict[str, Any]]:
        res = self._rpc("host.get", {"filter": {"host": [host]}, "selectInventory": "extend"})
        return res[0] if res else None

    def create_host(self, host: str, groupid: str, templateid: Optional[str]) -> str:
        params = {
            "host": host,
            "interfaces": [{
                "type": 1, "main": 1, "useip": 1, "ip": "127.0.0.1", "dns": "", "port": "10050"
            }],
            "groups": [{"groupid": groupid}]
        }
        if templateid:
            params["templates"] = [{"templateid": templateid}]
        res = self._rpc("host.create", params)
        return res["hostids"][0]

    def update_inventory(self, hostid: str, inv: Dict[str, str]):
        self._rpc("host.update", {"hostid": hostid, "inventory_mode": 0, "inventory": inv})

# ---------------------------
# Zabbix sender helper
# ---------------------------
def zabbix_sender_send(host: str, key: str, value: str) -> bool:
    try:
        proc = subprocess.run(
            ["zabbix_sender", "-z", ZBX_SERVER, "-s", host, "-k", key, "-o", value],
            capture_output=True, text=True, timeout=10
        )
        if proc.returncode != 0:
            logging.error("zabbix_sender failed for host=%s key=%s rc=%s stdout=%s stderr=%s",
                          host, key, proc.returncode, proc.stdout.strip(), proc.stderr.strip())
            return False
        logging.debug("zabbix_sender ok: host=%s key=%s", host, key)
        return True
    except Exception as e:
        logging.exception("zabbix_sender exception: %s", e)
        return False

# ---------------------------
# Worker thread for Zabbix ops
# ---------------------------
def worker_loop(zbx: ZabbixAPI, stop_evt: threading.Event):
    # Pre-fetch group and template
    try:
        groupid = zbx.get_or_create_hostgroup(ZBX_HOSTGROUP_NAME)
        templateid = zbx.get_template_id(ZBX_TEMPLATE_NAME)
        if templateid is None:
            logging.warning("Template '%s' not found. Hosts will be created without template.", ZBX_TEMPLATE_NAME)
    except Exception as e:
        logging.error("Failed to prepare Zabbix resources: %s", e)
        groupid = None
        templateid = None

    while not stop_evt.is_set():
        try:
            task = work_q.get(timeout=0.5)
        except queue.Empty:
            continue

        ttype = task.get("type")
        if ttype == "telemetry":
            device_id = task["deviceId"]
            payload = task["payload"]
            # Ensure host exists
            try:
                if device_id not in known_hosts:
                    host = zbx.get_host(device_id)
                    if not host:
                        if not groupid:
                            groupid = zbx.get_or_create_hostgroup(ZBX_HOSTGROUP_NAME)
                        hostid = zbx.create_host(device_id, groupid, templateid)
                        logging.info("Host created: %s (id=%s)", device_id, hostid)
                    known_hosts.add(device_id)
                # Send raw JSON to trapper key
                ok = zabbix_sender_send(device_id, ZBX_RAW_ITEM_KEY, payload)
                if not ok:
                    logging.warning("Failed to send telemetry for %s", device_id)
            except Exception as e:
                logging.exception("Error handling telemetry for %s: %s", device_id, e)

        elif ttype == "meta":
            device_id = task["deviceId"]
            data = task["data"]
            meta_cache[device_id] = data
            # Update inventory when host exists
            try:
                host = zbx.get_host(device_id)
                if not host:
                    # Create host now to store inventory
                    if not groupid:
                        groupid = zbx.get_or_create_hostgroup(ZBX_HOSTGROUP_NAME)
                    hostid = zbx.create_host(device_id, groupid, templateid)
                    logging.info("Host created (from meta): %s (id=%s)", device_id, hostid)
                else:
                    hostid = host["hostid"]

                inv = {}
                # Try common fields from meta JSON:
                # { "deviceId": "...", "model": "...", "fw": "...", "loc": {"lat": ..., "lon": ...} }
                if "model" in data:
                    inv["model"] = str(data["model"])
                if "fw" in data:
                    inv["software"] = str(data["fw"])
                loc = data.get("loc", {})
                if isinstance(loc, dict):
                    if "lat" in loc:
                        inv["location_lat"] = str(loc["lat"])
                    if "lon" in loc:
                        inv["location_lon"] = str(loc["lon"])
                # Optional extras:
                if "station" in data:
                    inv["site_address_a"] = str(data["station"])
                if inv:
                    zbx.update_inventory(hostid, inv)
                    logging.info("Inventory updated for %s: %s", device_id, inv)
                known_hosts.add(device_id)
            except Exception as e:
                logging.exception("Error handling meta for %s: %s", device_id, e)

        work_q.task_done()

# ---------------------------
# MQTT callbacks
# ---------------------------
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logging.info("Connected to MQTT broker")
        client.subscribe(MQTT_TELEMETRY_TOPIC, qos=1)
        client.subscribe(MQTT_META_TOPIC, qos=1)
    else:
        logging.error("Failed MQTT connect: rc=%s", reason_code)

def on_message(client, userdata, msg):
    topic = msg.topic
    m = TOPIC_RE.match(topic)
    if not m:
        logging.debug("Ignored topic: %s", topic)
        return
    device_id = m.group("deviceId")
    stream = m.group("stream")

    try:
        payload_text = msg.payload.decode("utf-8")
    except UnicodeDecodeError:
        logging.warning("Non-UTF8 payload on %s", topic)
        return

    if stream == "telemetry":
        # Minimal validation: must be JSON and deviceId must match if present
        try:
            data = json.loads(payload_text)
            if "deviceId" in data and data["deviceId"] != device_id:
                logging.warning("deviceId mismatch topic=%s payload=%s", device_id, data.get("deviceId"))
        except Exception as e:
            logging.warning("Invalid JSON on telemetry: %s", e)
            return
        work_q.put({"type": "telemetry", "deviceId": device_id, "payload": payload_text})
    elif stream == "meta":
        try:
            data = json.loads(payload_text)
        except Exception as e:
            logging.warning("Invalid JSON on meta: %s", e)
            return
        work_q.put({"type": "meta", "deviceId": device_id, "data": data})

# ---------------------------
# Main
# ---------------------------
def main():
    # Zabbix API login
    zbx = ZabbixAPI(ZBX_API_URL, ZBX_USER, ZBX_PASS, verify=ZBX_VERIFY_TLS)
    zbx.login()

    stop_evt = threading.Event()
    t = threading.Thread(target=worker_loop, args=(zbx, stop_evt), daemon=True)
    t.start()

    # MQTT client
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY, protocol=mqtt.MQTTv5)
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    if MQTT_TLS:
        client.tls_set()  # use system CA bundle; customize if needed
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)

    def handle_sig(sig, frame):
        logging.info("Shutting down...")
        stop_evt.set()
        client.disconnect()

    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)

    try:
        client.loop_forever()
    finally:
        stop_evt.set()
        t.join(timeout=5)

if __name__ == "__main__":
    main()
