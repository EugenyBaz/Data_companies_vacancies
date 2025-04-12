from unittest.mock import MagicMock, patch

import pytest

from src.headhunter_api import HeadHunterAPI


@pytest.fixture
def mock_requests():
    """
    Фикстура для подмены модуля requests
    """
    with patch("src.headhunter_api.requests", autospec=True) as mock:
        yield mock


def test_get_vacancies(mock_requests):
    # Создаем фиктивный ответ от API
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "items": [{"id": 1, "name": "Тестовая вакансия"}, {"id": 2, "name": "Другая тестовая вакансия"}]
    }

    # Настраиваем mock, чтобы вернуть фиктивный ответ
    mock_requests.get.return_value = fake_response

    # Создаем экземпляр класса HeadHunterAPI
    hh_api = HeadHunterAPI()

    # Вызываем метод get_vacancies с ключевым словом
    vacancies = hh_api.get_vacancies(keyword="test")

    # Проверяем, что возвращено два элемента
    assert len(vacancies) == 2
    assert {"id": 1, "name": "Тестовая вакансия"} in vacancies
    assert {"id": 2, "name": "Другая тестовая вакансия"} in vacancies
