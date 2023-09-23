from abc import ABC, abstractmethod


class Employee(ABC):

    @abstractmethod
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    @abstractmethod
    def calculate_payroll(self, fix_payroll):
        pass

    @abstractmethod
    def get_benefits(self):
        pass


class JuniorDeveloper(Employee):

    def calculate_payroll(self, fix_payroll):
        return fix_payroll * 1,10

    def get_benefits(self):
        return ['ticket_restaurant']


class SeniorDeveloper(Employee):

    def calculate_payroll(self, fix_payroll):
        return fix_payroll * 1.20

    def get_benefits(self):
        return ['ticket_restaurant']


class ExecutiveManager(Employee):
    def calculate_payroll(self, fix_payroll):
        return fix_payroll * 1.50

    def get_benefits(self):
        return ['ticket_restaurant', 'company_car']

