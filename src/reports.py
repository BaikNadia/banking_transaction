import json
from src.utils import read_excel_file
from datetime import datetime, timedelta
import logging

def spending_by_category(category: str, start_date_str: str, file_path: str) -> str:
    """
    Возвращает тренды трат по категории за трехмесячный период.

    :param category: Категория транзакций.
    :param start_date_str: Начальная дата периода (YYYY-MM-DD).
    :param file_path: Путь к Excel-файлу.
    :return: JSON-ответ с трендами.
    """
    try:
        # Преобразование строки даты в объект datetime
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = start_date + timedelta(days=90)

        # Чтение данных из файла
        df = read_excel_file(file_path)

        # Фильтрация по категории и дате
        filtered_df = df[(df['Категория'] == category) & (df['Дата операции'].dt.date >= start_date) & (df['Дата операции'].dt.date <= end_date)]

        # Группировка по дням
        grouped = filtered_df.groupby(filtered_df['Дата операции'].dt.date).agg({'Сумма операции': 'sum'}).reset_index()

        # Подготовка JSON-ответа
        response_data = {
            "category": category,
            "start_date": start_date_str,
            "end_date": end_date.strftime("%Y-%m-%d"),
            "spending_trend": grouped.to_dict(orient="records")
        }

        logging.info(f"Траты по категории '{category}' за период {start_date_str}-{end_date}: {response_data}")
        return json.dumps(response_data, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при расчете трендов трат: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)
