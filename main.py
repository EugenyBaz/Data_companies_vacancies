from src.interface import user_interaction


if __name__ == "__main__":
    search_query = input("Введите поисковый запрос: ").strip()
    while True:
        try:
            min_salary = float(input("Введите минимальную зарплату: "))
            break
        except ValueError:
            print("Ошибка ввода! Пожалуйста, введите числовое значение.")
    user_currency = input("Введите валюту, если рубли то введи RUR:").upper().strip()
    factor_user = input("Введите параметр").strip()
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    total_result = user_interaction(search_query, min_salary, user_currency, factor_user, top_n)
    for v in total_result:
        print(v)
