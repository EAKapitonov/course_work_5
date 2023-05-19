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
                     'page': 0,  # Номер страницы с работодателями (считается от 0, по умолчанию — 0)
                     'per_page': 1  # Количество элементов на страницу (по умолчанию — 20, максимум — 100 )
                     }
            req = requests.get("https://api.hh.ru/employers", param)  # Посылаем запрос к API
            data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
            data_dict = json.loads(data)
            self.employer_id = data_dict['items'][0]["id"]
        except ValueError:
            print("Ошибка значения, попробуйте снова")
            sys.exit()

    def import_information_about_employer(self):
        """
        Получение информации об работодателе
        """
        req = requests.get(f"https://api.hh.ru/employers/{self.employer_id}")  # Посылаем запрос к API
        data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
        data_dict = json.loads(data)
        employer = {}
        employer['employer_id'] = self.employer_id
        employer['name'] = data_dict['name']
        employer['url'] = data_dict['alternate_url']
        employer['description'] = data_dict['description']
        self.employer = employer

    def import_vacancy_employer_from_api(self):
        """
        Получает данные с вакансиями по employer_id
        """
        param_ = {'employer_id': self.employer_id,  # Идентификатор работодателя. Можно указать несколько значений
                  'page': 0,  # Номер страницы с работодателями (считается от 0, по умолчанию — 0)
                  'per_page': 100  # Количество элементов на страницу (по умолчанию — 20, максимум — 100 )
                  }
        req = requests.get("https://api.hh.ru/vacancies", param_)  # Посылаем запрос к API
        data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
        vacancy = json.loads(data)
        for i in range(0, len(vacancy)):
            items = {}
            items["employer_id"] = self.employer_id
            items["name"] = vacancy['items'][i]["name"]
            items["url"] = vacancy['items'][i]["alternate_url"]
            if isinstance(vacancy['items'][i]["salary"], dict):
                if isinstance(vacancy['items'][i]["salary"]["from"], int):
                    items["salary"] = vacancy['items'][i]["salary"]["from"]
                else:
                    items["salary"] = 0
            else:
                continue
            items["id_vacancy"] = vacancy['items'][i]["id"]
            items["requirement"] = vacancy['items'][i]['snippet'][
                'requirement']  # сохранение требований к вакансии
            items["responsibility"] = vacancy['items'][i]['snippet'][
                'responsibility']  # сохранение обязанностей вакансии
            self.employer_vacancy.append(items)

    def get_to_vacancy(self):
        """
        Метод добавляет в базу данных вакансии работодателей
        """
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                for i in self.employer_vacancy:
                    cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (i["employer_id"], i["id_vacancy"], i["name"], i["url"], i["salary"], i["requirement"],
                                 i["responsibility"]))
        conn.close()

    def get_to_employer(self):
        """
        Метод добавляет работодателя в базу данных
        """
        with psycopg2.connect(host="localhost", database="headhunter", user="postgres", password=password_bd) as conn:
            with conn.cursor() as cur:
                i = self.employer
                cur.execute("INSERT INTO employers VALUES (%s, %s, %s, %s)",
                            (i['employer_id'], i["name"], i['url'], i['description']))
        conn.close()
