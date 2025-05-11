# import os
# import sys
# from io import StringIO
# from unittest.mock import patch

# import pytest

# Убедитесь что путь корректен
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.views import main_views


# @pytest.fixture
# def sample_transactions():
#     return [{
#        "Дата операции": "01.01.2023 12:00:00",
#         "Сумма": "100",
#         "Валюта": "USD",
#        "Категория": "Еда",
#        "Описание": "Обед"
#     }]


# def test_main_views(sample_transactions):
#     with patch('src.views.utils.load_transactions') as mock_load, \
#             patch('src.views.utils.get_exchange_rates') as mock_rates, \
#             patch('src.views.utils.get_sp500_data') as mock_sp500, \
#             patch('src.views.services.search_transactions') as mock_search, \
#             patch('src.views.reports.spending_by_weekday') as mock_report, \
#            patch('builtins.input', side_effect=["2023-01-02 00:00:00", "", ""]), \
#            patch('sys.stdout', new_callable=StringIO) as mock_stdout:
#         mock_load.return_value = sample_transactions
#         mock_rates.return_value = {"USD": 1.0}
#         mock_sp500.return_value = {}
#         mock_search.return_value = []
#         mock_report.return_value = {}

#        main_views()

#        output = mock_stdout.getvalue()
#        assert "=== Загрузка транзакций из Excel-файла ===" in output


from unittest.mock import patch, MagicMock

import pytest

from src.views import get_greeting, get_card_stats, get_top_transactions, format_currency_rates, format_stock_prices

# Тест для get_greeting
def test_greeting_times():
    """Тест приветствий в зависимости от времени"""
    with patch('src.views.datetime') as mock_datetime:
        mock_datetime.now.return_value = MagicMock(hour=8)
        assert get_greeting() == "Доброе утро"

        mock_datetime.now.return_value = MagicMock(hour=14)
        assert get_greeting() == "Добрый день"

        mock_datetime.now.return_value = MagicMock(hour=21)
        assert get_greeting() == "Добрый вечер"

        mock_datetime.now.return_value = MagicMock(hour=2)
        assert get_greeting() == "Доброй ночи"


# Тест для get_card_stats
def test_get_card_stats():
    """Тест расчета кэшбэка по картам"""
    transactions = [
        {"Номер карты": "*7197", "Сумма операции": -87},
        {"Номер карты": "*4556", "Сумма операции": -305},
        {"Номер карты": float("nan"), "Сумма операции": -100},  # NaN
        {"Номер карты": "", "Сумма операции": -200},  # Пустая строка
        {"Номер карты": "*7197", "Сумма операции": 100},  # Пополнение
        {"Номер карты": "*4556", "Сумма операции": -500},  # Отрицательная сумма
    ]

    result = get_card_stats(transactions)

    assert len(result) == 2  # Только *7197 и *4556

    card_7197 = next(card for card in result if card["last_digits"] == "7197")
    assert card_7197["total_spent"] == 87
    assert card_7197["cashback"] == pytest.approx(0.87, 0.01)

    card_4556 = next(card for card in result if card["last_digits"] == "4556")
    assert card_4556["total_spent"] == 805  # 305 + 500
    assert card_4556["cashback"] == pytest.approx(8.05, 0.01)


# Тест для get_top_transactions
def test_get_top_transactions():
    """Тест получения топ-транзакций"""
    transactions = [
        # Отрицательные транзакции (расходы)
        {"Дата операции": "02.06.2019 17:46:06", "Сумма операции": -87, "Категория": "Супермаркеты",
         "Описание": "Колхоз"},
        {"Дата операции": "02.06.2019 15:33:54", "Сумма операции": -305, "Категория": "Транспорт",
         "Описание": "Яндекс Такси"},
        {"Сумма операции": -500, "Категория": "Фастфуд", "Описание": "Mouse Tail"},
        {"Сумма операции": -200, "Дата операции": "12.06.2019 10:00:00", "Категория": "Различные товары",
         "Описание": "Ozon.ru"},

        # Положительная транзакция (пополнение — игнорируется)
        {"Сумма операции": 1000}
    ]

    result = get_top_transactions(transactions)

    assert len(result) == 4  # Теперь ожидаем 4 транзакции

    # Проверяем сортировку по сумме (от наибольшей к наименьшей)
    assert result[0]["amount"] == 500
    assert result[1]["amount"] == 305
    assert result[2]["amount"] == 200
    assert result[3]["amount"] == 87

    # Проверяем поля
    assert result[0]["category"] == "Фастфуд"
    assert result[0]["description"] == "Mouse Tail"
    assert result[1]["category"] == "Транспорт"
    assert result[1]["description"] == "Яндекс Такси"
    assert result[2]["category"] == "Различные товары"
    assert result[2]["description"] == "Ozon.ru"
    assert result[3]["category"] == "Супермаркеты"
    assert result[3]["description"] == "Колхоз"


# Тест для format_currency_rates
def test_format_currency_rates():
    """Тест форматирования курсов валют"""
    rates = {"USD": 73.21, "EUR": 87.08}
    result = format_currency_rates(rates)

    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 73.21
    assert result[1]["currency"] == "EUR"
    assert result[1]["rate"] == 87.08


# Тест для format_stock_prices
def test_format_stock_prices():
    """Тест форматирования цен акций"""
    stocks = [{"AAPL": "150.12", "AMZN": "3173.18"}]
    result = format_stock_prices(stocks)

    assert len(result) == 2
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 150.12
    assert result[1]["stock"] == "AMZN"
    assert result[1]["price"] == 3173.18
