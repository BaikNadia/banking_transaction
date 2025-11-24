from unittest.mock import patch, MagicMock

import pandas as pd

import src.utils as utils


# Тест для load_transactions
@patch('src.utils.pd.read_excel')
def test_load_transactions_success(mock_read_excel):
    """Тест успешной загрузки транзакций"""
    mock_df = pd.DataFrame([
        {
            "Дата операции": "02.06.2019 17:46:06",
            "Сумма операции": -87,
            "Категория": "Супермаркеты"
        }
    ])
    mock_read_excel.return_value = mock_df
    result = utils.load_transactions()
    assert len(result) == 1
    assert result[0]["Категория"] == "Супермаркеты"


def test_load_transactions_file_not_found():
    """Тест отсутствия файла"""
    result = utils.load_transactions("data/nonexistent.xlsx")
    assert result == []


@patch('src.utils.pd.read_excel')
def test_load_transactions_invalid_format(mock_read_excel):
    """Тест ошибки чтения Excel"""
    mock_read_excel.side_effect = Exception("Invalid format")
    result = utils.load_transactions()
    assert result == []


# Тест для get_exchange_rates
@patch('src.utils.requests.get')
def test_get_exchange_rates_success(mock_get):
    """Тест успешного получения курсов валют"""
    mock_response = {"conversion_rates": {"USD": 1, "EUR": 0.9}}
    mock_get.return_value = MagicMock(json=lambda: mock_response)
    result = utils.get_exchange_rates()
    assert "USD" in result
    assert "EUR" in result


@patch('src.utils.requests.get')
def test_get_exchange_rates_api_error(mock_get):
    """Тест ошибки API при получении курсов валют"""
    mock_get.side_effect = Exception("API Error")
    result = utils.get_exchange_rates()
    assert result == {}


@patch('src.utils.requests.get')
def test_get_exchange_rates_missing_key(mock_get):
    """Тест отсутствия ключа API"""
    mock_get.return_value = {}
    # with patch.dict('os.environ', {"EXCHANGE_RATE_API_KEY": ""}):
    result = utils.get_exchange_rates()
    assert result == {}


# Тест для get_sp500_data
@patch('src.utils.requests.get')
def test_get_sp500_data_success(mock_get):
    """Тест успешного получения данных S&P 500"""
    # Настройка возвращаемого значения для mock_get
    mock_response = {
        "Time Series Daily Adjusted": {
            "2023-01-01": {"1. open": "300"},
            "2023-01-02": {"1. open": "305"},
        }
    }

    # Привязка метода json() к mock_get
    mock_get.return_value.json.return_value = mock_response

    result = utils.get_sp500_data()
    assert len(result) == 2
    assert result[0]["1. open"] == "300"


@patch('src.utils.requests.get')
def test_get_sp500_data_api_error(mock_get):
    """Тест ошибки API при получении данных S&P 500"""
    mock_get.side_effect = Exception("API Error")
    result = utils.get_sp500_data()
    assert result == []


@patch('src.utils.requests.get')
def test_get_sp500_data_empty_response(mock_get):
    """Тест пустого ответа от API S&P 500"""
    mock_get.return_value = MagicMock(json=lambda: {})
    result = utils.get_sp500_data()
    assert result == []

# # Параметризованные тесты
# @pytest.mark.parametrize("file_path,expected_result", [
#     ("data/operations.xlsx", 1),
#     ("data/nonexistent.xlsx", 0),
# ])
# @patch('src.utils.pd.read_excel')
# def test_load_transactions_parametrized(mock_read_excel, file_path, expected_result):
#     """Параметризованный тест загрузки транзакций"""
#     if "nonexistent" in file_path:
#         result = utils.load_transactions(file_path)
#         assert result == []
#     else:
#         mock_df = pd.DataFrame([
#             {
#                 "Дата операции": "02.06.2019 17:46:06",
#                 "Сумма операции": -87,
#                 "Категория": "Супермаркеты"
#             }
#         ])
#         mock_read_excel.return_value = mock_df
#         result = utils.load_transactions(file_path)
#         assert len(result) == 1
#         assert result[0]["Категория"] == "Супермаркеты"
