import json
from datetime import datetime
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def profitable_categories(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Анализирует выгодность категорий для выбора повышенного кэшбэка.

    :param data: Список словарей с транзакциями.
    :param year: Год анализа.
    :param month: Месяц анализа.
    :return: JSON-ответ с анализом кэшбэка по категориям.
    """
    try:
        # Преобразование даты операции в объект datetime
        filtered_data = filter(
            lambda x: (
                datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").year == year and
                datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").month == month
            ),
            data
        )

        # Фильтрация только расходов (отрицательных сумм)
        expenses = filter(lambda x: float(x["Сумма операции"]) < 0, filtered_data)

        # Группировка по категориям и подсчет возможного кэшбэка
        category_analysis = {}
        for transaction in expenses:
            category = transaction.get("Категория", "Неизвестная категория")
            amount = abs(float(transaction["Сумма операции"]))
            cashback_rate = 0.25  # Предполагаемый процент кэшбэка для расчета
            if category not in category_analysis:
                category_analysis[category] = 0
            category_analysis[category] += amount * cashback_rate

        # Логирование результата
        logging.info(f"Проанализированы выгодные категории за {year}-{month}: {category_analysis}")

        return json.dumps(category_analysis, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при анализе выгодных категорий: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)


# Инвесткопилка

def investment_bank(transactions: List[Dict[str, Any]], limit: int, month: str) -> str:
    """
    Рассчитывает сумму, которую можно отложить в «Инвесткопилку» через округление.

    :param transactions: Список словарей с транзакциями.
    :param limit: Предел округления (10, 50 или 100).
    :param month: Месяц для анализа (строка в формате 'YYYY-MM').
    :return: JSON-ответ с рассчитанной суммой.
    """
    try:
        # Фильтрация транзакций по указанному месяцу
        filtered_transactions = filter(
            lambda x: datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%Y-%m") == month,
            transactions
        )

        # Расчет разницы между фактической суммой и округленной
        def calculate_rounding_difference(amount: float) -> float:
            rounded_amount = (abs(amount) // limit + 1) * limit
            return rounded_amount - abs(amount)

        # Применение функции к каждой транзакции
        rounding_differences = map(
            lambda x: calculate_rounding_difference(float(x["Сумма операции"])) if float(x["Сумма операции"]) < 0 else 0,
            filtered_transactions
        )

        # Подсчет общей суммы для инвесткопилки
        total_investment = sum(rounding_differences)

        # Логирование результата
        logging.info(f"Рассчитана сумма для инвесткопилки за {month} с пределом {limit}: {total_investment}")

        return json.dumps({"total_investment": total_investment}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при расчете инвесткопилки: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)


# Простой поиск

import re

def simple_search(data: List[Dict[str, Any]], query: str) -> str:
    """
    Выполняет простой поиск среди описаний и категорий транзакций.

    :param data: Список словарей с транзакциями.
    :param query: Строка запроса для поиска.
    :return: JSON-ответ со списком найденных транзакций.
    """
    try:
        # Поиск по описанию и категории
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        search_results = filter(
            lambda x: pattern.search(x.get("Описание", "")) or pattern.search(x.get("Категория", "")),
            data
        )

        # Преобразование результатов в список словарей
        results_list = list(search_results)

        # Логирование результата
        logging.info(f"Найдено {len(results_list)} транзакций по запросу \"{query}\".")

        return json.dumps({"results": results_list}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при выполнении простого поиска: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)

# Поиск по телефонным номерам

def find_phone_numbers(data: List[Dict[str, Any]]) -> str:
    """
    Находит транзакции, содержащие телефонные номера в описании.

    :param data: Список словарей с транзакциями.
    :return: JSON-ответ со списком найденных транзакций.
    """
    try:
        # Регулярное выражение для поиска телефонных номеров
        phone_pattern = re.compile(r"\+7\s?\d{3}\s?\d{2}-\d{2}-\d{2}", re.IGNORECASE)

        # Поиск транзакций с телефонными номерами
        phone_results = filter(
            lambda x: phone_pattern.search(x.get("Описание", "")),
            data
        )

        # Преобразование результатов в список словарей
        results_list = list(phone_results)

        # Логирование результата
        logging.info(f"Найдено {len(results_list)} транзакций с телефонными номерами.")

        return json.dumps({"results": results_list}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при поиске телефонных номеров: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)

# Поиск переводов физическим лицам

def find_physical_transfers(data: List[Dict[str, Any]]) -> str:
    """
    Находит переводы физическим лицам.

    :param data: Список словарей с транзакциями.
    :return: JSON-ответ со списком найденных транзакций.
    """
    try:
        # Регулярное выражение для поиска имени и первой буквы фамилии
        physical_transfer_pattern = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$", re.IGNORECASE)

        # Поиск переводов физлицам
        transfer_results = filter(
            lambda x: x.get("Категория", "").strip() == "Переводы" and
                     physical_transfer_pattern.match(x.get("Описание", "").strip()),
            data
        )

        # Преобразование результатов в список словарей
        results_list = list(transfer_results)

        # Логирование результата
        logging.info(f"Найдено {len(results_list)} переводов физическим лицам.")

        return json.dumps({"results": results_list}, ensure_ascii=False, indent=4)

    except Exception as e:
        logging.error(f"Ошибка при поиске переводов физическим лицам: {e}")
        return json.dumps({"error": "Internal server error"}, ensure_ascii=False, indent=4)

