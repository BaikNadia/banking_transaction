from src.utils import read_excel_file
import os

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "operations.xlsx"
    file_path = os.path.join(current_dir, "..", "data", file_name)

    # Чтение данных из Excel-файла
    df = read_excel_file(file_name)

    # Проверка, что DataFrame не пустой
    if df.empty:
        print("Файл пуст или данные не были прочитаны.")
    else:
        print("Первые 5 строк файла:")
        print(df.head())