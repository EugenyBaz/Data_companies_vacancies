import pytest

from src.vacancy_handler import VacancyHandler

# Тесты для инициализации и валидаторов


def test_valid_init(vacancy_list):

    assert vacancy_list.name == "Test Job"
    assert vacancy_list.vacancies_url == "http://example.com/job"
    assert vacancy_list.salary == " от 50000 до 80000"
    assert vacancy_list.requirement == "Requirements here"


def test_empty_string_values(vacancy_list_invalid_name):
    with pytest.raises(ValueError):
        VacancyHandler(**vacancy_list_invalid_name)


def test_empty_string_values_url(vacancy_list_invalid_url):
    with pytest.raises(ValueError):
        VacancyHandler(**vacancy_list_invalid_url)


def test_invalid_types_name(vacancy_list_invalid_name_type):
    with pytest.raises(ValueError):
        VacancyHandler(**vacancy_list_invalid_name_type)


def test_invalid_types_url(vacancy_list_invalid_url_type):
    with pytest.raises(ValueError):
        VacancyHandler(**vacancy_list_invalid_url_type)


def test_non_dict_salary(vacancy_list_invalid_salary):
    with pytest.raises(ValueError):
        VacancyHandler(**vacancy_list_invalid_salary)


def test_salary_formats(vacancy_list_salary):
    assert float(vacancy_list_salary.salary) == 50000.00


def test_empty_requirements(vacancy_list_emp_req):
    assert vacancy_list_emp_req.requirement == ""


def extract_salary_int(salary_str):
    parts = salary_str.split()
    numbers = []

    for part in parts:
        try:
            number = int(part)  # Пробуем преобразовать слово в целое число
            numbers.append(number)
        except ValueError:
            pass
    return tuple(numbers[:2])


def test_gt_salary_comparison(vacancy_list_comp1, vacancy_list_comp2):

    vac1_min, vac1_max = extract_salary_int(vacancy_list_comp1.salary)
    vac2_min, vac2_max = extract_salary_int(vacancy_list_comp2.salary)
    assert vac2_max > vac1_max
