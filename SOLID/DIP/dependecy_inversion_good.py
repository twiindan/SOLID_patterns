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
    def save():
        # code to save in database
        pass


class ServicePerson:

    def __init__(self, persistence: Persistence):
        self.persistence = persistence

    def savePerson(self, person: Person):
        self.persistence.save()
        print(f"Person {person.name} saved in Database")
