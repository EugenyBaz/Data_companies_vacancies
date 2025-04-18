from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class AbstractApi(ABC):
    """Абстрактный класс"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_companies(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def _connect_to_api(self, url, params) -> requests.Response:
        pass


class HeadHunterAPI(AbstractApi):
    """Класс работы с API"""

    def __init__(self) -> None:
        """Инициализация атрибутов"""
        self.__url = "https://api.hh.ru/vacancies?employer_id={}"
        self.__url_empl = "https://api.hh.ru/employers/{}"
        self.__params = {"page": 0, "per_page": 50}

        self.__vacancies = []
        self.__companies = []
        self.__employer_ids = [78638, 3529, 1740, 3776, 4496, 3127, 2748, 907345, 49357, 1054705]

    def get_companies(self) -> List[Dict[str, Any]]:
        """Метод получения данных о компаниях"""
        for employer_id in self.__employer_ids:
            response = self._connect_to_api(self.__url_empl.format(employer_id), self.__params)
            if response.status_code == 200:
                company_data = response.json()
                self.__companies.append(company_data)
            else:
                raise ValueError("Ошибка запроса запрос. Статус !=200")
        return self.__companies

    def get_vacancies(self) -> List[Dict[str, Any]]:
        """Метод получения вакансии у выбранных компаний"""
        for employer_id in self.__employer_ids:
            response = self._connect_to_api(self.__url.format(employer_id), self.__params)
            if response.status_code != 200:
                break
            data = response.json()
            items = data.get("items", [])
            self.__vacancies.extend(items)
        return self.__vacancies

        #     page = 0
        #     while True:
        #         self.__params['page'] = page
        #         response = self._connect_to_api(self.__url.format(employer_id), self.__params)
        #         if response.status_code != 200:
        #             break
        #         data = response.json()
        #         items = data.get('items',[])
        #         self.__vacancies.extend(items)
        #         has_more_pages = data.get('has_more_pages', False)  # Проверяем, есть ли следующие страницы
        #         if not has_more_pages or page > 50:
        #             break
        #         page +=1
        # return self.__vacancies

    @property
    def vacancies(self) -> List[Dict[str, Any]]:
        return self.__vacancies

    @property
    def companies(self) -> List[Dict[str, Any]]:
        return self.__companies

    def _connect_to_api(self, url, params) -> requests.Response:
        """Метод для выполнения запроса"""
        response = requests.get(url, params=params)
        return response


hh_api = HeadHunterAPI()
# companies = hh_api.get_companies()
# print(companies)

vacancies = hh_api.get_vacancies()

print(vacancies)
print(len(hh_api.vacancies))
