import os
import json

from src.file_saver import JSONSaver, JSONSaver_company
from src.headhunter_api import HeadHunterAPI


current_dir = os.path.dirname((os.path.abspath(__file__)))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path = os.path.join(project_root, "data", "vacancy_data.json")
data_file_company = os.path.join(project_root, "data", "company_data.json")


def create_data_companies():
    """Создание файла компаний в формате  json"""

    hh_api = HeadHunterAPI()
    data_comp = hh_api.get_companies()

    for company in data_comp:
        del company['branded_description']

    with open(data_file_company, "w", encoding="utf-8") as file:
        json.dump(data_comp, file, indent=4, ensure_ascii=False)

create_data_companies()

def create_data_vacancies():
    """Создание файла вакансий в формате  json"""

    hh_api = HeadHunterAPI()
    data_vacancies = hh_api.get_vacancies()

    # for vac in data_vacancies:
    #     del company['branded_description']

    with open(data_file_path, "w", encoding="utf-8") as file:
        json.dump(data_vacancies, file, indent=4, ensure_ascii=False)

create_data_vacancies()