import pandas as pd
import pytest


@pytest.fixture
def mock_excel_data():
    data = {
        "Дата операции": ["2023-10-05 12:00:00", "2023-10-06 14:00:00"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-100, -200],
        "Категория": ["Фастфуд", "Супермаркеты"],
        "Описание": ["Kofe Lesnaya 24", "SPAR"]
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    return df

