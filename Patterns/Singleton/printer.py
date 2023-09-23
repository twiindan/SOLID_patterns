class Printer:

    _instance = None
    num_pages = 0

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Printer, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def print(self, num_pages):
        self.num_pages += num_pages


printer1 = Printer()
printer2 = Printer()
print(printer1 is printer2)


class Employee:

    def __init__(self, name, role):
        self.name = name
        self.role = role

    @staticmethod
    def print(num_pages):
        printer = Printer()
        printer.print(num_pages)


employee1 = Employee('Toni', 'Robres')
employee2 = Employee('Juan', 'Barrero')
employee3 = Employee('Agapito', 'Iglesias')

employee1.print(3)
employee2.print(8)
employee3.print(54)

printer = Printer()
print(printer.num_pages)