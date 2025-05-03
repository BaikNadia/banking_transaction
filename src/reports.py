import json
import logging

import pandas as pd


def spending_by_weekday(df, date_filter=None):
    """
    Генерирует отчет о расходах по дням недели.

    Args:
        df (pd.DataFrame): DataFrame с транзакциями.
        date_filter (str, optional): Фильтр по дате в формате YYYY-MM-DD.

    Returns:
        str: JSON-строка с суммарными расходами по дням недели.
    """
    try:
        if date_filter:
            df = df[df['Дата операции'] <= pd.to_datetime(date_filter)]
        df['Дата операции'] = pd.to_datetime(df['Дата операции'])
        df['День недели'] = df['Дата операции'].dt.day_name()
        grouped = df.groupby('День недели')['Сумма операции'].sum().to_dict()
        return json.dumps(grouped, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Weekday report error: {e}")
        return json.dumps({})
