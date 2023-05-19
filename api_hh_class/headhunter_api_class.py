import sys
import json
import requests
import psycopg2
import os
from abs_class.abs_class_api import AbsHeadHunter

password_bd: str = os.getenv('password_bd')


class HeadHunter(AbsHeadHunter):
    """
    Класс для работы с API HH
    """

    def __init__(self, name: str, parent_area_employer: int = 113, ):
        """
        Инициализация объекта класса параметрами поиска работодателя
        """
        self.name = name  # Текст поиска вакансии
        self.parent_area_employer = parent_area_employer  # Код страны поиска, по умолчанию Россия
        self.employer_id = None  # id работодателя
        self.employer = {}
        self.employer_vacancy = []

    def research_employer_from_api(self):
        """
        Метод получения данных через API по указанным параметрам
        """
        try:
            param = {'text': self.name,
                     'parent_id': self.parent_area_employer,  # Код страны.
                     'page': 1,  # Номер страницы с работодателями (считается от 0, по умолчанию — 0)
                     'per_page': 1  # Количество элементов на страницу (по умолчанию — 20, максимум — 100 )
                     }
            req = requests.get("https://api.hh.ru/employers", param)  # Посылаем запрос к API
            data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
            data_dict = json.loads(data)
            self.employer_id = "Написать"
        except ValueError:
            print("Ошибка значения, попробуйте снова")
            sys.exit()

    def import_information_about_employer(self):
        """
        Получение информации об работодателе
        """
        req = requests.get(f"https://api.hh.ru/employers/{self.employer_id}")  # Посылаем запрос к API
        data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
        self.employer = json.loads(data)

    def import_vacancy_employer_from_api(self):
        """
        Получает данные с вакансиями по employer_id
        """
        param_ = {'employer_id': employer_id,  # Идентификатор работодателя. Можно указать несколько значений
                  'page': page,  # Номер страницы с работодателями (считается от 0, по умолчанию — 0)
                  'per_page': 1  # Количество элементов на страницу (по умолчанию — 20, максимум — 100 )
                  }
        req = requests.get("https://api.hh.ru/vacancies", param_)  # Посылаем запрос к API
        data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
        vac = json.loads(data)
        self.employer_vacancy.append(vac['items'])


    def response_format(self):
        """
        Форматирования ответа сервера
        """
        for i in range(0, len(self.employer_vacancy)):
            items = {}
            items["name"] = self.employer_vacancy[i]["name"]
            items["url"] = self.employer_vacancy[i]["alternate_url"]
            if isinstance(self.employer_vacancy[i]["salary"], dict):
                if isinstance(self.employer_vacancy[i]["salary"]["from"], int):
                    items["salary"] = self.employer_vacancy[i]["salary"]["from"]
                else:
                    items["salary"] = 0
            else:
                continue
            items["id_vacancy"] = self.employer_vacancy[i]["id"]
            if "employer" in self.employer_vacancy[i]:
                items["employer"] = self.employer_vacancy[i]["employer"]["name"]  # сохранение имени работодателя
                items["employer_url"] = self.employer_vacancy[i]["employer"][
                    "alternate_url"]  # сохранение ссылки на карточку работодателя
            else:
                items["employer"] = "нет данных"  # сохранение имени работодателя
                items["employer_url"] = "нет данных"  # сохранение ссылки на карточку работодателя
            items["requirement"] = self.employer_vacancy[i]['snippet']['requirement']  # сохранение требований к вакансии
            items["responsibility"] = self.employer_vacancy[i]['snippet'][
                'responsibility']  # сохранение обязанностей вакансии
            self.data_from_vacancy.append(items)

    def get_to_vacancy(self):
        """
        Метод добавляет в базу данных вакансии работодателей
        """
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                for i in reader:
                    cur.execute("INSERT INTO customers_name VALUES (%s, %s, %s, %s, %s, %s)",
                                (i["customer_id"], i["company_name"], i["contact_name"]))
        conn.close()

    def get_to_employer(self):
        """
        Метод добавляет работодателя в базу данных
        """
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                for i in reader:
                    cur.execute("INSERT INTO customers_name VALUES (%s, %s, %s, %s, %s, %s)",
                                (i["customer_id"], i["company_name"], i["contact_name"]))
        conn.close()
