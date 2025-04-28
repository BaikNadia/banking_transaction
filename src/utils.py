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


import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def read_excel_file(file_name: str) -> pd.DataFrame:
    """
    Чтение Excel-файла с транзакциями.

    :param file_name: Название файла.
    :return: DataFrame с данными.
    """
    try:
        df = pd.read_excel(file_name)

        # Проверка наличия необходимых столбцов
        required_columns = ["Дата операции", "Статус", "Сумма операции", "Категория", "Описание"]
        if not all(col in df.columns for col in required_columns):
            raise KeyError(f"Отсутствуют необходимые столбцы: {required_columns}")

        # Преобразование даты в формат datetime
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format='%d.%m.%Y %H:%M:%S', errors='coerce')

        logging.info(f"Файл {file_name} успешно прочитан.")
        return df

    except Exception as e:
        logging.error(f"Ошибка при чтении файла {file_name}: {e}")
        return pd.DataFrame()
