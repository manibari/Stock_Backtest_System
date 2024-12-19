import yfinance as yf
import os
import pandas as pd


def download_stock_data(ticker, start_date, end_date, save_path='./stock_data/'):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    data = yf.download(ticker, start=start_date, end=end_date)

    # Transform the columns
    data = data.reset_index()

    # Remove all column names
    data.columns = [None] * len(data.columns)

    # Provide the column names again
    data.columns = ['Date', 'Adj Close',
                    'Close', 'High', 'Low', 'Open', 'Volume']

    file_path = os.path.join(save_path, f"{ticker}.csv")
    data.to_csv(file_path)
    return file_path


# Example usage
if __name__ == "__main__":
    download_stock_data('QQQ', '2020-01-01', '2024-12-18')
