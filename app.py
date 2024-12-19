import streamlit as st
import pandas as pd
import os
from download_data import download_stock_data
from strategy_template import sma_cross_strategy_5_10, sma_cross_strategy_20_60, buy_and_hold_strategy, rsi_strategy
from backtest import backtest_strategy

st.title('股票回測系統')

# 股票數據下載
st.header('股票數據下載')
ticker = st.text_input('輸入股票代碼', 'QQQ')
start_date = st.date_input('開始日期', pd.to_datetime('2020-01-01'))
end_date = st.date_input('結束日期', pd.to_datetime('2024-12-17'))

# 自動下載數據並提供下載鏈接
file_path = download_stock_data(ticker, start_date, end_date)
st.success(f'數據已下載並儲存至 {file_path}')

# 提供下載鏈接
with open(file_path, 'rb') as file:
    st.download_button(
        label="下載 CSV",
        data=file,
        file_name=f"{ticker}.csv",
        mime='text/csv'
    )

# 股票策略回測
st.header('股票策略回測')
uploaded_file = st.file_uploader('選擇股票數據檔案 (CSV)', type='csv')
initial_capital = st.number_input('初始投資金額', value=10000)

# 策略選擇
st.header('選擇策略')
strategy_options = {
    'SMA Cross 5 10': sma_cross_strategy_5_10,
    'SMA Cross 20 60': sma_cross_strategy_20_60,
    'Buy and Hold': buy_and_hold_strategy,
    'RSI': rsi_strategy
}
strategy_name = st.selectbox('選擇策略', list(strategy_options.keys()))
selected_strategy = strategy_options[strategy_name]

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, index_col='Date', parse_dates=True)
    signals = selected_strategy(data)
    portfolio = backtest_strategy(data, signals, initial_capital)
    st.write('回測結果')
    st.line_chart(portfolio['total'])
    st.write('每月獲利')
    monthly_returns = portfolio['returns'].resample('M').sum() * 100  # 轉換為百分比
    st.bar_chart(monthly_returns)
    st.write('總獲利數據')
    st.write(portfolio.tail(1))

    # 顯示所有買進賣出日期的表格
    st.header('買進賣出日期')
    trade_dates = signals[signals['positions']
                          != 0].sort_index(ascending=False)

    st.write(trade_dates[['price', 'signal', 'positions']])

    # 儲存回測結果
    if st.button('儲存回測結果'):
        result_path = './results/'
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        result_file = os.path.join(result_path, f'{ticker}_backtest.html')
        with open(result_file, 'w') as f:
            f.write(portfolio.to_html())
        st.success(f'回測結果已儲存至 {result_file}')
