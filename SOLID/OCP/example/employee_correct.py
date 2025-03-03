from abc import ABC, abstractmethod


# This file demonstrates code that follows the Open/Closed Principle (OCP)
# OCP states that software entities should be OPEN for extension but CLOSED for modification

class Employee(ABC):
    # Using an abstract base class (ABC) with abstract methods creates
    # a blueprint that can be extended without modifying existing code
    # This is the foundation of adhering to the Open/Closed Principle

    @abstractmethod
    def __init__(self, name, surname):
        # Base initialization that all employee types will share
        # Note we no longer need a 'position' parameter - the class type itself
        # represents the employee's position
        self.name = name
        self.surname = surname

    @abstractmethod
    def calculate_payroll(self, fix_payroll):
        # Abstract method that each subclass must implement
        # This creates a contract that all employee types will follow
        pass

    @abstractmethod
    def get_benefits(self):
        # Another abstract method that enforces the contract
        # Each employee type will implement its own benefit logic
        pass


class JuniorDeveloper(Employee):
    # New employee type is created by EXTENDING the base class
    # rather than MODIFYING existing code

    def __init__(self, name, surname):
        # Note: This method is missing but should implement the parent init
        super().__init__(name, surname)

    def calculate_payroll(self, fix_payroll):
        # Implementation specific to JuniorDeveloper
        # Note: There's a bug here - using comma instead of decimal point
        return fix_payroll * 1.10

    def get_benefits(self):
        # Benefits specific to JuniorDeveloper
        return ['ticket_restaurant']


class SeniorDeveloper(Employee):
    # Another employee type extending the base class

    def __init__(self, name, surname):
        # Note: This method is missing but should implement the parent init
        super().__init__(name, surname)

    def calculate_payroll(self, fix_payroll):
        # Implementation specific to SeniorDeveloper
        return fix_payroll * 1.20

    def get_benefits(self):
        # Benefits specific to SeniorDeveloper
        return ['ticket_restaurant']


class ExecutiveManager(Employee):
    # A third employee type extending the base class

    def __init__(self, name, surname):
        # Note: This method is missing but should implement the parent init
        super().__init__(name, surname)

    def calculate_payroll(self, fix_payroll):
        # Implementation specific to ExecutiveManager
        return fix_payroll * 1.50

    def get_benefits(self):
        # Benefits specific to ExecutiveManager
        return ['ticket_restaurant', 'company_car']
