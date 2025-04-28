from datetime import datetime

import pandas as pd


def get_homepage_data(date_time_str: str, file_path: str) -> dict:
    """
    Возвращает данные для страницы «Главная» за указанную дату.

    :param date_time_str: Дата в формате YYYY-MM-DD.
    :param file_path: Путь к Excel-файлу.
    :return: JSON-ответ с данными для главной страницы.
    """
    try:
        # Чтение файла
        df = pd.read_excel(file_path)

        # Вывод названий столбцов для диагностики
        print("Названия столбцов:", df.columns.tolist())

        # Преобразование строки даты в объект datetime
        target_date = datetime.strptime(date_time_str, "%Y-%m-%d").date()

        # Проверка наличия столбца "Дата операции"
        if "Дата операции" not in df.columns:
            raise KeyError(f"Столбец 'Дата операции' отсутствует в файле {file_path}")

        # Преобразование столбца "Дата операции" в формат datetime
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S', errors='coerce')

        # Фильтрация по дате
        filtered_df = df[df['Дата операции'].dt.date == target_date]

        # Подготовка данных для JSON
        response_data = {
            "date": date_time_str,
            "transactions_count": len(filtered_df),
            "total_amount": filtered_df["Сумма операции"].sum()
        }

        return response_data

    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
        return {"error": str(e)}
