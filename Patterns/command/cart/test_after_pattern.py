from playwright.sync_api import sync_playwright


# Command Pattern Implementation for E-commerce Testing

# Base Command - Abstract class that defines the command interface
# Each command must implement execute() and undo() methods
class Command:
    def execute(self):
        # This method will be overridden by concrete commands
        # to perform their specific actions
        raise NotImplementedError("Subclasses must implement execute()")

    def undo(self):
        # This method will be overridden by concrete commands
        # to reverse their specific actions
        raise NotImplementedError("Subclasses must implement undo()")


# Concrete Command 1: Handles adding items to the shopping cart
class AddToCart(Command):
    def __init__(self, page, item_id):
        # Store references needed to execute this command
        self.page = page
        self.item_id = item_id

    def execute(self):
        # Implementation of adding an item to the cart
        print(f"🛒 Adding item {self.item_id} to cart")
        self.page.click(f"#item-{self.item_id} .add-to-cart")

    def undo(self):
        # Implementation to reverse the action (remove the item)
        print(f"❌ Removing item {self.item_id} from cart")
        self.page.click(f"#item-{self.item_id} .remove-from-cart")


# Concrete Command 2: Handles the checkout process
class Checkout(Command):
    def __init__(self, page):
        # Store reference to the page
        self.page = page

    def execute(self):
        # Implementation of proceeding to checkout
        print("💳 Proceeding to checkout")
        self.page.click("#checkout")

    def undo(self):
        # Implementation to reverse the checkout action
        print("⏪ Cancelling checkout (going back)")
        self.page.go_back()


# Command Invoker - Responsible for executing commands and tracking history
# This class manages the command execution flow and enables undo functionality
class CartInvoker:
    def __init__(self):
        # Command history enables undo functionality
        self.history = []

    def execute_command(self, command):
        # Execute the command and store it in history
        command.execute()
        self.history.append(command)

    def undo_last_command(self):
        # Retrieve and undo the last command from history
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("⚠️ No actions to undo")


# BENEFITS OF COMMAND PATTERN:
# 1. Encapsulation - Each action is encapsulated in its own class
# 2. Extensibility - New commands can be added without changing existing code
# 3. History tracking - Commands can be stored for undo/redo functionality
# 4. Separation of concerns - Commands are separated from their invoker
# 5. Composability - Commands can be combined and sequenced flexibly

# Running the test with Command Pattern
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigate to shopping site
    page.goto("https://example.com/shop")

    # Create invoker to manage commands
    cart = CartInvoker()

    # Execute commands through the invoker
    cart.execute_command(AddToCart(page, 1))  # Add item 1
    cart.execute_command(AddToCart(page, 2))  # Add item 2

    # Demonstrate undo functionality
    cart.undo_last_command()  # Undo the last command (remove item 2)

    # Continue with checkout
    cart.execute_command(Checkout(page))

    browser.close()
