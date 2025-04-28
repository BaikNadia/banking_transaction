import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


def filter_transactions_by_date(target_date: datetime) -> list:
    """
    Фильтрует транзакции по заданной дате.

    :param target_date: Дата для фильтрации.
    :return: Список словарей с транзакциями.
    """
    # Загружаем данные из Excel (например, operations.xlsx)
    df = pd.read_excel("data/operations.xlsx")

    # Преобразуем столбец 'date' в формат datetime
    df['date'] = pd.to_datetime(df['date'])

    # Фильтруем транзакции по дате
    filtered_df = df[df['date'].dt.date == target_date.date()]

    # Преобразуем DataFrame в список словарей
    transactions = filtered_df.to_dict(orient="records")

    logging.info(f"Filtered {len(transactions)} transactions by date {target_date.date()}")
    return transactions


def filter_events_by_month(dataframe) -> list:
    """
    Фильтрует события по текущему месяцу.

    :param dataframe: DataFrame с транзакциями.
    :return: Список словарей с событиями.
    """
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Фильтруем транзакции по текущему месяцу
    filtered_df = dataframe[
        (dataframe['date'].dt.month == current_month) &
        (dataframe['date'].dt.year == current_year)
        ]

    # Преобразуем DataFrame в список словарей
    events = filtered_df.to_dict(orient="records")

    logging.info(f"Filtered {len(events)} events for month {current_month}/{current_year}")
    return events


import os
import pandas as pd
from datetime import datetime

def read_excel_file(file_name: str) -> pd.DataFrame:
    """
    Читает Excel-файл с транзакциями и возвращает DataFrame.

    :param file_name: Название файла (например, "operations.xlsx").
    :return: DataFrame с данными.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", file_name)

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return pd.DataFrame()  # Возвращаем пустой DataFrame

    try:
        # Чтение файла
        df = pd.read_excel(file_path)

        # Преобразование даты операции в формат datetime
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S', errors='coerce')

        print(f"Файл {file_path} успешно прочитан.")
        return df

    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame
