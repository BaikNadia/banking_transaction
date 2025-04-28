# src/services.py

import json
import logging
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

import pandas as pd

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

def investment_piggy_bank(transactions: List[Dict], month: int, rounding_limit: int) -> str:
    """
    Расчитывает сумму для инвесткопилки через округление трат.

    :param transactions: Список словарей с транзакциями.
    :param month: Месяц для анализа.
    :param rounding_limit: Лимит округления.
    :return: JSON-ответ с рассчитанной суммой.
    """
    try:
        current_year = datetime.now().year

        # Фильтрация транзакций по месяцу текущего года
        filtered_transactions = [
            t for t in transactions
            if "Дата операции" in t and isinstance(t["Дата операции"], datetime) and
               t["Дата операции"].year == current_year and
               t["Дата операции"].month == month
        ]

        # Расчет разницы между фактической суммой и округленной
        def calculate_rounding_difference(amount: float) -> float:
            rounded_amount = ((abs(amount) // rounding_limit) + 1) * rounding_limit
            return rounded_amount - abs(amount)

        total_investment = sum(
            calculate_rounding_difference(float(t["Сумма операции"]))
            for t in filtered_transactions
            if "Сумма операции" in t and float(t["Сумма операции"]) < 0
        )

        return json.dumps({"total_investment": total_investment}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при расчете инвесткопилки: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)

# Сервис «Простой поиск»

def simple_search(query: str, transactions: List[Dict]) -> str:
    """
    Выполняет простой поиск среди транзакций.

    :param query: Строка запроса.
    :param transactions: Список словарей с транзакциями.
    :return: JSON-ответ со списком найденных транзакций.
    """
    try:
        # Проверяем наличие текстовых полей (Описание, Категория)
        search_results = [
            t for t in transactions
            if ("Описание" in t and query.lower() in t["Описание"].lower()) or
               ("Категория" in t and query.lower() in t["Категория"].lower())
        ]

        return json.dumps({"results": search_results}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при выполнении простого поиска: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)


# Сервис «Поиск по телефонным номерам»

import re

def find_phone_numbers(transactions: List[Dict]) -> str:
    """
    Находит транзакции, содержащие телефонные номера.

    :param transactions: Список словарей с транзакциями.
    :return: JSON-ответ со списком найденных транзакций.
    """
    try:
        # Регулярное выражение для поиска телефонных номеров
        phone_pattern = re.compile(r"\+7\s?\d{3}\s?\d{2}-\d{2}-\d{2}", re.IGNORECASE)

        # Поиск транзакций с телефонными номерами
        phone_results = [
            {key: (value.isoformat() if isinstance(value, pd.Timestamp) else value)
             for key, value in t.items()}
            for t in transactions if "Описание" in t and phone_pattern.search(t["Описание"])
        ]

        return json.dumps({"results": phone_results}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при поиске телефонных номеров: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)

# Сервис «Поиск переводов физическим лицам»

def find_physical_transfers(transactions: List[Dict]) -> str:
    """
    Находит переводы физическим лицам.

    :param transactions: Список словарей с транзакциями.
    :return: JSON-ответ со списком найденных транзакций.
    """
    try:
        # Регулярное выражение для поиска имени и первой буквы фамилии
        physical_transfer_pattern = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$", re.IGNORECASE)

        # Поиск переводов физлицам
        transfer_results = [
            {key: (value.isoformat() if isinstance(value, pd.Timestamp) else value)
             for key, value in t.items()}
            for t in transactions if "Категория" in t and t["Категория"] == "Переводы" and
                                  "Описание" in t and physical_transfer_pattern.match(t["Описание"].strip())
        ]

        return json.dumps({"results": transfer_results}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при поиске переводов физическим лицам: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)
