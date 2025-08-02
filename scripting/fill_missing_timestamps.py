
import pandas as pd

def fill_missing_timestamps(df, freq="1H", sensor_name=None, unit=None):
    """
    Fill missing timestamps in the DataFrame with null values.

    Parameters:
        df: DataFrame with columns ['timestamp', 'valor']
        freq: expected sampling frequency (e.g., '1H')
        sensor_name: name of the sensor (str)
        unit: measurement unit (str)

    Returns:
        DataFrame with complete timestamps and null for missing data
    """
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    # Generate full timeline
    start = df.index.min()
    end = df.index.max()
    full_index = pd.date_range(start=start, end=end, freq=freq)

    # Reindex and insert nulls
    df_full = df.reindex(full_index)

    # Fill in sensor and unit fields
    df_full["sensor"] = sensor_name
    df_full["unit"] = unit
    df_full = df_full.reset_index().rename(columns={"index": "timestamp"})

    # Format timestamp
    df_full["timestamp"] = df_full["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Corrige os NaN para None
    df_full = df_full.where(pd.notnull(df_full), None)
    
    return df_full
