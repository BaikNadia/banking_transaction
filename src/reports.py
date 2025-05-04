import json
import logging

import pandas as pd
from win32ctypes.pywin32.pywintypes import datetime


def spending_by_weekday(df, date_filter=None):
    """
    Генерирует отчет о расходах по дням недели.

    Args:
        df (pd.DataFrame): DataFrame с транзакциями.
        date_filter (str, optional): Фильтр по дате в формате YYYY-MM-DD.

    Returns:
        str: JSON-строка с суммарными расходами по дням недели.
    """
    if not date_filter:
        date_filter = datetime.now().date()
        print(date_filter)
    try:
        if date_filter:
            start_date = pd.to_datetime(date_filter, dayfirst=True) - pd.DateOffset(months=3)

            df = start_date <= df[pd.to_datetime(df['Дата операции'], dayfirst=True) <= pd.to_datetime(date_filter, dayfirst=True)]

        df['День недели'] = pd.to_datetime(df['Дата операции'], dayfirst=True).dt.day_name(locale="ru")
        grouped = df.groupby('День недели')['Сумма операции'].sum().to_dict()
        return json.dumps(grouped, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Weekday report error: {e}")
        return json.dumps({})

if __name__ == "__main__":
    data = {
        "Дата операции": [
            "12.05.2021 13:57:38",  # Понедельник
            "12.05.2021 13:15:26",  # Понедельник
            "13.05.2021 10:00:00",  # Вторник
            "14.05.2021 15:30:00",  # Среда
            "15.05.2021 09:45:12",  # Четверг
            "16.05.2021 18:22:05",  # Пятница
            "17.05.2021 20:00:00",  # Суббота
            "18.05.2021 14:14:14"  # Воскресенье
        ],
        "Сумма операции": [-7900, -120, -200, -300, -400, -500, -600, -700]
    }
    data_df = pd.DataFrame(data)
    print(spending_by_weekday(data_df))
