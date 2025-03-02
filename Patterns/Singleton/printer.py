class Printer:
    # Class variables shared across all instances
    _instance = None  # Will hold the single instance of the Printer class
    num_pages = 0     # Counter for total pages printed, shared across all references

    def __new__(cls):
        # SINGLETON PATTERN: Core implementation
        # This special method controls instance creation
        if cls._instance is None:
            # This message will only print once, the first time a Printer is created
            print('Creating the object')
            # Create the single instance by calling the parent class's __new__ method
            cls._instance = super(Printer, cls).__new__(cls)
            # Any one-time initialization can be placed here
            # Note: __init__ will still be called every time Printer() is called
        # Always return the same instance for any subsequent instantiation
        return cls._instance

    def print(self, num_pages):
        # Since all "instances" are actually references to the same object,
        # this method updates the shared num_pages counter
        self.num_pages += num_pages


# Creating two printer "instances"
printer1 = Printer()  # Creates the singleton instance
printer2 = Printer()  # Returns the existing singleton instance
# This will print True, confirming both variables reference the same object
print(printer1 is printer2)


class Employee:
    # Regular class (not a singleton)
    def __init__(self, name, role):
        self.name = name
        self.role = role

    @staticmethod
    def print(num_pages):
        # Static method that doesn't require an instance of Employee
        # This method obtains the singleton Printer instance
        printer = Printer()  # Gets the existing singleton instance
        # Each call to print adds to the same shared counter
        printer.print(num_pages)


# Creating multiple Employee instances (not singletons)
employee1 = Employee('Toni', 'Robres')
employee2 = Employee('Juan', 'Barrero')
employee3 = Employee('Agapito', 'Iglesias')

# Each employee uses the same printer instance behind the scenes
employee1.print(3)    # Adds 3 to the shared counter
employee2.print(8)    # Adds 8 to the shared counter
employee3.print(54)   # Adds 54 to the shared counter

# Getting the singleton Printer instance again
printer = Printer()
# This will print 65 (3 + 8 + 54), showing that all print jobs used the same counter
print(printer.num_pages)
