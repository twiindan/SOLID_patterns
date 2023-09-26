# Each module should have only one reason to change (Separation of Concerns)

# Examples

"""
Let’s take the example of a Telephone Directory application.
We are designing a Telephone Directory and that contains a TelephoneDirectory Class
which is supposed to handle the primary responsibility of maintaining Telephone Directory entries,
i. e Telephone numbers and names of the entities to which the Telephone Numbers belong.
Thus, the operations that this class is expected to perform are adding a new entry (Name and Telephone Number),
delete an existing entry, change a Telephone Number assigned to an entity Name, and provide
a lookup that returns the Telephone Number assigned to a particular entity Name.
"""


class PhoneDirectory:
    def __init__(self):
        self.phone_directory = {}

    def add_entry(self, name, number):
        self.phone_directory[name] = number

    def delete_entry(self, name):
        self.phone_directory.pop(name)

    def update_entry(self, name, number):
        self.phone_directory[name] = number

    def find_entry(self, name):
        return self.phone_directory[name]

"""
Now let’s say that there are two more requirements in the project – Persist the contents of the Telephone Directory 
to a Database and transfer the contents of Telephone Directory to a file.
"""


class TelephoneDirectory:
    def __init__(self):
        self.telephonedirectory = {}

    def add_entry(self, name, number):
        self.telephonedirectory[name] = number

    def delete_entry(self, name):
        self.telephonedirectory.pop(name)

    def update_entry(self, name, number):
        self.telephonedirectory[name] = number

    def find_entry(self, name):
        return self.telephonedirectory[name]

    def save_to_file(self, file_name, location):
        # code to save the contents of telephonedirectory dictionary to the file
        pass

    def persist_to_database(self, database_details):
        # code to persist the contents of telephonedirectory dictionary to database
        pass

    def __str__(self):
        ret_dct = ""
        for key, value in self.telephonedirectory.items():
            ret_dct += f'{key} : {value}\n'
        return ret_dct

""" We are broking the SRP principle because we are adding new responsabilities to the class. 
Instead of adding this new methods or functions we can create new classes with the new responsabilities
"""


class persist_to_database:
  #functionality of the class
  def __init__(self, object_to_persist):
    pass


class save_to_file:
  #functionality of the class
  def __init__(self, object_to_save):
    pass

