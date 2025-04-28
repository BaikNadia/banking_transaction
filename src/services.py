import json
import logging
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Сервис «Выгодные категории повышенного кэшбэка»

def profitable_categories(transactions: List[Dict], year: int, month: int) -> str:
    """
    Анализирует выгодные категории повышенного кэшбэка за указанный год и месяц.

    :param transactions: Список словарей с транзакциями.
    :param year: Год анализа.
    :param month: Месяц анализа.
    :return: JSON-ответ с анализом по категориям.
    """
    try:
        # Фильтрация транзакций по году и месяцу
        filtered_transactions = [
            t for t in transactions
            if "Дата операции" in t and
               isinstance(t["Дата операции"], datetime) and
               t["Дата операции"].year == year and
               t["Дата операции"].month == month
        ]

        # Группировка транзакций по категориям
        category_sums = defaultdict(float)
        for t in filtered_transactions:
            if "Категория" in t and "Сумма операции" in t:
                category = t["Категория"]
                amount = abs(float(t["Сумма операции"]))
                category_sums[category] += amount

        # Отбор топ-3 категорий по сумме расходов
        top_categories = dict(sorted(category_sums.items(), key=lambda x: x[1], reverse=True)[:3])

        # Логирование результата
        logging.info(f"Выгодные категории за {year}-{month}: {top_categories}")

        return json.dumps(top_categories, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при расчете выгодных категорий: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)


# Сервис «Инвесткопилка»

def investment_piggy_bank(transactions: list, month: int, rounding_limit: int) -> str:
    """
    Расчет суммы для инвесткопилки через округление трат.

    :param transactions: Список словарей с транзакциями.
    :param month: Месяц для анализа.
    :param rounding_limit: Лимит округления (например, 50 или 100).
    :return: JSON-ответ с рассчитанной суммой.
    """
    try:
        current_year = datetime.now().year

        # Фильтрация транзакций по месяцу текущего года
        filtered_transactions = [
            t for t in transactions
            if "Дата операции" in t and isinstance(t["Дата операции"], datetime) and
               t["Дата операции"].year == current_year and
               t["Дата операции"].month == month and
               float(t["Сумма операции"]) < 0  # Только расходы
        ]

        def calculate_rounding_difference(amount: float) -> float:
            rounded_amount = ((abs(amount) // rounding_limit) + 1) * rounding_limit
            return rounded_amount - abs(amount)

        total_investment = sum(
            calculate_rounding_difference(float(t["Сумма операции"]))
            for t in filtered_transactions
        )

        return json.dumps({"total_investment": total_investment}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при расчете инвесткопилки: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)


# Сервис «Простой поиск»

def simple_search(query: str, transactions: List[Dict]) -> str:
    """
    Выполняет простой поиск среди описаний и категорий транзакций.

    :param query: Строка запроса для поиска.
    :param transactions: Список словарей с транзакциями.
    :return: JSON-ответ со списком найденных транзакций.
    """
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    search_results = [
        {key: value.isoformat() if isinstance(value, datetime) else value for key, value in t.items()}
        for t in transactions
        if ("Описание" in t and pattern.search(str(t["Описание"]))) or
           ("Категория" in t and pattern.search(str(t["Категория"])))
    ]

    return json.dumps({"results": search_results}, ensure_ascii=False, indent=4)


# Сервис «Поиск по телефонным номерам»

import re


def find_phone_numbers(transactions: List[Dict]) -> str:
    """
    Находит транзакции, содержащие телефонные номера.

    :param transactions: Список словарей с транзакциями.
    :return: JSON-ответ со списком найденных транзакций.
    """
    phone_pattern = re.compile(r"\+7\s?\d{3}\s?\d{2}-\d{2}-\d{2}", re.IGNORECASE)
    phone_results = [
        {key: value.isoformat() if isinstance(value, datetime) else value for key, value in t.items()}
        for t in transactions
        if "Описание" in t and phone_pattern.search(str(t["Описание"]))
    ]

    return json.dumps({"results": phone_results}, ensure_ascii=False, indent=4)


# Сервис «Поиск переводов физическим лицам»

def find_physical_transfers(transactions: list) -> str:
    physical_transfer_pattern = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$|[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+$", re.IGNORECASE)
    transfer_results = [
        {key: value.isoformat() if isinstance(value, datetime) else value
         for key, value in t.items()}
        for t in transactions if "Категория" in t and t["Категория"] == "Переводы" and
                                 "Описание" in t and physical_transfer_pattern.match(str(t["Описание"]).strip())
    ]

    return json.dumps({"results": transfer_results}, ensure_ascii=False, indent=4)
