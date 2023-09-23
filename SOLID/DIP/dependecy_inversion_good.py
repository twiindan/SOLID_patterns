from abc import ABC, abstractmethod


class Person():

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class Persistence(ABC):

    @abstractmethod
    def save(object):
        pass


class MySql(Persistence):

    @staticmethod
    def save_person(person: Person):
        # code to save in database
        print(f"Person {person.name} saved in Database")


class ServicePerson:

    def __init__(self, persistence: Persistence):
        self.persistence = persistence

    def savePerson(self):
        self.persistence.save()

