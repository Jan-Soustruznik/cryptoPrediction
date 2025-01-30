import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Compute RSI and MACD
def compute_indicators(df):
    df['change'] = df['close'].diff()
    df['gain'] = df['change'].mask(df['change'] < 0, 0)
    df['loss'] = -df['change'].mask(df['change'] > 0, 0)
    df['avg_gain'] = df['gain'].rolling(window=14).mean()
    df['avg_loss'] = df['loss'].rolling(window=14).mean()
    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    df['ema12'] = df['close'].ewm(span=12).mean()
    df['ema26'] = df['close'].ewm(span=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9).mean()
    return df

# Prepare data for training
def prepare_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['close', 'volume', 'rsi', 'macd']].dropna())

    sequence_length = 60
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i])
        y.append(scaled_data[i, 0])

    return np.array(X), np.array(y), scaler
