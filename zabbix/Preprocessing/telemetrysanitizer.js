var obj; 
try { obj = JSON.parse(value); } catch (e) { return value; }

function toNum(v) {
  if (v === null || v === undefined || v === "") return null;
  v = String(v).replace(",", ".");
  var n = Number(v);
  return isNaN(n) ? null : n;
}

if (obj.co !== undefined) obj.co = toNum(obj.co);
if (obj.temperatura !== undefined) obj.temperatura = toNum(obj.temperatura);
if (obj.pressao !== undefined) obj.pressao = toNum(obj.pressao);

var keys = ["lat","lon","pm10","pm25","o3","no2","so2","umidade"];
for (var i = 0; i < keys.length; i++) {
  var k = keys[i];
  if (obj[k] !== undefined) obj[k] = toNum(obj[k]);
}

return JSON.stringify(obj);