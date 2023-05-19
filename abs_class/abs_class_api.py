from abc import ABC, abstractmethod


class AbsHeadHunter(ABC):
    @abstractmethod
    def research_employer_from_api(self):
        """
        Метод получения данных через API по указанным параметрам
        """
        pass

    @abstractmethod
    def import_information_about_employer(self):
        """
        Получение информации об работодателе
        """
        pass

    @abstractmethod
    def import_vacancy_employer_from_api(self):
        """
        Получает данные с вакансиями по employer_id
        """
        pass


    @abstractmethod
    def get_to_vacancy(self):
        """
        Метод добавляет в базу данных вакансии работодателей
        """
        pass

    @abstractmethod
    def get_to_employer(self):
        """
        Метод добавляет работодателя в базу данных
        """
        pass
