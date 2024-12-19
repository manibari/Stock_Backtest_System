import pandas as pd
import matplotlib.pyplot as plt
from strategy_template import sma_cross_strategy_5_10, sma_cross_strategy_20_60, buy_and_hold_strategy, rsi_strategy


def backtest_strategy(data, signals, initial_capital=10000.0):
    # 創建一個與信號索引相同的 DataFrame 來存儲持倉信息，並將所有值初始化為 0.0
    positions = pd.DataFrame(index=signals.index).fillna(0.0)

    # 根據信號計算持倉數量，初始持倉數量應該是 initial capital 除以初始股票金額
    initial_stock_price = data['Adj Close'].iloc[0]
    initial_stock_quantity = initial_capital // initial_stock_price
    positions['stock'] = initial_stock_quantity * signals['signal']

    # 計算每個時間點的投資組合價值，根據持倉數量和調整後的收盤價
    portfolio = positions.multiply(data['Adj Close'], axis=0)

    # 計算持倉變化
    pos_diff = positions.diff()

    # 計算持倉價值，將每個時間點的持倉數量乘以調整後的收盤價，並對所有持倉求和
    portfolio['holdings'] = (positions.multiply(
        data['Adj Close'], axis=0)).sum(axis=1)

    # 計算現金餘額，初始資金減去每次交易的成本，並累積求和
    portfolio['cash'] = initial_capital - \
        (pos_diff.multiply(data['Adj Close'], axis=0)).sum(axis=1).cumsum()

    # 計算投資組合總價值，包括現金和持倉價值
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']

    # 計算投資組合的每日回報率
    portfolio['returns'] = portfolio['total'].pct_change()

    # 返回包含投資組合信息的 DataFrame
    return portfolio


def plot_backtest_results(data, signals, portfolio):
    # 創建一個包含兩個子圖的圖形，並共享 x 軸
    fig, ax = plt.subplots(2, sharex=True, figsize=(12, 8))

    # 在第一個子圖中繪製調整後的收盤價
    data['Adj Close'].plot(ax=ax[0], color='r', lw=2.)
    ax[0].set_ylabel('Price in $')

    # 在第一個子圖中繪製短期和長期移動平均線
    # signals[['short_mavg', 'long_mavg']].plot(ax=ax[0], lw=2.)

    # 在第一個子圖中標記買入信號的位置
    # ax[0].plot(signals.loc[signals.positions == 1.0].index,
    #           signals.short_mavg[signals.positions == 1.0],
    #           '^', markersize=10, color='m')

    # 在第一個子圖中標記賣出信號的位置
    # ax[0].plot(signals.loc[signals.positions == -1.0].index,
    #           signals.short_mavg[signals.positions == -1.0],
    #           'v', markersize=10, color='k')

    # 在第二個子圖中繪製投資組合總價值
    portfolio['total'].plot(ax=ax[1], lw=2.)
    ax[1].set_ylabel('Portfolio value in $')

    # 顯示圖形
    plt.show()


# Example usage
if __name__ == "__main__":
    data = pd.read_csv('./stock_data/QQQ.csv',
                       index_col='Date', parse_dates=True)
    signals = buy_and_hold_strategy(data)
    portfolio = backtest_strategy(data, signals)
    plot_backtest_results(data, signals, portfolio)
