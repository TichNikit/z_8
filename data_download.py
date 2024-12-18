import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, start_date=None, end_date=None):
    stock = yf.Ticker(ticker)

    try:
        if start_date and end_date:
            data = stock.history(start=start_date, end=end_date)
        else:
            data = stock.history(period='1mo')
        return data
    except Exception as e:
        print(f"Ошибка при загрузке данных для {ticker}: {e}")
        return pd.DataFrame()

def add_moving_average(data, window_size=5):
    if 'Close' in data:
        data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
        data['STD_Dev'] = data['Close'].rolling(window=window_size).std()
    return data

def calculate_and_display_statistics(data):
    if not data.empty:
        average_price = data['Close'].mean()
        std_deviation = data['Close'].std()
        print(f"Средняя цена закрытия акций за данный период: {average_price:.2f} USD")
        print(f"Стандартное отклонение цены закрытия: {std_deviation:.2f} USD")
    else:
        print("Нет данных для расчета статистики.")

def notify_if_strong_fluctuations(data, threshold):
    if 'Close' in data:
        initial_price = data['Close'].iloc[0]
        final_price = data['Close'].iloc[-1]

        if pd.notna(initial_price):
            percentage_change = ((final_price - initial_price) / initial_price) * 100
            if abs(percentage_change) > threshold:
                print(f"ЦЕНА СИЛЬНО ИЗМЕНИЛАСЬ! {percentage_change:.2f}% > {threshold}%")
            else:
                print(f"ЦЕНА В ПРЕДЕЛАХ ОЖИДАНИЯ: {percentage_change:.2f}% < {threshold}%")
    else:
        print("Данные о закрытии отсутствуют.")

def export_data_to_csv(data, file_name):
    try:
        data.to_csv(file_name, index=True)
        print(f"Данные экспортированы в файл: {file_name}")
    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")

def calculate_rsi(data, window=14):
    if 'Close' in data:
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss.replace({0: pd.NA})
        data['RSI'] = 100 - (100 / (1 + rs))
    return data

def calculate_macd(data):
    if 'Close' in data:
        short_ema = data['Close'].ewm(span=12, adjust=False).mean()
        long_ema = data['Close'].ewm(span=26, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=9, adjust=False).mean()
        data['MACD'] = macd
        data['MACD_Signal'] = signal
    return data