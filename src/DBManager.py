import psycopg2
from config import config




class DBManager():

    def __init__(self):

        self.__params = config()
        self.__conn = psycopg2.connect(**self.__params)
        self.__cur = self.__conn.cursor()


    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            self.__cur.execute ("""
            SELECT companies.name, COUNT(vacancies.id_vacancy) as count_vac
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.employer_id
            GROUP BY companies.name
            """)
            return self.__cur.fetchall()

        except Exception as e:
            print(f'Ошибка при выполнении запроса {e}')

    def close_connection(self):
        # Закрываем курсор и соединение
        if self.__cur is not None:
            self.__cur.close()
        if self.__conn is not None:
            self.__conn.close()


db_manager = DBManager()
result = db_manager.get_companies_and_vacancies_count()
if result:
    for company_name, vacancy_count in result:
        print(f'{company_name}: {vacancy_count} вакансии')
else:
    print('Нет данных.')





    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass