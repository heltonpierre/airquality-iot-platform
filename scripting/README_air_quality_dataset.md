
# 🌍 Air Quality Dataset Processing Pipeline for Node-RED IoT Simulation

## 📘 Introdução

Este repositório apresenta o pipeline de preparação e estruturação de dados ambientais provenientes do sistema de monitoramento da qualidade do ar mantido pela CETESB (Companhia Ambiental do Estado de São Paulo). Esses dados serão utilizados para simular dispositivos de IoT em experimentos conduzidos no ambiente **Node-RED**, como parte do projeto de pesquisa de mestrado.

Para viabilizar a simulação fidedigna e sem inconsistências temporais, foi necessário processar os **datalakes originais** da CETESB e convertê-los em **datasets estruturados no formato JSON**, com amostragens contínuas e tratamento de valores ausentes.

---

## 🎯 Objetivo

Garantir que os arquivos JSON utilizados na simulação contenham:

- Dados de todos os sensores esperados para cada dispositivo;
- Amostragens uniformes a cada hora (frequência de 1h);
- Inclusão explícita de valores ausentes (`null`) para sensores que não registraram medições em determinados timestamps.

---

## 🗂️ Estrutura dos dispositivos simulados

Cada **estação simulada (device)** contempla nove sensores:

- **Poluentes atmosféricos**:
  - MP2.5
  - MP10
  - CO
  - NO2
  - SO2
  - O3

- **Variáveis meteorológicas**:
  - Temperatura
  - Umidade relativa do ar
  - Pressão atmosférica

Devido à limitação de estações reais que contemplem os nove sensores simultaneamente, cada estação simulada foi composta a partir da junção de dados de duas ou mais estações físicas, considerando a proximidade geográfica.

### 📍 Mapeamento das estações simuladas

| Estação Simulada | CETESB (Poluentes)               | CETESB (Meteorologia)         |
|------------------|----------------------------------|-------------------------------|
| Station 01       | Osasco (MP2.5, MP10, CO, NO2, SO2) | Carapicuíba (O3, T, URA, P)   |
| Station 02       | *(a ser definido)*                | *(a ser definido)*            |
| Station 03       | *(a ser definido)*                | *(a ser definido)*            |

---

## ⚠️ Problemas identificados nos datalakes da CETESB

Durante a análise dos dados brutos exportados da base da CETESB (ano de 2024), foram identificadas inconsistências críticas:

- **Descontinuidade temporal**: os sensores apresentam falhas de coleta que resultam em lacunas temporais (apagões), com perdas de até 10% em alguns poluentes.
- **Timestamps não uniformes entre sensores**: cada sensor registra medições em seu próprio conjunto de horários, dificultando a agregação síncrona dos dados.

---

## 🔧 Scripts Utilizados

### 1. `fill_missing_timestamps.py`

Este script é responsável por preencher **lacunas de tempo** nos dados de cada sensor, garantindo que:

- Todos os **timestamps estejam presentes**, mesmo que sem valor de medição;
- Valores ausentes sejam representados explicitamente com `"valor": null`;
- Os metadados do sensor (nome e unidade) sejam preservados.

**Formato de entrada esperado**: DataFrame com colunas `timestamp` e `valor`.

**Saída**: DataFrame com todos os timestamps no intervalo, preenchendo valores ausentes com `null`.

---

### 2. `transform_datalake_csv_to_json_dataset.py`

Este script realiza a conversão dos arquivos `.csv` da CETESB para `.json` estruturado. Funções principais:

- Detecta automaticamente o nome do sensor e sua unidade de medição a partir do cabeçalho do CSV;
- Realiza parsing das colunas `Data`, `Hora` e `valor`;
- Gera o campo `timestamp` padronizado no formato ISO8601 (`YYYY-MM-DDTHH:MM:SS`);
- Invoca o script `fill_missing_timestamps.py` para preencher os timestamps ausentes;
- Salva a saída no formato JSON, pronta para uso no Node-RED.

**Formato de saída final**:
```json
[
  {
    "sensor": "no2",
    "valor": 42,
    "unidade": "µg/m3",
    "timestamp": "2024-01-06T00:00:00"
  },
  {
    "sensor": "no2",
    "valor": null,
    "unidade": "µg/m3",
    "timestamp": "2024-01-06T01:00:00"
  }
]
```

---

## 🛠️ Como Executar

1. **Coloque os arquivos .csv da CETESB** no diretório:

```
../cetesb_data/datalake/
```

2. **Execute o script de transformação**:

```bash
python3 transform_datalake_csv_to_json_dataset.py
```

3. Os arquivos `.json` serão salvos em:

```
../cetesb_data/dataset/station_01/
```

---

## 📌 Observações Importantes

- A frequência das amostragens é padronizada para **1 hora**.
- Os arquivos `.json` resultantes podem ser consumidos diretamente no Node-RED via `file in`.
- Essa estrutura garante consistência e robustez para a simulação de sensores em tempo real.

---

## 📚 Referências

- [CETESB - Qualidade do Ar](https://cetesb.sp.gov.br/ar/)
- [Node-RED - Official Site](https://nodered.org/)
- [Projeto de Mestrado - Plataforma de Monitoramento da Qualidade do Ar baseada em IoT (2024)]
