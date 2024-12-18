import pandas as pd
import plotly.graph_objects as go

def plot_interactive_graph(data):
    if data.empty or 'Close' not in data:
        print("Ошибка: Нет данных для построения графика или отсутствует столбец 'Close'.")
        return

    mean_close = data['Close'].mean()
    print(f"Среднее значение цены закрытия: {mean_close:.2f} USD")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index, y=[mean_close] * len(data), mode='lines', name='Mean Close', line=dict(dash='dash', color='red')))
    fig.update_layout(title='Интерактивный график цен акций', xaxis_title='Дата', yaxis_title='Цена (USD)', template='plotly')
    fig.show()