
import pandas as pd
import json

# Caminho de entrada e saída
csv_path = "../datalake/CSV/cetesb_osasco_mp10_2024.csv"
json_path = "../datalake/JSON/cetesb_osasco_mp10_2024.json"

# Carrega o CSV (ajuste se necessário)
df = pd.read_csv(csv_path, sep=";", encoding="utf-8")

# Verifica e formata o timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Converte para string ISO8601
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

# Converte para lista de dicionários
records = df.to_dict(orient="records")

# Salva como JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"Arquivo JSON gerado com sucesso: {json_path}")
