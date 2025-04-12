class VacancyHandler:
    """Создаем класс для инициализации и валидации параметров вакансии"""

    __slots__ = ("name", "vacancies_url", "salary", "requirement")

    def __init__(self, name, vacancies_url, salary=None, requirement=None):
        """Метод инициализации атрибутов"""
        self.name = self._validate_name(name)
        self.vacancies_url = self._validate_vacancies_url(vacancies_url)
        self.salary = self._validate_salary(salary)
        self.requirement = self._validate_requirement(requirement or "")

    def _validate_name(self, name):
        """Метод валидации name"""
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Название вакансии должно быть непустым строковым значением.")
        return name.strip()

    def _validate_vacancies_url(self, vacancies_url):
        """Метод валидации url"""
        if not isinstance(vacancies_url, str) or len(vacancies_url.strip()) == 0:
            raise ValueError("Ссылка должна быть не пустой строкой.")
        return vacancies_url.strip()

    def _validate_salary(self, salary):
        """Метод валидации зарплаты"""
        if salary is None:
            return "Зарплата не указана"
        elif isinstance(salary, (int, float)):
            return f"{salary:.2f}"
        elif isinstance(salary, str):
            return f"{float(salary):.2f}"
        elif isinstance(salary, dict):
            salary_value_from = salary.get("from")
            salary_value_to = salary.get("to")
            return f" от {salary_value_from} до {salary_value_to}"
        else:
            raise ValueError("Заработная плата должна быть числом или пустой строкой.")

    def _validate_requirement(self, requirement):
        """Метод валидации требований"""
        if not isinstance(requirement, str):
            raise ValueError("Требования  должны быть строкой.")
        return requirement.strip() if requirement else ""

    def __gt__(self, other):
        """Метод для сравнений вакансий по зарплате."""

        if self.salary == "Зарплата не указана" or other.salary == "Зарплата не указана":
            return False
        try:
            my_salary = float(self.salary.replace(",", ".")) if "," in self.salary else float(self.salary)
            other_salary = float(other.salary.replace(",", ".")) if "," in other.salary else float(other.salary)
            return my_salary > other_salary
        except ValueError as e:
            print(f"Произошла ошибка при сравнении зарплат: {e}. Пропускаем сравнение.")
            return False
