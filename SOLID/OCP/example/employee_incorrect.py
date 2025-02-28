# This file demonstrates code that violates the Open/Closed Principle (OCP)
# The Open/Closed Principle states that software entities should be OPEN for extension
# but CLOSED for modification.

class Employee:
    # This class violates OCP because:
    # 1. To add a new employee type, we must MODIFY this existing class
    # 2. The calculate_payroll and get_benefits methods contain conditionals
    #    that need to be updated every time a new position is added
    # 3. This creates a high risk of bugs when extending functionality

    def __init__(self, name, surname, position):
        self.name = name
        self.surname = surname
        self.position = position  # Using a string to determine behavior is problematic

    def calculate_payroll(self, fix_payroll):
        # This method violates OCP because:
        # - Every new position requires modifying this method
        # - Adding a new position might introduce bugs in existing code
        # - The class has multiple reasons to change (violating Single Responsibility)
        if self.position == 'junior_developer':
            return fix_payroll * 1.10
        if self.position == 'senior_developer':
            return fix_payroll * 1.20
        if self.position == 'executive_manager':
            return fix_payroll * 1.50

    def get_benefits(self):
        # Similar to calculate_payroll, this method also violates OCP
        # - Each new position requires changing existing code
        # - String comparisons can lead to typo-related bugs
        # - Logic for different positions is mixed in one place
        if self.position == 'junior_developer':
            return ['ticket_restaurant']
        if self.position == 'senior_developer':
            return ['ticket_restaurant']
        if self.position == 'executive_manager':
            return ['ticket_restaurant', 'company_car']
