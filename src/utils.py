import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


def load_transactions(file_path=None):
    """
    Загружает транзакции из Excel-файла.

    Args:
        file_path (str): Путь к Excel-файлу с транзакциями.

    Returns:
        List[Dict]: Список транзакций в формате словарей или пустой список при ошибке.
    """

    if not file_path:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, "..", "data", "operations.xlsx")

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        df = pd.read_excel(file_path)
        return df.to_dict(orient='records')
    except Exception as e:
        logging.error(f"Error loading transactions: {e}")
        return []


def get_exchange_rates():
    """
    Получает текущие курсы валют через Exchange Rate API.

    Returns:
        Dict: Курсы валют относительно USD или пустой словарь при ошибке.
    """
    url = f"https://v6.exchangerate-api.com/v6/{os.getenv('EXCHANGE_RATE_API_KEY')}/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['conversion_rates']
    except Exception as e:
        logging.error(f"Exchange rate API error: {e}")
        return {}


def get_sp500_data():
    """
    Получает данные о S&P 500 через Alpha Vantage API.

    Returns:
        List[Dict]: Последние 5 записей о S&P 500 или пустой список при ошибке.
    """
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPX&apikey=demo"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return list(data.get('Time Series Daily Adjusted', {}).values())[:5]
    except Exception as e:
        logging.error(f"S&P 500 API error: {e}")
        return []
