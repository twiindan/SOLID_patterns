from abc import ABC, abstractmethod


class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


# SOLUTION: Create an abstraction (interface) that both high and low-level modules depend on
# This abstract class defines the contract that any persistence implementation must follow
class Persistence(ABC):
    # Abstract interface that defines the persistence behavior
    # Both the high-level service and low-level database implementations will depend on this abstraction
    @abstractmethod
    def save(person: Person) -> None:
        # This method must be implemented by any concrete persistence class
        pass


# SOLUTION: Low-level module now depends on abstraction
# Concrete implementation of the Persistence interface for MySQL
class MySql(Persistence):
    # This class provides the specific MySQL implementation
    # But adheres to the interface defined by the Persistence abstract class
    @abstractmethod
    def save(person: Person) -> None:
        # code to save in database
        pass


# SOLUTION: High-level module also depends on abstraction
# Service class now depends on the Persistence abstraction, not concrete implementation
class ServicePerson:
    # Dependency is injected through constructor
    # The class doesn't know or care which concrete persistence implementation it's using
    def __init__(self, persistence: Persistence):
        # Takes any implementation of Persistence interface
        self.persistence = persistence

    def save_person(self, person: Person):
        # Uses the abstraction method, not concrete implementation details
        self.persistence.save()
        print(f"Person {person.name} saved in Database")


# BENEFITS OF THIS IMPLEMENTATION:
# 1. ServicePerson can work with any persistence mechanism (MySQL, MongoDB, file system, etc.)
# 2. Easy to test with mock implementation of Persistence
# 3. Changing database technology doesn't require changes to ServicePerson class
# 4. Both high-level (ServicePerson) and low-level (MySql) modules depend on abstraction (Persistence)
# 5. New persistence implementations can be added without modifying existing code
# 6. Follows the principle: "Depend on abstractions, not on concretions"
