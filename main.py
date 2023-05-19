from api_hh_class.headhunter_api_class import HeadHunter

hh = HeadHunter('Tigers Realm Coal')
hh.research_employer_from_api()
print(1)
hh.import_information_about_employer()
hh.import_vacancy_employer_from_api()
hh.get_to_employer()
hh.get_to_vacancy()