# Before applying DIP
# This implementation violates the Dependency Inversion Principle

class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


# PROBLEM: This is a concrete low-level implementation
# The service will directly depend on this specific class
class MySQL:
    # Concrete implementation for MySQL database operations
    @staticmethod
    def save_person(person):
        # code to save in database
        print(f"Person {person.name} saved in Database")


# VIOLATION: This high-level service class directly depends on the low-level MySQL class
# This creates a tight coupling between the service and the specific database implementation
class ServicePerson:
    @staticmethod
    def save_person(person):
        # Direct instantiation of MySQL creates rigid dependency
        # The service class knows too much about how data is stored
        mysql_driver = MySQL()
        mysql_driver.save_person(person)


# ISSUES WITH THIS IMPLEMENTATION:
# 1. The ServicePerson class is tightly coupled to MySQL implementation
# 2. Impossible to unit test ServicePerson without a real MySQL connection
# 3. Changing database technology requires modifying the ServicePerson class
# 4. Violates the "high-level modules should not depend on low-level modules" principle
# 5. No abstraction layer between business logic and database implementation
