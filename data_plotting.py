import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    plt.style.use(style)
    plt.figure(figsize=(10, 6))

    if 'Date' in data:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        dates = data['Date']
    elif pd.api.types.is_datetime64_any_dtype(data.index):
        dates = data.index
    else:
        print("Информация о дате отсутствует или не имеет распознаваемого формата.")
        return

    plt.plot(dates, data['Close'], label='Close Price')

    if 'Moving_Average' in data:
        plt.plot(dates, data['Moving_Average'], label='Moving Average')

        if 'STD_Dev' in data:
            plt.fill_between(dates,
                             data['Moving_Average'] + data['STD_Dev'],
                             data['Moving_Average'] - data['STD_Dev'],
                             color='gray', alpha=0.2, label='Standard Deviation')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    plt.close()
    print(f"График сохранен как {filename}")

    if 'RSI' in data:
        plot_rsi(data, ticker)
    if 'MACD' in data:
        plot_macd(data, ticker)


def plot_rsi(data, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['RSI'], label='RSI', color='orange')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red', label='Overbought (70)')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green', label='Oversold (30)')
    plt.title(f"RSI для {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()
    plt.savefig(f"{ticker}_RSI_chart.png")
    plt.close()
    print(f"График RSI сохранен как {ticker}_RSI_chart.png")


def plot_macd(data, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['MACD'], label='MACD')
    plt.plot(data['Date'], data['MACD_Signal'], label='MACD Signal', linestyle='--')
    plt.title(f"MACD для {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()
    plt.savefig(f"{ticker}_MACD_chart.png")
    plt.close()
    print(f"График MACD сохранен как {ticker}_MACD_chart.png")


def plot_interactive_graph(data):
    if data.empty or 'Close' not in data:
        print("Ошибка: Нет данных для построения графика или отсутствует столбец 'Close'.")
        return

    mean_close = data['Close'].mean()
    print(f"Среднее значение цены закрытия: {mean_close:.2f} USD")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index, y=[mean_close] * len(data), mode='lines', name='Mean Close',
                             line=dict(dash='dash', color='red')))
    fig.update_layout(title='Интерактивный график цен акций', xaxis_title='Дата', yaxis_title='Цена (USD)',
                      template='plotly')
    fig.show()
