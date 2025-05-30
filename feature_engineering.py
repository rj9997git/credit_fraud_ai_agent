import pandas as pd

def add_features(df):
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['merchant', 'timestamp'])
    df['time_since_last'] = df.groupby('merchant')['timestamp'].diff().dt.total_seconds() / 3600
    df['rolling_avg_amount'] = df.groupby('merchant')['amount'].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df['amount_ratio'] = df['amount'] / df['rolling_avg_amount']
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['is_weekend'] = df['timestamp'].dt.dayofweek >= 5
    return df