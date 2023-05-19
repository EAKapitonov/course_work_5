import sys
import json
import requests
import time


class HeadHunter(ApiVacancy):
    """
    Класс для работы с API HH
    """

    def __init__(self, parent_area, text):
        """
        Инициализация объекта класса параметрами поиска работодателя
        """
        self.text = text  # Текст поиска вакансии
        self.parent_area = None
        self.list_data_dict = []
        self.data_from_vacancy = []



    def import_vacancy_from_api(self):
        """
        Метод получения данных через API по указанным параметрам
        """
        try:
            for i in range(1, 11):
                page = i
                param = {'text': self.text,
                         # Переданное значение ищется в полях вакансии, указанных в параметре search_field
                         'parent_id': self.parent_area,  # Код страны.
                         'page': page,  # Параметры пагинации. Параметр per_page ограничен значением в 100
                         'per_page': 100
                         # Параметры пагинации. Параметр per_page ограничен значением в 100. Количество в странице
                         }
                req = requests.get("https://api.hh.ru/vacancies", param)  # Посылаем запрос к API
                data = req.content.decode()  # декодируем ответ чтобы  Кириллица отображалось корректно
                data_dict = json.loads(data)
                self.list_data_dict.extend(data_dict['items'])
                time.sleep(0.25)
        except ValueError:
            print("Ошибка значения, попробуйте снова")
            sys.exit()

    def response_format(self):
        """
        Форматирования ответа сервера
        """
        for i in range(0, len(self.list_data_dict)):
            items = {}
            items["name"] = self.list_data_dict[i]["name"]
            items["url"] = self.list_data_dict[i]["alternate_url"]
            if isinstance(self.list_data_dict[i]["salary"], dict):
                if isinstance(self.list_data_dict[i]["salary"]["from"], int):
                    items["salary"] = self.list_data_dict[i]["salary"]["from"]
                else:
                    items["salary"] = 0
            else:
                continue
            items["id_vacancy"] = self.list_data_dict[i]["id"]
            if "employer" in self.list_data_dict[i]:
                items["employer"] = self.list_data_dict[i]["employer"]["name"]  # сохранение имени работодателя
                items["employer_url"] = self.list_data_dict[i]["employer"][
                    "alternate_url"]  # сохранение ссылки на карточку работодателя
            else:
                items["employer"] = "нет данных"  # сохранение имени работодателя
                items["employer_url"] = "нет данных"  # сохранение ссылки на карточку работодателя
            items["requirement"] = self.list_data_dict[i]['snippet']['requirement']  # сохранение требований к вакансии
            items["responsibility"] = self.list_data_dict[i]['snippet'][
                'responsibility']  # сохранение обязанностей вакансии
            self.data_from_vacancy.append(items)

    def get_to_vacancy(self):
        """
        Метод возвращает полученные данные с API
        """
        return self.data_from_vacancy

    def get_to_employer(self):
        """
        Метод возвращает информацию о работодателе
        """
