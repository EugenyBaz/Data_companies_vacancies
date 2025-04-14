from configparser import ConfigParser


def config(filename="../database.ini", section="postgresql"):
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
    db = {}
    params = parser.items(section)
    for param in params:
        db[param[0]] = param[1]

    return db