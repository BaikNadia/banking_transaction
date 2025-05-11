# import pandas as pd

# import utils
# import services
# import reports
# from datetime import datetime
# import json


# def main_views():
#     """Основная функция для запуска анализа транзакций."""

#     print("=== Загрузка транзакций из Excel-файла ===")
#     transactions = utils.load_transactions()
#     print(f"Загружено {len(transactions)} транзакций")
#     print(json.dumps(transactions[:2], indent=2, ensure_ascii=False))  # Пример первых 2 транзакций

#     print("\n=== Получение курсов валют ===")
#     exchange_rates = utils.get_exchange_rates()
#     print(f"Курсы валют (USD): {json.dumps(exchange_rates, indent=2, ensure_ascii=False)}")

#     print("\n=== Получение данных о S&P 500 ===")
#     sp500_data = utils.get_sp500_data()
#     print(f"S&P 500: {json.dumps(sp500_data, indent=2, ensure_ascii=False)}")

#     print("\n=== Фильтрация транзакций по дате ===")
#     date_str = input("Введите дату фильтрации (YYYY-MM-DD HH:MM:SS): ")
#     try:
#         target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#         filtered = [t for t in transactions if
#                     datetime.strptime(t['Дата операции'], "%d.%m.%Y %H:%M:%S") <= target_date]
#         print(f"Найдено {len(filtered)} транзакций до {date_str}")
#         print(json.dumps(filtered[:2], indent=2, ensure_ascii=False))  # Пример первых 2 транзакций
#     except ValueError:
#         print("Ошибка: Неверный формат даты")

#     print("\n=== Поиск транзакций ===")
#     search_query = input("Введите строку для поиска: ")
#     search_result = services.search_transactions(search_query, transactions)
#     print(f"Результаты поиска для '{search_query}': {search_result}")

#     print("\n=== Отчет по дням недели ===")
#     date_filter = input("Введите дату для фильтрации отчета (YYYY-MM-DD, Enter для пропуска): ")
#     df = pd.DataFrame(transactions)
#     weekday_report = reports.spending_by_weekday(df, date_filter or None)
#     print(f"Расходы по дням недели: {weekday_report}")


# if __name__ == "__main__":
#     main_views()

import json
import logging
from datetime import datetime

import pandas as pd

from src.utils import load_transactions, get_exchange_rates, get_sp500_data

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_greeting():
    """Генерирует приветствие в зависимости от текущего времени"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_stats(transactions):
    """Собирает статистику по картам"""
    card_groups = {}

    for t in transactions:
        card = t.get('Номер карты', '')
        amount = t.get('Сумма операции', 0)

        # Пропускаем ненужные записи
        if pd.isna(card) or not card or card == "*":
            continue
        if amount >= 0:
            continue  # Пропускаем пополнения

        # Преобразуем номер карты к строке
        if isinstance(card, (float, int)):
            card_str = str(int(card)) if card != "*" else str(card)
        else:
            card_str = str(card)

        card_key = card_str[-4:]  # Последние 4 цифры
        if card_key not in card_groups:
            card_groups[card_key] = {"total_spent": 0, "cashback": 0}

        card_groups[card_key]["total_spent"] += abs(amount)
        card_groups[card_key]["cashback"] += abs(amount) / 100  # Используем дробное деление

    # Округляем кэшбэк до 2 знаков после запятой
    return [{"last_digits": k, "total_spent": v["total_spent"], "cashback": round(v["cashback"], 2)}
            for k, v in card_groups.items()]


def get_top_transactions(transactions):
    """Возвращает топ-5 транзакций по сумме платежа"""
    valid_transactions = [t for t in transactions if t.get('Сумма операции', 0) < 0]

    return [{
        "date": t.get("Дата операции", "Неизвестно").split()[0],  # Обработка отсутствующего ключа
        "amount": abs(t.get("Сумма операции", 0)),
        "category": t.get("Категория", "Неизвестно"),  # Обработка отсутствующего ключа
        "description": t.get("Описание", "Неизвестно")  # Обработка отсутствующего ключа
    } for t in sorted(valid_transactions, key=lambda x: abs(x.get("Сумма операции", 0)), reverse=True)[:5]]


def format_currency_rates(rates):
    """Форматирует курсы валют в нужный формат"""
    return [{"currency": k, "rate": v} for k, v in rates.items()]


def format_stock_prices(stocks):
    """
    Форматирует цены акций в нужный формат

    Args:
        stocks (List[Dict]): Список с данными о ценах акций

    Returns:
        List[Dict]: Список акций с ценами или пустой список
    """
    if not stocks:
        return []  # Возвращаем пустой список, если данных нет

    return [{"stock": k, "price": float(v)} for k, v in stocks[0].items()]


def generate_report(date_str):
    """
    Основная функция для генерации полного отчета

    Args:
        date_str (str): Дата в формате YYYY-MM-DD HH:MM:SS

    Returns:
        Dict: JSON-словарь с результатами анализа
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"error": "Неверный формат даты"}

    # Фильтрация транзакций (начало месяца - текущая дата)
    start_of_month = target_date.replace(day=1, hour=0, minute=0, second=0)
    filtered_transactions = [
        t for t in load_transactions()
        if target_date >= datetime.strptime(t['Дата операции'], "%d.%m.%Y %H:%M:%S") >= start_of_month
    ]

    report = {
        "greeting": get_greeting(),
        "cards": get_card_stats(filtered_transactions),
        "top_transactions": get_top_transactions(filtered_transactions),
        "currency_rates": format_currency_rates(get_exchange_rates()),
        "stock_prices": format_stock_prices(get_sp500_data())
    }

    return report


if __name__ == "__main__":
    # Пример использования
    result = generate_report("2020-05-20 15:30:00")
    print(json.dumps(result, ensure_ascii=False, indent=2))
