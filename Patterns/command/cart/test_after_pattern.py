from playwright.sync_api import sync_playwright


# Base Command class
class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")

    def undo(self):
        raise NotImplementedError("Subclasses must implement undo()")


# Concrete Commands
class AddToCart(Command):
    def __init__(self, page, item_id):
        self.page = page
        self.item_id = item_id

    def execute(self):
        print(f"🛒 Adding item {self.item_id} to cart")
        self.page.click(f"#item-{self.item_id} .add-to-cart")

    def undo(self):
        print(f"❌ Removing item {self.item_id} from cart")
        self.page.click(f"#item-{self.item_id} .remove-from-cart")


class Checkout(Command):
    def __init__(self, page):
        self.page = page

    def execute(self):
        print("💳 Proceeding to checkout")
        self.page.click("#checkout")

    def undo(self):
        print("⏪ Cancelling checkout (going back)")
        self.page.go_back()


# Command Invoker (Manages command execution and undo)
class CartInvoker:
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


# Running the test with Command Pattern
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigate to shopping site
    page.goto("https://example.com/shop")

    # Create invoker and add commands
    cart = CartInvoker()
    cart.execute_command(AddToCart(page, 1))  # Add item 1
    cart.execute_command(AddToCart(page, 2))  # Add item 2

    # Undo last action (remove item 2)
    cart.undo_last_command()

    # Proceed to checkout
    cart.execute_command(Checkout(page))

    browser.close()
