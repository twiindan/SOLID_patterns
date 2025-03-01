import requests


# Command Pattern Implementation for API Testing

# Base Command - Abstract class that defines the command interface
# Each API operation is encapsulated as a command with execute and undo capabilities
class Command:
    def execute(self):
        # This method will perform the actual API operation
        raise NotImplementedError("Subclasses must implement execute()")

    def undo(self):
        # This method will reverse the API operation if possible
        raise NotImplementedError("Subclasses must implement undo()")


# Concrete Command 1: Create User API Operation
class CreateUser(Command):
    def __init__(self, session, url, user_data):
        # Store all necessary information to perform the operation
        self.session = session
        self.url = url
        self.user_data = user_data
        self.user_id = None  # Will store the created user's ID for undo operation

    def execute(self):
        # Perform the user creation API call
        print("🆕 Creating a new user...")
        response = self.session.post(self.url, json=self.user_data)
        if response.status_code == 201:
            # Store the ID for potential undo operation
            self.user_id = response.json().get("id")
        print(f"✅ Created: {response.status_code}, {response.json()}")

    def undo(self):
        # Undo the creation by deleting the user
        if self.user_id:
            print(f"❌ Undo: Deleting user {self.user_id}...")
            response = self.session.delete(f"{self.url}/{self.user_id}")
            print(f"🗑️ Deleted: {response.status_code}")


# Concrete Command 2: Get User API Operation
class GetUser(Command):
    def __init__(self, session, url, user_id):
        self.session = session
        self.url = url
        self.user_id = user_id

    def execute(self):
        # Perform the get user API call
        print(f"🔍 Fetching details for user {self.user_id}...")
        response = self.session.get(f"{self.url}/{self.user_id}")
        print(f"📄 Response: {response.status_code}, {response.json()}")

    def undo(self):
        # Get operation doesn't modify data, so undo is not needed
        # However, we still implement the method as required by the interface
        pass


# Concrete Command 3: Update User API Operation
class UpdateUser(Command):
    def __init__(self, session, url, user_id, new_data):
        self.session = session
        self.url = url
        self.user_id = user_id
        self.new_data = new_data
        self.old_data = None  # Will store the previous user data for undo

    def execute(self):
        # First, get the current data to enable undoing
        print(f"📝 Updating user {self.user_id}...")
        old_response = self.session.get(f"{self.url}/{self.user_id}")
        if old_response.status_code == 200:
            # Store the current state for potential undo
            self.old_data = old_response.json()

        # Perform the update operation
        response = self.session.put(f"{self.url}/{self.user_id}", json=self.new_data)
        print(f"✅ Updated: {response.status_code}, {response.json()}")

    def undo(self):
        # Revert the user to its previous state
        if self.old_data:
            print(f"↩️ Undo: Reverting user {self.user_id} to previous state...")
            response = self.session.put(f"{self.url}/{self.user_id}", json=self.old_data)
            print(f"🔄 Reverted: {response.status_code}, {response.json()}")


# Concrete Command 4: Delete User API Operation
class DeleteUser(Command):
    def __init__(self, session, url, user_id):
        self.session = session
        self.url = url
        self.user_id = user_id

    def execute(self):
        # Perform the delete operation
        print(f"🗑️ Deleting user {self.user_id}...")
        response = self.session.delete(f"{self.url}/{self.user_id}")
        print(f"✅ Deleted: {response.status_code}")

    def undo(self):
        # To properly undo a delete, we would need to store the user data before deletion
        # This implementation is simplified and doesn't include full undo capability
        pass


# Command Invoker - Manages command execution and history
class APIInvoker:
    def __init__(self):
        # Command history for undo functionality
        self.history = []

    def execute_command(self, command):
        # Execute the command and add to history
        command.execute()
        self.history.append(command)

    def undo_last_command(self):
        # Undo the last executed command
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("⚠️ No actions to undo")


# BENEFITS OF COMMAND PATTERN IN API TESTING:
# 1. Encapsulation - Each API operation is encapsulated in its own class
# 2. Transactional operations - Changes can be undone if needed
# 3. Audit trail - History of operations is maintained
# 4. Reusability - Commands can be reused with different parameters
# 5. Separation of concerns - API operations are separated from their invocation

# Running API tests with Command Pattern
if __name__ == "__main__":
    # Create a session for all requests
    session = requests.Session()
    base_url = "https://jsonplaceholder.typicode.com/users"
    invoker = APIInvoker()

    # Create a user command
    create_cmd = CreateUser(session, base_url, {"name": "John Doe"})
    invoker.execute_command(create_cmd)

    # Get user details command
    get_cmd = GetUser(session, base_url, 1)
    invoker.execute_command(get_cmd)

    # Update user command
    update_cmd = UpdateUser(session, base_url, 1, {"name": "John Updated"})
    invoker.execute_command(update_cmd)

    # Demonstrate undo functionality - revert the update
    invoker.undo_last_command()

    # Delete user command
    delete_cmd = DeleteUser(session, base_url, 1)
    invoker.execute_command(delete_cmd)
