import json

import pandas as pd
import pytest

from src.reports import spending_by_weekday


# Тестовые данные
@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": [
            "12.05.2021 13:57:38",  # Среда
            "12.05.2021 13:15:26",  # Среда
            "13.05.2021 10:00:00",  # Четверг
            "14.05.2021 15:30:00",  # Пятница
            "15.05.2021 09:45:12",  # Суббота
            "16.05.2021 18:22:05",  # Воскресенье
            "17.05.2021 20:00:00",  # Понедельник
            "18.05.2021 14:14:14"  # Вторник
        ],
        "Сумма операции": [-7900, -120, -200, -300, -400, -500, -600, -700]
    }
    return pd.DataFrame(data)


# Тест с пустым DataFrame
def test_empty_dataframe():
    result = spending_by_weekday(pd.DataFrame())
    assert result == "{}"


# Тест без фильтрации по дате
def test_without_date_filter(sample_transactions):
    result = spending_by_weekday(sample_transactions)
    data = json.loads(result)
    assert "Среда" in data
    assert data["Среда"] == -8020  # Сумма -7900 + (-120)


# Тест с фильтрацией по дате
def test_with_date_filter(sample_transactions):
    result = spending_by_weekday(sample_transactions, date_filter="2021-05-13")
    data = json.loads(result)
    assert "Понедельник" not in data
    assert "Вторник" not in data
    assert data["Среда"] == -8020


# Тест с некорректной датой фильтрации
def test_invalid_date_filter(sample_transactions):
    result = spending_by_weekday(sample_transactions, date_filter="некорректная_дата")
    assert result == "{}"


# Тест с отсутствующим столбцом 'Дата операции'
def test_missing_date_column():
    df = pd.DataFrame({"Сумма операции": [-100, -200]})
    result = spending_by_weekday(df)
    assert result == "{}"


# Тест с некорректным форматом даты
def test_invalid_date_format():
    df = pd.DataFrame({
        "Дата операции": ["12/05/2021", "13-05-2021"],
        "Сумма операции": [-100, -200]
    })
    result = spending_by_weekday(df)
    assert result == "{}"


# Параметризованный тест для разных дней недели
@pytest.mark.parametrize("transactions,expected_days", [
    (
            pd.DataFrame({
                "Дата операции": ["12.05.2021 13:57:38", "12.05.2021 13:15:26"],
                "Сумма операции": [-7900, -120]
            }),
            {"Понедельник": -8020}
    ),
    (
            pd.DataFrame({
                "Дата операции": ["13.05.2021 10:00:00", "14.05.2021 15:30:00"],
                "Сумма операции": [-200, -300]
            }),
            {"Вторник": -200, "Среда": -300}
    )
])
def test_spending_by_weekday_parametrized(transactions, expected_days):
    result = spending_by_weekday(transactions)
    data = json.loads(result)
    for day, amount in expected_days.items():
        assert data.get(day) == amount


# Тест с отрицательными и положительными суммами
def test_positive_and_negative_amounts():
    df = pd.DataFrame({
        "Дата операции": [
            "12.05.2021 13:57:38",  # Среда
            "12.05.2021 13:15:26",  # Среда
            "13.05.2021 10:00:00"  # Четверг
        ],
        "Сумма операции": [1000, -200, -300]  # Доход и расход
    })
    result = spending_by_weekday(df)
    data = json.loads(result)
    assert "Среда" in data
    assert data["Среда"] == 800  # 1000 - 200
    assert data["Четверг"] == -300


# Тест с несколькими транзакциями в один день
def test_multiple_transactions_same_day():
    df = pd.DataFrame({
        "Дата операции": ["12.05.2021 13:57:38"] * 5,
        "Сумма операции": [-100, -200, -300, -400, -500]
    })
    result = spending_by_weekday(df)
    data = json.loads(result)
    assert "Среда" in data
    assert data["Среда"] == -1500


# Тест с фильтром, который исключает все транзакции
def test_date_filter_excludes_all(sample_transactions):
    result = spending_by_weekday(sample_transactions, date_filter="2020-01-01")
    assert result == "{}"


# Тест с NaN в столбце даты
def test_nan_date_handling():
    df = pd.DataFrame({
        "Дата операции": ["12.05.2021 13:57:38", None, "13.05.2021 10:00:00"],
        "Сумма операции": [-7900, -120, -200]
    })
    result = spending_by_weekday(df)
    data = json.loads(result)
    assert "Среда" in data
    assert data["Среда"] == -7900  # NaN-транзакция не учитывается
