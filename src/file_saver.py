import json
import os
from abc import ABC, abstractmethod

current_dir = os.path.dirname((os.path.abspath(__file__)))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path = os.path.join(project_root, "data", "vacancy_data.json")


class SAVER(ABC):
    """Определяем абстрактный класс"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancy_factor(self, factor):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass


class JSONSaver(SAVER):
    """Определяем класс для работы с файлами"""

    def __init__(self, filename=data_file_path):
        """Метод инициализации атрибутов класса"""
        self.__filename = filename
        self.data = []
        self.load = ()

    def load_data(self):
        """Метод чтения и загрузки файла в data"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.save_data()

    def save_data(self):
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
                return

        # Обновляем существующие данные
        for vacancy in self.data:
            found = False
            for existing_vacancy in existing_data:
                if existing_vacancy["id"] == vacancy["id"]:
                    existing_vacancy.update(vacancy)
                    found = True
                    break
            if not found:
                existing_data.append(vacancy)

        # Сохраняем обновленные данные
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        """Метод добавления вакансии"""
        vacancy_id = vacancy.get("id")
        if vacancy_id not in [v["id"] for v in self.data]:
            self.data.append(vacancy)

        else:
            print(f"Вакансия с id={vacancy_id} уже существует.")

    def get_vacancy_currency(self, factor, vacancies=None):
        """Метод определения необходимой валюты"""
        results = []

        if vacancies is None:
            vacancies = self.data
        for vacancy in vacancies:
            if vacancy.get("salary") and vacancy["salary"].get("currency") == factor:
                results.append(vacancy)

        return results

    def get_vacancy_factor(self, factor_user, vacancies=None):
        """Поиск вакансии по параметру"""
        results = []

        if vacancies is None:
            vacancies = self.data

        for vacancy in vacancies:
            if factor_user is not None:
                for field in ["name", "area", "snippet", "requirement", "responsibility"]:
                    if field in vacancy and factor_user in str(vacancy[field]):
                        results.append(vacancy)

                        break

        return results

    def delete_vacancy(self, vacancy_id):
        """Удаление вакансии"""

        vacancy_to_delete = next((vacancy for vacancy in self.data if vacancy["id"] == vacancy_id), None)

        if vacancy_to_delete:
            # Удаляем вакансию из списка
            self.data.remove(vacancy_to_delete)
            self.save_data()
        else:
            print(f"Вакансия с id={vacancy_id} не найдена.")
