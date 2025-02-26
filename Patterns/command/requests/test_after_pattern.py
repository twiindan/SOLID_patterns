import requests


# Base Command class
class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")

    def undo(self):
        raise NotImplementedError("Subclasses must implement undo()")


# Concrete Commands
class CreateUser(Command):
    def __init__(self, session, url, user_data):
        self.session = session
        self.url = url
        self.user_data = user_data
        self.user_id = None  # Store the created user's ID

    def execute(self):
        print("🆕 Creating a new user...")
        response = self.session.post(self.url, json=self.user_data)
        if response.status_code == 201:
            self.user_id = response.json().get("id")
        print(f"✅ Created: {response.status_code}, {response.json()}")

    def undo(self):
        if self.user_id:
            print(f"❌ Undo: Deleting user {self.user_id}...")
            response = self.session.delete(f"{self.url}/{self.user_id}")
            print(f"🗑️ Deleted: {response.status_code}")


class GetUser(Command):
    def __init__(self, session, url, user_id):
        self.session = session
        self.url = url
        self.user_id = user_id

    def execute(self):
        print(f"🔍 Fetching details for user {self.user_id}...")
        response = self.session.get(f"{self.url}/{self.user_id}")
        print(f"📄 Response: {response.status_code}, {response.json()}")


class UpdateUser(Command):
    def __init__(self, session, url, user_id, new_data):
        self.session = session
        self.url = url
        self.user_id = user_id
        self.new_data = new_data
        self.old_data = None  # Store previous data for undo

    def execute(self):
        print(f"📝 Updating user {self.user_id}...")
        # Get current data before updating
        old_response = self.session.get(f"{self.url}/{self.user_id}")
        if old_response.status_code == 200:
            self.old_data = old_response.json()

        response = self.session.put(f"{self.url}/{self.user_id}", json=self.new_data)
        print(f"✅ Updated: {response.status_code}, {response.json()}")

    def undo(self):
        if self.old_data:
            print(f"↩️ Undo: Reverting user {self.user_id} to previous state...")
            response = self.session.put(f"{self.url}/{self.user_id}", json=self.old_data)
            print(f"🔄 Reverted: {response.status_code}, {response.json()}")


class DeleteUser(Command):
    def __init__(self, session, url, user_id):
        self.session = session
        self.url = url
        self.user_id = user_id

    def execute(self):
        print(f"🗑️ Deleting user {self.user_id}...")
        response = self.session.delete(f"{self.url}/{self.user_id}")
        print(f"✅ Deleted: {response.status_code}")


# Command Invoker
class APIInvoker:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        command.execute()
        self.history.append(command)

    def undo_last_command(self):
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("⚠️ No actions to undo")


# Running API tests with Command Pattern
if __name__ == "__main__":
    session = requests.Session()
    base_url = "https://jsonplaceholder.typicode.com/users"
    invoker = APIInvoker()

    # Create a user
    create_cmd = CreateUser(session, base_url, {"name": "John Doe"})
    invoker.execute_command(create_cmd)

    # Fetch user details
    get_cmd = GetUser(session, base_url, 1)
    invoker.execute_command(get_cmd)

    # Update user
    update_cmd = UpdateUser(session, base_url, 1, {"name": "John Updated"})
    invoker.execute_command(update_cmd)

    # Undo update
    invoker.undo_last_command()

    # Delete user
    delete_cmd = DeleteUser(session, base_url, 1)
    invoker.execute_command(delete_cmd)
