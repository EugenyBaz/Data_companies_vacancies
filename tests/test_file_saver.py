import pytest

from src.file_saver import JSONSaver

# Фиктивная вакансия
VACANCY_1 = {"id": 1, "name": "Тестовая вакансия"}
VACANCY_2 = {"id": 2, "name": "Вторая вакансия"}
VACANCY_WITH_SALARY = {"id": 3, "name": "Третья вакансия", "salary": {"currency": "RUB"}}

# Путь к временному файлу данных
TEST_DATA_FILE_PATH = "temp_test_data.json"

# Фикстуры для временных данных
# @pytest.fixture(scope="session")
# def temp_data_file():
#     """Создание временного файла данных"""
#     yield TEST_DATA_FILE_PATH
#     # Удаляем файл после завершения тестов
#     os.remove(TEST_DATA_FILE_PATH)
#
# @pytest.fixture
# def saver(temp_data_file):
#     """Создание экземпляра JSONSaver с временным файлом"""
#     return JSONSaver(filename=str(temp_data_file))


@pytest.fixture
def saver(tmp_path):
    """Создание экземпляра JSONSaver с временным файлом"""
    temp_file = tmp_path / "temp_test_data.json"
    return JSONSaver(filename=str(temp_file))


# ТЕСТЫ


def test_add_vacancy(saver):
    """Тестирование добавления вакансии"""
    saver.add_vacancy(VACANCY_1)
    saver.save_data()

    # Загружаем сохранённые данные
    saver.load_data()
    assert VACANCY_1 in saver.data


def test_delete_vacancy(saver):
    """Тестирование удаления вакансии"""
    saver.add_vacancy(VACANCY_1)
    saver.delete_vacancy(1)

    # Проверяем, что вакансия была удалена
    saver.load_data()
    assert saver.data == []


def test_load_nonexistent_file(saver):
    """Тестирование загрузки несуществующего файла"""
    saver.load_data()
    assert saver.data == []


def test_duplicate_vacancy(saver):
    """Тестирование попытки добавления дублирующей вакансии"""
    saver.add_vacancy(VACANCY_1)
    saver.add_vacancy(VACANCY_1)

    # Проверяем, что добавлена только одна вакансия
    saver.load_data()
    assert len(saver.data) == 1


def test_add_duplicate_vacancy(saver):
    """Тестирование добавления дублирующей вакансии"""
    saver.add_vacancy(VACANCY_1)
    saver.add_vacancy(VACANCY_1)

    # Проверяем, что добавлена только одна вакансия
    saver.load_data()
    assert len(saver.data) == 1


def test_delete_nonexistent_vacancy(saver):
    """Тестирование удаления несуществующей вакансии"""
    saver.delete_vacancy(999)  # несуществующий id

    # Проверяем, что ничего не было удалено
    saver.load_data()
    assert saver.data == []


def test_save_existing_data(saver):
    """Тестирование сохранения существующих данных"""
    saver.add_vacancy(VACANCY_1)
    saver.save_data()

    # Проверяем, что данные были сохранены
    saver.load_data()
    assert VACANCY_1 in saver.data


def test_add_vacancy_with_empty_salary(saver):
    """Тестирование добавления вакансии с пустой зарплатой"""
    vacancy_with_empty_salary = {"id": 4, "name": "Вакансия без зарплаты", "salary": {}}
    saver.add_vacancy(vacancy_with_empty_salary)
    saver.save_data()

    # Проверяем, что вакансия была добавлена
    saver.load_data()
    assert vacancy_with_empty_salary in saver.data


def test_get_vacancy_by_area(saver):
    """Тестирование поиска вакансии по области"""
    saver.add_vacancy({"id": 3, "name": "Вакансия в Санкт-Петербурге", "area": "Санкт-Петербург"})

    # Поиск вакансии по области "Санкт-Петербург"
    result = saver.get_vacancy_factor("Санкт-Петербург")
    assert {"id": 3, "name": "Вакансия в Санкт-Петербурге", "area": "Санкт-Петербург"} in result
