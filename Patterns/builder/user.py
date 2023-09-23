import random

class BasicUser:

    def __init__(self, name, surname, age, country):

        self.name = name
        self.surname = surname
        self.age = age
        self.country = country


user1 = BasicUser('Toni', 'Robres', 39, 'Spain')


class User():

    def __init__(self):
        self.name = None
        self.surname = None
        self.age = None
        self.country = None

    def set_name(self, name):
        self.name = name
        return self

    def set_surname(self, surname):
        self.name = surname
        return self

    def set_age(self, age):
        self.name = age
        return self

    def set_country(self, country):
        self.name = country
        return self

    def set_american_country(self):
        self.country = random.choice(["EEUU", "Mexico", "Uruguay", "Peru"])
        return self


user_builder = User()
user2 = user_builder.set_name('Toni').set_age(25).set_country('Spain')
user3 = user_builder.set_name('Toni').set_age(25).set_american_country()
print(user3.country)