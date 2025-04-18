from src.DBManager import DBManager


if __name__ == "__main__":
    print ("""                                   Привет! 
    Предлагаю выбрать интересующие параметры по обзору и поиску вакансии:""")
    while True:
        search_query = input("""
    Введи - 1 для просмотра выбранных мной компаний :-) и количество вакансий у каждой компании;
    Введи - 2 для просмотра  вакансий с названием компании, вакансии, зарплаты и ссылки;
    Введи - 3 для ознакомления со средней зарплатой по вакансиям;
    Введи - 4 для просмотра вакансий, у которых зарплата выше средней по всем вакансиям;
    Ну или Введи - 5 для поиска вакансии по твоему ключевому слову: \n """).strip()


        while True:

            if search_query == "1":
                db_manager = DBManager()
                result = db_manager.get_companies_and_vacancies_count()
                if result:
                    for company_name, vacancy_count in result:
                        print(f'{company_name}: {vacancy_count} вакансии')

                else:
                    print('Нет данных.')
                break
            elif search_query == "2":
                db_manager = DBManager()
                result = db_manager.get_all_vacancies()

                if result:
                    for name, name_vacancy, salary_from, salary_to, alternate_url in result:
                        print(f'Компания: {name}, Вакансия: {name_vacancy},'
                              f' Заработная плата от {salary_from} до {salary_to},'
                              f' ссылка на вакансию {alternate_url}')
                else:
                    print('Нет данных.')

                break

            elif search_query == "3":
                db_manager = DBManager()
                result = db_manager.get_avg_salary()
                print (f' Средняя зарплата по вакансиям составляет: {result} руб.')
                break

            elif search_query == "4":
                db_manager = DBManager()
                result = db_manager.get_vacancies_with_higher_salary()
                for row in result:
                    print(f'{row[0]}, {row[1]}, заработная плата от {row[2]} до {row[3]}, ссылка: {row[4]}')
                break

            elif search_query == "5":
                db_manager = DBManager()
                result = db_manager.get_vacancies_with_keyword()
                for row in result:
                    print(f'{row[0]}, {row[1]}, заработная плата от {row[2]} до {row[3]}, ссылка: {row[4]}')

                break

            else:
                print("Ошибка ввода! Пожалуйста, введите значение от 1 до 5.")
                break






