import pandas as pd
import json
import re
import os
import numpy as np
from fill_missing_timestamps import fill_missing_timestamps

# Diretórios de entrada e saída
csv_dir = "../cetesb_data/datalake/group_of_stations_01/"
json_dir = "../cetesb_data/dataset/device_01/"

# Garante que o diretório de saída exista
os.makedirs(json_dir, exist_ok=True)

# Lista todos os arquivos CSV no diretório
arquivos_csv = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]

for nome_arquivo in arquivos_csv:
    csv_path = os.path.join(csv_dir, nome_arquivo)
    nome_base = os.path.splitext(nome_arquivo)[0]
    json_path = os.path.join(json_dir, f"{nome_base}.json")

    try:
        with open(csv_path, "r", encoding="latin1") as f:
            linhas = [next(f) for _ in range(9)]

        linha_identificacao = linhas[7].strip()
        match = re.search(r"([A-Z0-9]+).*?-\s*([^\s]+)", linha_identificacao)
        if match:
            sensor_nome = match.group(1).lower()
            unidade = match.group(2)
        else:
            raise ValueError("❌ Não foi possível extrair o nome do sensor e unidade.")

        df = pd.read_csv(csv_path, sep=";", encoding="latin1", skiprows=8)
        df.columns = ["Data", "Hora", "valor"]
        df = df.dropna(subset=["Data", "Hora", "valor"])
        df = df.copy()  # Evita SettingWithCopyWarning

        df["Hora"] = df["Hora"].replace("24:00", "00:00")
        df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce")
        df.loc[df["Hora"] == "00:00", "Data"] += pd.Timedelta(days=1)

        df["timestamp"] = pd.to_datetime(df["Data"].dt.strftime("%Y-%m-%d") + " " + df["Hora"])
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

        # Preenche lacunas e obtém DataFrame completo
        df_completo = fill_missing_timestamps(
            df[["timestamp", "valor"]],
            freq="1h",
            sensor_name=sensor_nome,
            unit=unidade
        )

        # Renomeia e seleciona colunas finais
        df_json = df_completo[["sensor", "valor", "unit", "timestamp"]].rename(columns={"unit": "unidade"})

        # Conversão segura de NaN para None (null no JSON)
        registros = df_json.to_dict(orient="records")
        for r in registros:
            for k, v in r.items():
                if isinstance(v, float) and np.isnan(v):
                    r[k] = None

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)

        print(f"✅ JSON gerado com sucesso: {json_path}")

    except Exception as e:
        print(f"❌ Erro ao processar {csv_path}: {e}")
