import os
from typing import List, Any
import psycopg2
import json
from config import config

current_dir = os.path.dirname((os.path.abspath(__file__)))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path = os.path.join(project_root, "data", "vacancy_data.json")
data_file_company = os.path.join(project_root, "data", "company_data.json")


def read_json(file_path) -> Any:
    with open(file_path, 'r') as file:
        return json.load(file)


params = config()
conn = psycopg2.connect(**params)

cur = conn.cursor()

# Удаляем таблицу компаний перед вставкой
cur.execute("DROP TABLE IF EXISTS companies CASCADE;")

# Удаляем таблицу вакансий перед вставкой
cur.execute("DROP TABLE IF EXISTS vacancies CASCADE;")

# Создаем таблицу компаний
cur.execute("""
CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    area VARCHAR(255),
    industries TEXT,
    open_vacancies INT,
    site_url VARCHAR(255)
);
""")

# Создаем таблицу вакансий
cur.execute("""
CREATE TABLE vacancies (
    id_vacancy VARCHAR(20)PRIMARY KEY,
    name_vacancy VARCHAR(255),
    area_name VARCHAR(255),
    salary_from DECIMAL,
    salary_to DECIMAL,
    salary_cur VARCHAR(10),
    employer_id INT REFERENCES companies(id),
    employer_url VARCHAR(255),
    snippet_requirement TEXT,
    snippet_responsibility TEXT,
    schedule_name VARCHAR(255),
    professional_roles_name TEXT,
    experience_name VARCHAR(255),
    alternate_url VARCHAR(255)
);
""")
# Чтение данных из JSON-файлов
companies_data = read_json(data_file_company)
vacancies_data = read_json(data_file_path)

def convert_list_to_string(lst) -> str:
    """Конвертирует список в строку"""
    return ', '.join([item.get('name', '') for item in lst])


def insert_companies(cursor, data : List[dict]) -> None:
    for company in data:
        area_name = company['area'].get('name') if company.get('area') else None
        industries_str = convert_list_to_string(company.get('industries', [])) or ''
        cursor.execute(
            "INSERT INTO public.companies (id, name, area, industries, open_vacancies, site_url)"
            " VALUES (%s, %s, %s, %s, %s, %s)",
            (company['id'], company['name'], area_name,
             industries_str, company['open_vacancies'], company['site_url']))


# Функция для вставки данных о вакансиях
def insert_vacancies(cursor, data: List[dict]) -> None:
        for vacancy in data:
                area_name = vacancy['area'].get('name') if vacancy.get('area') else None
                salary_from = vacancy['salary'].get('from') if vacancy.get('salary') else None
                salary_to = vacancy['salary'].get('to') if vacancy.get('salary') else None
                salary_cur = vacancy['salary'].get('currency') if vacancy.get('salary') else None
                prof_roles = convert_list_to_string(vacancy.get('professional_roles', [])) or ''

                cursor.execute(
                """
                INSERT INTO public.vacancies (id_vacancy, name_vacancy, area_name,
                salary_from, salary_to,salary_cur, employer_id, employer_url, snippet_requirement,
                snippet_responsibility, schedule_name, professional_roles_name,
                experience_name, alternate_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id'], vacancy['name'],area_name, salary_from,
                 salary_to, salary_cur, vacancy['employer'].get('id'), vacancy['employer'].get('alternate_url'),
                 vacancy['snippet'].get('requirement'), vacancy['snippet'].get('responsibility'),
                 vacancy['schedule'].get('name'), prof_roles, vacancy['experience'].get('name'),
                 vacancy['alternate_url'])
        )


# Выполняем вставку данных
try:
    with conn:
        insert_companies(cur, companies_data)
        insert_vacancies(cur, vacancies_data)

    print("Данные успешно загружены!")
except Exception as e:
    print(f"Произошла ошибка при вставке данных: {e}")
finally:
    # Всегда закрываем соединение после завершения работы
    if conn:
        cur.close()
        conn.close()

