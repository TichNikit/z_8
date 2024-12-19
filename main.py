import data_download as dd
import data_plotting as dplt
import matplotlib.pyplot as plt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    available_styles = plt.style.available
    print("Доступные стили графиков:")
    for style in available_styles:
        print("-", style)

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    print("Вы можете ввести период, за который вас интересует цена акции.\n"
          "Если вы хотите указа конкретные даты, то пропустите этот пункт.")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    if not period:
        period = '1mo'

    start_date = input("Введите дату начала в формате ГГГГ-ММ-ДД: ")
    end_date = input("Введите дату окончания в формате ГГГГ-ММ-ДД: ")

    style = input("Введите стиль графика (по умолчанию 'default'): ") or 'default'

    stock_data = dd.fetch_stock_data(ticker, start_date, end_date)

    stock_data = dd.add_moving_average(stock_data)

    dd.calculate_and_display_statistics(stock_data)

    threshold = float(input("Процент для сравнения (в %): "))
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    file_name = input('Имя файла (по умолчанию inf.csv): ') or 'inf.csv'
    dd.export_data_to_csv(stock_data, file_name=file_name)

    dplt.create_and_save_plot(stock_data, ticker, period)
    dplt.plot_interactive_graph(stock_data)


if __name__ == "__main__":
    main()
