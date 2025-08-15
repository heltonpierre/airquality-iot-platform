// ===== Metadados estáticos do dispositivo =====
const DEVICE_META = {
    deviceId: "device12", // ID único do dispositivo
    station: "Hospital Infantil Maria Alice", // Nome da estação
    lat: -5.763483396042317, // Latitude e Longitude do dispositivo
    lon: -35.282321778592525, // cuidado com espaços antes do número!
    model: "Node-RED", // Modelo do dispositivo
    fw_version: "v3.1.0" // Versão do firmware
};

// ===== Mapeamento nomes reais -> padronizados =====
const mapSensor = {
    "mp10": "pm10",
    "mp2": "pm25",
    "o3": "o3",
    "no2": "no2",
    "so2": "so2",
    "co": "co",
    "temp": "temperatura",
    "ur": "umidade",
    "press": "pressao"
};

const sensoresEsperados = Object.values(mapSensor);

// Buffer por timestamp no flow context
let buffer = flow.get("sensorBuffer") || {};

const dado = msg.payload;
const ts = dado.timestamp;                // ISO8601/epoch conforme sua entrada
const nomeSensor = mapSensor[dado.sensor];

if (!nomeSensor) return null; // ignora sensores desconhecidos

// Cria bucket do timestamp se necessário
if (!buffer[ts]) buffer[ts] = {};

// Armazena valor padronizado
buffer[ts][nomeSensor] = dado.valor;
flow.set("sensorBuffer", buffer);

// Verifica se todos os sensores chegaram
const sensoresPresentes = Object.keys(buffer[ts]);
const todosPresentes = sensoresEsperados.every(s => sensoresPresentes.includes(s));

if (todosPresentes) {
    // Payload final: metadados + geolocalização + timestamp + leituras
    const payloadFinal = {
        // --- metadados (topo) ---
        deviceId: DEVICE_META.deviceId,
        station: DEVICE_META.station,
        lat: Number(DEVICE_META.lat),
        lon: Number(DEVICE_META.lon),
        model: DEVICE_META.model,
        fw_version: DEVICE_META.fw_version,
        // --- tempo ---
        timestamp: ts
    };

    // Leituras (flatten para facilitar consumo / Grafana)
    sensoresEsperados.forEach(s => {
        payloadFinal[s] = buffer[ts][s] ?? null;
    });

    // Limpa o bucket do timestamp
    delete buffer[ts];
    flow.set("sensorBuffer", buffer);
    
    // Playload pronto para envio
    msg.payload = payloadFinal;
    msg.qos = 1;        // opcional
    msg.retain = false;    // telemetria normalmente não é retida
    return msg;
}

// Ainda aguardando outros sensores desse timestamp
return null;