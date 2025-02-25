class Person:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class MySQL():

    @staticmethod
    def save_person(person):
        # code to save in database
        print(f"Person {person.name} saved in Database")


class ServicePerson:

    @staticmethod
    def save_person(person):

        mysql_driver = MySQL()
        mysql_driver.save_person(person)


# Is not testable
# What happen if I change SQL to Mongo?

