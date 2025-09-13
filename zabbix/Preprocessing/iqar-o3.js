// value = média móvel 8h do O3 (µg/m³)
var C = parseFloat(value);
if (!isFinite(C)) { return; } // sem dado

// Tabela de faixas (Índice x Concentração) – O3
var bands = [
  { Imin: 0,   Imax: 40,  Cmin: 0,    Cmax: 100   },
  { Imin: 41,  Imax: 80,  Cmin: 100.0000001, Cmax: 130  },
  { Imin: 81,  Imax: 120, Cmin: 130.0000001, Cmax: 160 },
  { Imin: 121, Imax: 200, Cmin: 160.0000001, Cmax: 200 },
  { Imin: 201, Imax: 400, Cmin: 200.0000001, Cmax: 800 }
];

// Encontra a faixa da concentração C
var b = null;
for (var i = 0; i < bands.length; i++) {
  var x = bands[i];
  if ((C >= x.Cmin) && (C <= x.Cmax)) { b = x; break; }
}

// Tratamentos de borda
if (!b) {
  if (C < 0) { return 0; } // satura inferior
  // acima da última faixa: satura em Cmax para limitar o índice
  b = bands[bands.length - 1];
  C = Math.min(C, b.Cmax);
}

// IQAr = Iini + (Ifin−Iini)/(Cfin−Cini) * (C−Cini)
var IQAr = b.Imin + ((b.Imax - b.Imin) / (b.Cmax - b.Cmin)) * (C - b.Cmin);

// Arredonda para inteiro (como nos exemplos); troque para toFixed(1) se quiser 1 casa.
return Math.round(IQAr);
