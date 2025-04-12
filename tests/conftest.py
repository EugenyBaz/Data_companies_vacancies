import pytest

from src.vacancy_handler import VacancyHandler


@pytest.fixture
def vacancy_list():
    return VacancyHandler("Test Job", "http://example.com/job", {"from": 50000, "to": 80000}, "Requirements here")


@pytest.fixture
def vacancy_list_invalid_name():
    return {
        "name": "",
        "vacancies_url": "http://example.com/job",
        "salary": {"from": 50000, "to": 80000},
        "requirement": "Requirements here",
    }


@pytest.fixture
def vacancy_list_invalid_url():
    return {
        "name": "Test Job",
        "vacancies_url": "",
        "salary": {"from": 50000, "to": 80000},
        "requirement": "Requirements here",
    }


@pytest.fixture
def vacancy_list_invalid_name_type():
    return {
        "name": 123,
        "vacancies_url": "http://example.com/job",
        "salary": {"from": 50000, "to": 80000},
        "requirement": "Requirements here",
    }


@pytest.fixture
def vacancy_list_invalid_url_type():
    return {
        "name": "Test Job",
        "vacancies_url": 123,
        "salary": {"from": 50000, "to": 80000},
        "requirement": "Requirements here",
    }


@pytest.fixture
def vacancy_list_invalid_salary():
    return {
        "name": "Test Job",
        "vacancies_url": "http://example.com/job",
        "salary": {"Nothing"},
        "requirement": "Requirements here",
    }


@pytest.fixture
def vacancy_list_salary():
    return VacancyHandler("Test Job", "http://example.com/job", 50000, "Requirements here")


@pytest.fixture
def vacancy_list_emp_req():
    return VacancyHandler("Test Job", "http://example.com/job", 50000, "")


@pytest.fixture
def vacancy_list_comp1():
    return VacancyHandler("Test Job", "http://example.com/job", {"from": 50000, "to": 80000}, "Requirements here")


@pytest.fixture
def vacancy_list_comp2():
    return VacancyHandler("Test Job", "http://example.com/job", {"from": 100000, "to": 180000}, "Requirements here")
