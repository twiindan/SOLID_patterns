class Employee():

    def __init__(self, name, surname, position):
        self.name = name
        self.surname = surname
        self.position = position

    def calculate_payroll(self, fix_payroll):
        if self.position == 'junior_developer':
            return fix_payroll * 1.10
        if self.position == 'senior_developer':
            return fix_payroll * 1.20
        if self.position == 'executive_manager':
            return fix_payroll * 1.50

    def get_benefits(self):
        if self.position == 'junior_developer':
            return ['ticket_restaurant']
        if self.position == 'senior_developer':
            return ['ticket_restaurant']
        if self.position == 'executive_manager':
            return ['ticket_restaurant', 'company_car']
