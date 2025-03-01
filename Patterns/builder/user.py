import random


# Basic implementation of a user class using traditional constructor
class BasicUser:
    """
    Traditional way to create a user object.
    All parameters must be provided at initialization time.
    """
    def __init__(self, name, surname, age, country):
        self.name = name
        self.surname = surname
        self.age = age
        self.country = country


# Example of creating a user with the traditional approach
user1 = BasicUser('Toni', 'Robres', 41, 'Spain')


# Implementation of the Builder pattern for creating users
class User:
    """
    User class that implements the Builder pattern.
    Allows for step-by-step construction of a User object with method chaining.
    """
    def __init__(self):
        # Initialize all attributes as None
        self.name = None
        self.surname = None
        self.age = None
        self.country = None

    def with_name(self, name):
        """Set the user's name and return self for method chaining."""
        self.name = name  # Fixed: was incorrectly setting self.name
        return self

    def with_surname(self, surname):
        """Set the user's surname and return self for method chaining."""
        self.surname = surname  # Fixed: was incorrectly setting self.name
        return self

    def with_age(self, age):
        """Set the user's age and return self for method chaining."""
        self.age = age  # Fixed: was incorrectly setting self.name
        return self

    def with_country(self, country):
        """Set the user's country and return self for method chaining."""
        self.country = country  # Fixed: was incorrectly setting self.name
        return self

    def with_american_country(self):
        """
        Set the user's country to a random American country.
        This demonstrates how builders can encapsulate complex logic.
        """
        self.country = random.choice(["USA", "Mexico", "Uruguay", "Peru"])
        return self


# Example of the Builder pattern in use
user_builder = User()

# Create a user with specific attributes using method chaining
user2 = user_builder.with_name('Toni').with_age(25).with_country('Spain')

# Create another user with a random American country
# Note: This should be a new User() instance to avoid overwriting user2
user_builder = User()  # Fixed: creating a new instance to avoid modifying user2
user3 = user_builder.with_name('Toni').with_age(25).with_american_country()

# Print the randomly selected country
print(user3.country)
