import os
import sys
from io import StringIO
from unittest.mock import patch

import pytest

# Убедитесь что путь корректен
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.views import main_views


@pytest.fixture
def sample_transactions():
    return [{
        "Дата операции": "01.01.2023 12:00:00",
        "Сумма": "100",
        "Валюта": "USD",
        "Категория": "Еда",
        "Описание": "Обед"
    }]


def test_main_views(sample_transactions):
    with patch('src.views.utils.load_transactions') as mock_load, \
            patch('src.views.utils.get_exchange_rates') as mock_rates, \
            patch('src.views.utils.get_sp500_data') as mock_sp500, \
            patch('src.views.services.search_transactions') as mock_search, \
            patch('src.views.reports.spending_by_weekday') as mock_report, \
            patch('builtins.input', side_effect=["2023-01-02 00:00:00", "", ""]), \
            patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        mock_load.return_value = sample_transactions
        mock_rates.return_value = {"USD": 1.0}
        mock_sp500.return_value = {}
        mock_search.return_value = []
        mock_report.return_value = {}

        main_views()

        output = mock_stdout.getvalue()
        assert "=== Загрузка транзакций из Excel-файла ===" in output
