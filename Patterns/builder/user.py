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

    def with_name(self, name):
        self.name = name
        return self

    def with_surname(self, surname):
        self.name = surname
        return self

    def with_age(self, age):
        self.name = age
        return self

    def with_country(self, country):
        self.name = country
        return self

    def with_american_country(self):
        self.country = random.choice(["EEUU", "Mexico", "Uruguay", "Peru"])
        return self


user_builder = User()
user2 = user_builder.with_name('Toni').with_age(25).with_country('Spain')
user3 = user_builder.with_name('Toni').with_age(25).with_american_country()
print(user3.country)
