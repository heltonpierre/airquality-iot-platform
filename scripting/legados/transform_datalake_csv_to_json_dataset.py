
import pandas as pd
import json
import re
from fill_missing_timestamps import fill_missing_timestamps  # novo import

# Caminhos de entrada e saída
csv_path = "../cetesb_data/datalake/cetesb_osasco_no2_2024.csv"
json_path = "../cetesb_data/dataset/station_01/cetesb_osasco_no2_2024.json"

# Lê as primeiras 9 linhas para extrair metadados e cabeçalhos
with open(csv_path, "r", encoding="latin1") as f:
    linhas = [next(f) for _ in range(9)]

# Extrai nome do poluente e unidade da linha 8
linha_identificacao = linhas[7].strip()
match = re.search(r"([A-Z0-9]+).*?-\s*([^\s]+)", linha_identificacao)
if match:
    sensor_nome = match.group(1).lower()
    unidade = match.group(2)
else:
    raise ValueError("❌ Não foi possível extrair o nome do sensor e unidade da linha 8.")

# Carrega os dados a partir da linha 9
df = pd.read_csv(csv_path, sep=";", encoding="latin1", skiprows=8)
df.columns = ["Data", "Hora", "valor"]
df = df.dropna(subset=["Data", "Hora", "valor"])

# Corrige horários 24:00 para 00:00 do dia seguinte
df["Hora"] = df["Hora"].replace("24:00", "00:00")
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce")
df.loc[df["Hora"] == "00:00", "Data"] += pd.Timedelta(days=1)

# Gera timestamp ISO
df["timestamp"] = pd.to_datetime(df["Data"].dt.strftime("%Y-%m-%d") + " " + df["Hora"])
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

# Aplica preenchimento de lacunas
df_completo = fill_missing_timestamps(df[["timestamp", "valor"]], freq="1H", sensor_name=sensor_nome, unit=unidade)

# Reorganiza
df_json = df_completo[["sensor", "valor", "unit", "timestamp"]].rename(columns={"unit": "unidade"})

# Exporta para JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(df_json.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

print(f"✅ JSON gerado com sucesso: {json_path}")
