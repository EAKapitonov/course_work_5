import psycopg2
import os
from abs_class.abs_class_dbmanager import AbsDBManager

password_bd: str = os.getenv('password_bd')


class DBManager(AbsDBManager):
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT employer_name, COUNT(vacancies.employer_id) AS count_vac FROM employers
                INNER JOIN vacancies USING(employer_id)
                GROUP BY employer_name
                ORDER BY COUNT(*) DESC""")
                rows = cur.fetchall()
        conn.close()
        return rows

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию """
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT employers.employer_name, vacancies_name, salary, vacancies_url FROM vacancies
                INNER JOIN employers USING(employer_id)""")
                rows = cur.fetchall()
        conn.close()
        return rows

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT ROUND(AVG(salary)) FROM vacancies WHERE salary > 0""")
                rows = cur.fetchall()
        conn.close()
        return rows[0][0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM vacancies
                WHERE salary > (SELECT ROUND(AVG(salary)) FROM vacancies WHERE salary > 0)""")
                rows = cur.fetchall()
        conn.close()
        return rows

    def get_vacancies_with_keyword(self, text):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT *
                FROM vacancies
                WHERE vacancies_name LIKE '%{text}%'""")
                rows = cur.fetchall()
        conn.close()
        return rows

i = DBManager()
i.get_avg_salary()
