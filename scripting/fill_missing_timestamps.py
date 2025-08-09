import pandas as pd
from datetime import datetime

def fill_missing_timestamps(df, freq="1H", sensor_name=None, unit=None):
    """
    Preenche lacunas de timestamps no DataFrame com valores null,
    abrangendo sempre o intervalo do início ao fim do ano de referência.

    Parâmetros:
        df: DataFrame com colunas ['timestamp', 'valor']
        freq: frequência esperada das amostras (ex.: '1H')
        sensor_name: nome do sensor (str)
        unit: unidade de medição (str)

    Retorno:
        DataFrame com todos os timestamps do ano, preenchendo com null onde não houver valor.
    """
    # Garante formato datetime para timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    # Determina ano de referência a partir do primeiro registro disponível
    ano_ref = df.index.min().year

    # Define início e fim do ano
    start = datetime(ano_ref, 1, 1, 0, 0, 0)
    end = datetime(ano_ref, 12, 31, 23, 0, 0)

    # Cria série contínua para o ano inteiro
    full_index = pd.date_range(start=start, end=end, freq=freq)

    # Reindexa preenchendo lacunas com NaN
    df_full = df.reindex(full_index)

    # Adiciona colunas de metadados
    df_full["sensor"] = sensor_name
    df_full["unit"] = unit

    # Ajusta índice e nomes das colunas
    df_full = df_full.reset_index().rename(columns={"index": "timestamp"})

    # Formata timestamp para ISO8601
    df_full["timestamp"] = df_full["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Substitui NaN por None (null no JSON)
    df_full = df_full.where(pd.notnull(df_full), None)

    return df_full
