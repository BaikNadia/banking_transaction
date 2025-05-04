import pytest
import json
import logging
from src.services import search_transactions

# Тестовые данные
@pytest.fixture
def sample_transactions():
    return [
        {
            "Дата операции": "02.06.2019 17:46:06",
            "Описание": "Колхоз",
            "Категория": "Супермаркеты"
        },
        {
            "Дата операции": "02.06.2019 15:33:54",
            "Описание": "Яндекс Такси",
            "Категория": "Транспорт"
        },
        {
            "Дата операции": "02.06.2019 08:27:24",
            "Описание": "IP Yakubovskaya M. V.",
            "Категория": "Фастфуд"
        }
    ]

# Успешный поиск по описанию
def test_search_by_description(sample_transactions):
    result = search_transactions("колхоз", sample_transactions)
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Описание"] == "Колхоз"

# Успешный поиск по категории
def test_search_by_category(sample_transactions):
    result = search_transactions("транспорт", sample_transactions)
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Категория"] == "Транспорт"

# Регистронезависимый поиск
def test_case_insensitive_search(sample_transactions):
    result = search_transactions("КОЛХОЗ", sample_transactions)
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Описание"] == "Колхоз"

# Поиск без совпадений
def test_no_matches(sample_transactions):
    result = search_transactions("ресторан", sample_transactions)
    assert result == "[]"

# Поиск с частичным совпадением
def test_partial_match(sample_transactions):
    result = search_transactions("кофе", [
        {"Описание": "Кофейня", "Категория": "Кафе"},
        {"Описание": "Багги", "Категория": "Техника"}
    ])
    data = json.loads(result)
    assert len(data) == 1
    assert "Кофейня" in data[0]["Описание"]

# Проверка пустого запроса
def test_empty_query(sample_transactions):
    result = search_transactions("", sample_transactions)
    data = json.loads(result)
    assert len(data) == 3  # Возвращает все транзакции

# Проверка некорректных данных
def test_invalid_transactions_format(caplog):
    with caplog.at_level(logging.ERROR):
        result = search_transactions("test", "не список")
        assert result == "[]"
        assert "Search error:" in caplog.text

# Параметризованный тест
@pytest.mark.parametrize("query,expected_count", [
    ("колхоз", 1),
    ("такси", 1),
    ("фастфуд", 1),
    ("не_существует", 0),
    ("", 3)
])
def test_search_variants(sample_transactions, query, expected_count):
    result = search_transactions(query, sample_transactions)
    if expected_count == 0:
        assert result == "[]"
    else:
        data = json.loads(result)
        assert len(data) == expected_count
