import os
from typing import Dict
from configparser import ConfigParser

current_dir = os.path.dirname((os.path.abspath(__file__)))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file = os.path.join(project_root, "database.ini")


def config(filename=data_file, section="postgresql") -> Dict [str, str]:
    # Создаем парсер
    parser = ConfigParser()

    # Читаем файл конфигурации
    try:
        parser.read(filename)
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла {filename}: {e}")

    # Проверяем наличие раздела
    if not parser.has_section(section):
        raise Exception(f'Раздел {section} не найден в файле {filename}')

    # Получаем параметры
    db: Dict [str,str] = {}
    params = parser.items(section)
    for param in params:
        db[param[0]] = param[1]

    return db