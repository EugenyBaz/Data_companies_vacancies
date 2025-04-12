from abc import ABC, abstractmethod

import requests


class AbstractApi(ABC):
    """Абстрактный класс"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        pass

    @abstractmethod
    def _connect_to_api(self, url, params):
        pass


class HeadHunterAPI(AbstractApi):
    """Класс работы с API"""

    def __init__(self):
        """Инициализация атрибутов"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []

    def get_vacancies(self, keyword):
        """Метод получения вакансии"""
        self.__params["text"] = keyword
        while self.__params.get("page") != 1:
            response = self._connect_to_api(self.__url, self.__params)
            if response.status_code != 200:
                break
            items = response.json()["items"]
            self.__vacancies.extend(items)
            self.__params["page"] += 1
        return self.__vacancies

    @property
    def vacancies(self):
        return self.__vacancies

    def _connect_to_api(self, url, params):
        """Метод для выполнения запроса"""
        response = requests.get(url, params=params)
        return response


#
# hh_api = HeadHunterAPI()
# vacancies = hh_api.get_vacancies("менеджер")
# print(len(hh_api.vacancies))
# print(hh_api.vacancies)
