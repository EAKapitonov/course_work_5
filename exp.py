import json
import requests

text_employer = "Дальневосточный государственный технический рыбохозяйственный университет"
parent_area_employer = 113  # Россия
page = 0
param = {'text': text_employer,
         'parent_id': parent_area_employer,  # Код страны.
         'page': page,  # Номер страницы с работодателями (считается от 0, по умолчанию — 0)
         'per_page': 10  # Количество элементов на страницу (по умолчанию — 20, максимум — 100 )
         }
req = requests.get("https://api.hh.ru/employers", param)  # Посылаем запрос к API
data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
data_dict = json.loads(data)
print(data_dict)
print()


employer_id = data_dict['items'][0]['id']  # Идентификатор работодателя
param = {'employer_id': employer_id  # Идентификатор работодателя
         }
req = requests.get(f"https://api.hh.ru/employers/{employer_id}")  # Посылаем запрос к API
data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
employer = json.loads(data)
print(employer)
print()


parent_area_employer = 113  # Россия
page = 0
param_ = {'employer_id': employer_id,  # Идентификатор работодателя. Можно указать несколько значений
          'page': page,  # Номер страницы с работодателями (считается от 0, по умолчанию — 0)
          'per_page': 100  # Количество элементов на страницу (по умолчанию — 20, максимум — 100 )
          }
req = requests.get("https://api.hh.ru/vacancies", param_)  # Посылаем запрос к API
data = req.content.decode()  # декодируем ответ чтобы Кириллица отображалось корректно
vac = json.loads(data)
print(len(vac['items']))
