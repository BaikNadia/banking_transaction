import pandas as pd

import utils
import services
import reports
from datetime import datetime
import json


def main():
    """Основная функция для запуска анализа транзакций."""

    print("=== Загрузка транзакций из Excel-файла ===")
    transactions = utils.load_transactions()
    print(f"Загружено {len(transactions)} транзакций")
    print(json.dumps(transactions[:2], indent=2, ensure_ascii=False))  # Пример первых 2 транзакций

    print("\n=== Получение курсов валют ===")
    exchange_rates = utils.get_exchange_rates()
    print(f"Курсы валют (USD): {json.dumps(exchange_rates, indent=2, ensure_ascii=False)}")

    print("\n=== Получение данных о S&P 500 ===")
    sp500_data = utils.get_sp500_data()
    print(f"S&P 500: {json.dumps(sp500_data, indent=2, ensure_ascii=False)}")

    print("\n=== Фильтрация транзакций по дате ===")
    date_str = input("Введите дату фильтрации (YYYY-MM-DD HH:MM:SS): ")
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        filtered = [t for t in transactions if
                    datetime.strptime(t['Дата операции'], "%d.%m.%Y %H:%M:%S") <= target_date]
        print(f"Найдено {len(filtered)} транзакций до {date_str}")
        print(json.dumps(filtered[:2], indent=2, ensure_ascii=False))  # Пример первых 2 транзакций
    except ValueError:
        print("Ошибка: Неверный формат даты")

    print("\n=== Поиск транзакций ===")
    search_query = input("Введите строку для поиска: ")
    search_result = services.search_transactions(search_query, transactions)
    print(f"Результаты поиска для '{search_query}': {search_result}")

    print("\n=== Отчет по дням недели ===")
    date_filter = input("Введите дату для фильтрации отчета (YYYY-MM-DD, Enter для пропуска): ")
    df = pd.DataFrame(transactions)
    weekday_report = reports.spending_by_weekday(df, date_filter or None)
    print(f"Расходы по дням недели: {weekday_report}")


if __name__ == "__main__":
    main()
