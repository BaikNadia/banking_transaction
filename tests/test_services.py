import pytest
from src.services import (
    profitable_categories,
    investment_piggy_bank,
    simple_search,
    find_phone_numbers,
    find_physical_transfers
)
from datetime import datetime
import json


@pytest.mark.parametrize(
    "year, month, expected",
    [
        (2023, 9, {"Фастфуд": 100, "Супермаркеты": 200}),
        (2023, 12, {"Транспорт": 300}),
    ]
)
def test_profitable_categories(year, month, expected):
    mock_transactions = [
        {"Дата операции": datetime(2023, 9, 1), "Сумма операции": -100, "Категория": "Фастфуд"},
        {"Дата операции": datetime(2023, 9, 2), "Сумма операции": -200, "Категория": "Супермаркеты"},
        {"Дата операции": datetime(2023, 12, 1), "Сумма операции": -300, "Категория": "Транспорт"},
    ]

    result = json.loads(profitable_categories(mock_transactions, year, month))
    assert isinstance(result, dict)
    assert all(category in result for category in expected)
    assert all(abs(result[category] - expected[category]) < 0.01 for category in expected)

@pytest.mark.parametrize(
    "month, limit, expected",
    [
        (9, 50, 27),  # Новое значение для месяца 9 и лимита 50
        (12, 100, 127),  # Новое значение для месяца 12 и лимита 100
    ]
)
def test_investment_piggy_bank(month, limit, expected):
    mock_transactions = [
        {"Дата операции": datetime(2023, month, 1), "Сумма операции": -45},
        {"Дата операции": datetime(2023, month, 2), "Сумма операции": -98},
        {"Дата операции": datetime(2023, month, 3), "Сумма операции": -140},  # Добавляем дополнительные транзакции
        {"Дата операции": datetime(2023, month, 4), "Сумма операции": -190},
    ]

    def calculate_rounding_difference(amount: float) -> float:
        rounded_amount = ((abs(amount) // limit) + 1) * limit
        return rounded_amount - abs(amount)

    expected_sum = sum(calculate_rounding_difference(t["Сумма операции"]) for t in mock_transactions)

    result = json.loads(investment_piggy_bank(mock_transactions, month, limit))
    assert isinstance(result, dict)
    assert abs(result["total_investment"] - expected_sum) < 0.01  # Проверяем результат

@pytest.mark.parametrize(
    "query, expected_count",
    [
        ("Фастфуд", 2),
        ("Магнит", 3),
    ]
)
def test_simple_search(query, expected_count):
    mock_transactions = [
        {"Описание": "IP Yakubovskaya M.V.", "Категория": "Фастфуд"},
        {"Описание": "SPAR", "Категория": "Супермаркеты"},
        {"Описание": "Магнит", "Категория": "Супермаркеты"},
        {"Описание": "Магнит2", "Категория": "Супермаркеты"},
        {"Описание": "Фастфуд", "Категория": "Другое"},
        {"Описание": "Магнит3", "Категория": "Супермаркеты"},  # Добавляем дополнительное совпадение
    ]

    result = json.loads(simple_search(query, mock_transactions))
    assert isinstance(result, dict)
    assert len(result["results"]) == expected_count

@pytest.mark.parametrize(
    "expected_count",
    [2]
)
def test_find_phone_numbers(expected_count):
    mock_transactions = [
        {"Описание": "+7 921 11-22-33", "Категория": "Телефоны"},
        {"Описание": "+79955555555", "Категория": "Телефоны"},  # Добавляем номер без пробелов
        {"Описание": "Перевод на карту", "Категория": "Переводы"},
    ]

    result = json.loads(find_phone_numbers(mock_transactions))
    assert isinstance(result, dict)
    assert len(result["results"]) == expected_count

@pytest.mark.parametrize(
    "expected_count",
    [3]
)
def test_find_physical_transfers(expected_count):
    mock_transactions = [
        {"Описание": "Валерий А.", "Категория": "Переводы"},
        {"Описание": "Сергей З.", "Категория": "Переводы"},
        {"Описание": "Иван Иванович", "Категория": "Переводы"},  # Добавляем имя с двойной буквой
        {"Описание": "IP Yakubovskaya", "Категория": "Фастфуд"},
    ]

    result = json.loads(find_physical_transfers(mock_transactions))
    assert isinstance(result, dict)
    assert len(result["results"]) == expected_count
