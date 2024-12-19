import numpy as np
import pandas as pd


def sma_cross_strategy_5_10(data, short_window=5, long_window=10):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['short_mavg'] = data['Close'].rolling(
        window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['Close'].rolling(
        window=long_window, min_periods=1, center=False).mean()
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    return signals


def sma_cross_strategy_20_60(data, short_window=20, long_window=60):
    # 創建一個與輸入數據索引相同的 DataFrame 來存儲信號
    signals = pd.DataFrame(index=data.index)

    # 將收盤價存儲在 'price' 列中
    signals['price'] = data['Close']

    # 計算短期移動平均線，默認窗口為 20 天
    signals['short_mavg'] = data['Close'].rolling(
        window=short_window, min_periods=1, center=False).mean()

    # 計算長期移動平均線，默認窗口為 60 天
    signals['long_mavg'] = data['Close'].rolling(
        window=long_window, min_periods=1, center=False).mean()

    # 初始化 'signal' 列，所有值設置為 0.0
    signals['signal'] = 0.0

    # 當短期移動平均線大於長期移動平均線時，設置 'signal' 為 1.0，否則為 0.0
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    # 計算 'positions' 列，表示信號的變化 (買進或賣出)
    signals['positions'] = signals['signal'].diff()

    # 返回包含信號和位置的 DataFrame
    return signals


def buy_and_hold_strategy(data):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['signal'] = 0.0

    # 在第二天買入股票訊號
    if len(signals) > 1:
        signals['signal'].iloc[1] = 1.0

    # 從第二天到倒數第二天的信號設置為 1.0
    signals['signal'][1:-1] = 1.0

    # 計算 'positions' 列，表示信號的變化
    signals['positions'] = signals['signal'].diff()
    return signals


def rsi_strategy(data, window=14, overbought=70, oversold=30):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']

    # 計算 RSI 指標
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    signals['rsi'] = 100 - (100 / (1 + rs))

    # 初始化 'signal' 列，所有值設置為 0.0
    signals['signal'] = 0.0

    # 當 RSI 低於 oversold 閾值時，設置 'signal' 為 1.0，表示買入
    signals['signal'][signals['rsi'] < oversold] = 1.0

    # 當 RSI 高於 overbought 閾值時，設置 'signal' 為 -1.0，表示賣出
    signals['signal'][signals['rsi'] > overbought] = -1.0

    # 計算 'positions' 列，表示信號的變化
    signals['positions'] = signals['signal'].diff()

    return signals


# Example usage
if __name__ == "__main__":
    data = pd.read_csv('./stock_data/QQQ.csv',
                       index_col='Date', parse_dates=True)
    signals = buy_and_hold_strategy(data)
    print(signals.head(15))
    print(signals.tail(15))
