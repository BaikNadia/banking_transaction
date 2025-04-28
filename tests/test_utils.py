from unittest.mock import patch

import pandas as pd

from src.utils import read_excel_file


@patch("src.utils.pd.read_excel")
def test_read_excel_file(mock_read_excel):
    """
    Тестирует функцию чтения Excel-файла.
    """
    mock_data = pd.DataFrame({
        "Дата операции": ["2023-10-05 12:00:00", "2023-10-06 14:00:00"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-100, -200],
        "Категория": ["Фастфуд", "Супермаркеты"],
        "Описание": ["Kofe Lesnaya 24", "SPAR"]
    })

    mock_read_excel.return_value = mock_data

    result = read_excel_file("mock_path.xlsx")
    assert not result.empty
    assert len(result) == 2
    assert "Дата операции" in result.columns
    assert "Статус" in result.columns
    assert "Сумма операции" in result.columns
    assert "Категория" in result.columns
    assert "Описание" in result.columns
