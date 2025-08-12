// Zabbix JS (ES5) – remove o envelope do tópico e normaliza números
function toNum(v) {
  if (v === null || v === undefined || v === "") return null;
  v = String(v).replace(",", ".");
  var n = Number(v);
  return isNaN(n) ? v : n;
}

function normalizeNumbers(p) {
  // converta apenas os campos esperados
  var keys = ["co","temperatura","pressao","pm10","pm25","o3","no2","so2","umidade","lat","lon"];
  for (var i = 0; i < keys.length; i++) {
    var k = keys[i];
    if (p.hasOwnProperty(k)) p[k] = toNum(p[k]);
  }
  return p;
}

var raw = value;

// 1) Tente interpretar 'raw' como objeto envelope { "<topico>": "<json-string>" }
var outer;
try {
  outer = JSON.parse(raw);
} catch (e1) {
  // Talvez já seja o payload puro
  try {
    return JSON.stringify(normalizeNumbers(JSON.parse(raw)));
  } catch (e2) {
    return raw; // não é JSON, devolve como veio
  }
}

// 2) Obtenha o primeiro valor do envelope (payload)
var payloadStr = null;
if (outer && typeof outer === "object") {
  for (var prop in outer) {
    if (outer.hasOwnProperty(prop)) {
      payloadStr = outer[prop];
      break;
    }
  }
}

// 3) Se já veio objeto, normalize e devolva
if (payloadStr && typeof payloadStr === "object") {
  return JSON.stringify(normalizeNumbers(payloadStr));
}

// 4) Caso geral: é uma string JSON com aspas escapadas → parse de novo
try {
  var payload = JSON.parse(payloadStr);
  return JSON.stringify(normalizeNumbers(payload));
} catch (e3) {
  // Falhou o parse interno: devolve string sem envelope
  return payloadStr;
}