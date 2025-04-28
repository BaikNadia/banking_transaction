import logging
import os

from src.services import (
    profitable_categories,
    investment_piggy_bank,
    simple_search,
    find_phone_numbers,
    find_physical_transfers
)
from src.utils import read_excel_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", "operations.xlsx")

    # Чтение данных из Excel-файла
    df = read_excel_file(file_path)
    if df.empty:
        print("Файл не найден или пуст.")
        exit(1)

    # Преобразование DataFrame в список словарей
    transactions = df.to_dict(orient="records")

    # 1. Выгодные категории
    print("\nВыгодные категории:")
    result_profitable = profitable_categories(transactions, 2021, 9)
    print(result_profitable)

    # 2. Инвесткопилка
    print("\nИнвесткопилка:")
    result_investment = investment_piggy_bank(transactions, 9, 50)
    print(result_investment)

    # 3. Простой поиск
    print("\nПростой поиск:")
    try:
        result_simple_search = simple_search("Фастфуд", transactions)
        print(result_simple_search)
    except Exception as e:
        logging.error(f"Ошибка при выполнении простого поиска: {e}")

    # 4. Поиск по телефонным номерам
    print("\nПоиск по телефонным номерам:")
    result_phone_search = find_phone_numbers(transactions)
    print(result_phone_search)

    # 5. Поиск переводов физическим лицам
    print("\nПоиск переводов физическим лицам:")
    result_physical_transfers = find_physical_transfers(transactions)
    print(result_physical_transfers)
