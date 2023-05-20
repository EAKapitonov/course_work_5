from abs_class.abs_class_dbmanager import AbsDBManager


class DBManager(AbsDBManager):
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        pass

    SELECT employer_name, COUNT(vacancies.employer_id) FROM employers
    INNER JOIN vacancies USING(employer_id)
    GROUP BY employer_name
    ORDER BY COUNT(*) DESC

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию """
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        pass
