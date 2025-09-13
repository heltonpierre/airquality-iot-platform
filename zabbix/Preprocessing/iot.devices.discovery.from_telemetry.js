// Gera {data:[{#DEVICEID}, {#STATION}, {#TOPIC_TEL}, {#LAT}, {#LON}]}
function toStr(v){ return (v===undefined||v===null) ? "" : String(v); }
var p;
try { p = JSON.parse(value); } catch(e) { return null; }
if (!p || !p.deviceId) return null;

var out = { data: [ {
  "{#DEVICEID}": toStr(p.deviceId),
  "{#STATION}": toStr(p.station),
  "{#TOPIC_TEL}": "airq/devices/"+toStr(p.deviceId)+"/telemetria",
  "{#LAT}": toStr(p.lat),
  "{#LON}": toStr(p.lon)
} ] };
return JSON.stringify(out);