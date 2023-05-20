from api_hh_class.headhunter_api_class import HeadHunter
from dbmanager_class.dbmanager_class import DBManager


""" Код создает объекты класса HeadHunter и базу данных. Импортирует данные с API и сохраняет в базу данных"""
HeadHunter.great_database()
list_firm = ["Московский университет имени С.Ю.Витте",
             "Санкт-Петербургский государственный электротехнический университет “ЛЭТИ” им. В.И. Ульянова (Ленина)",
             "Научно-Технологический Университет «Сириус",
             "Образовательное учреждение Дальневосточный федеральный университет",
             "Казанский (Приволжский) федеральный университет",
             "Московский авиационный институт (национальный исследовательский университет)",
             "ФГАОУ ВО Крымский Федеральный Университет Имени В.И. Вернадского",
             "Самарский Государственный университет Путей Сообщения филиал в г. Нижний Новгород",
             "Нек. орг. Российский университет дружбы народов, ФГАОУ ВО",
             "Дальневосточный государственный технический рыбохозяйственный университет"]
for x in range(0, len(list_firm)):
    i = HeadHunter(list_firm[x])
    i.research_employer_from_api()
    i.import_information_about_employer()
    i.import_vacancy_employer_from_api()
    i.get_to_employer()
    i.get_to_vacancy()


"""Запускаем функции класса DBManager, и распечатываем результат в виде количество полученных записей и пример записи"""
i = DBManager()
list_1 = i.get_companies_and_vacancies_count()
print(len(list_1))
print(list_1[0])
print()
list_2 = i.get_all_vacancies()
print(len(list_2))
print(list_2[0])
print()
print(f"Средняя зарплата - {i.get_avg_salary()}")
print()
list_3 = i.get_vacancies_with_higher_salary()
print(len(list_3))
print(list_3[0])
print()
list_4 = i.get_vacancies_with_keyword("Главный")
print(len(list_4))
print(list_4[0])
