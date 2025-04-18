import psycopg2
from src.config import config




class DBManager():

    def __init__(self):

        self.__params = config()
        self.__conn = psycopg2.connect(**self.__params)
        self.__cur = self.__conn.cursor()
        self.__conn.commit()


    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            self.__cur.execute ("""
            SELECT companies.name, COUNT(vacancies.id_vacancy) as count_vac
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.employer_id
            GROUP BY companies.name
            ORDER BY companies.name ASC
            """)
            return self.__cur.fetchall()

        except Exception as e:
            print(f'Ошибка при выполнении запроса {e}')




    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        try:
            self.__cur.execute("""
                    SELECT companies.name, vacancies.name_vacancy, vacancies.salary_from,
                      vacancies.salary_to, vacancies.alternate_url
                    FROM companies
                    LEFT JOIN vacancies ON companies.id = vacancies.employer_id
                    ORDER BY companies.name ASC;
                    """)
            return self.__cur.fetchall()

        except Exception as e:
            print(f'Ошибка при выполнении запроса {e}')




    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        try:
            self.__cur.execute("""
                    SELECT
                        AVG((vacancies.salary_from + vacancies.salary_to)/ 2) as avr_salary 
                        FROM vacancies
                        WHERE salary_cur = 'RUR';
                    
                    """)
            res = self.__cur.fetchone()
            if res is not None:
                return round(float(res[0]),2)

            else:
                return "Нет данных для расчета средней зарплаты."

        except Exception as e:
            print(f'Ошибка при выполнении запроса {e}')



    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        try:
            avg_salary = self.get_avg_salary()

            self.__cur.execute("""
                    SELECT
                        companies.name, vacancies.name_vacancy, vacancies.salary_from,
                        vacancies.salary_to, vacancies.alternate_url
                        FROM vacancies
                        FULL JOIN companies ON companies.id = vacancies.employer_id
                        WHERE salary_from > %s
                        ORDER BY companies.name ASC;""", (avg_salary,))

            return self.__cur.fetchall()


        except Exception as e:
            print(f'Ошибка при выполнении запроса {e}')

    def input_keyword(self):
        return input("Введите поисковый запрос: ").lower().strip()

    def get_vacancies_with_keyword(self):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""

        try:
            keyword = self.input_keyword()

            self.__cur.execute("""
                    SELECT
                        companies.name, vacancies.name_vacancy, vacancies.salary_from,
                        vacancies.salary_to, vacancies.alternate_url
                        FROM vacancies
                        FULL JOIN companies ON companies.id = vacancies.employer_id
                        WHERE vacancies.name_vacancy ILIKE %s
                        ORDER BY companies.name ASC;""", ("%" + keyword + "%",))

            return self.__cur.fetchall()


        except Exception as e:
            print(f'Ошибка при выполнении запроса {e}')



db_manager = DBManager()
result = db_manager.get_companies_and_vacancies_count()
# if result:
#     for company_name, vacancy_count in result:
#         print(f'{company_name}: {vacancy_count} вакансии')
# else:
#     print('Нет данных.')


db_manager = DBManager()
result = db_manager.get_all_vacancies()

# if result:
#     for name, name_vacancy, salary_from, salary_to, alternate_url in result:
#         print(f'Компания: {name}, Вакансия: {name_vacancy},'
#               f' Заработная плата от {salary_from} до {salary_to},'
#               f' ссылка на вакансию {alternate_url}')
# else:
#     print('Нет данных.')



db_manager = DBManager()
result = db_manager.get_vacancies_with_higher_salary()
# for row in result:
    # print(f'{row[0]}, {row[1]}, заработная плата от {row[2]} до {row[3]}, ссылка: {row[4]}')

db_manager = DBManager()
result = db_manager.get_avg_salary()
# print (f' Средняя зарплата по вакансиям составляет: {result} руб.')

db_manager = DBManager()
# result = db_manager.get_vacancies_with_keyword()
# for row in result:
#     print(f'{row[0]}, {row[1]}, заработная плата от {row[2]} до {row[3]}, ссылка: {row[4]}')


def close_connection(self):
    # Закрываем курсор и соединение
    if self.__cur is not None:
        self.__cur.close()
    if self.__conn is not None:
        self.__conn.close()