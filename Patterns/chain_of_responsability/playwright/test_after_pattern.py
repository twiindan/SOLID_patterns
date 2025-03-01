from playwright.sync_api import sync_playwright


# Chain of Responsibility Pattern Implementation

# Base Handler - The abstract handler in the Chain of Responsibility pattern
# This class defines the interface for all concrete handlers and manages the chain
class Handler:
    def __init__(self, next_handler=None):
        # Each handler stores a reference to the next handler in the chain
        self.next_handler = next_handler

    def handle(self, page):
        # If there's a next handler, pass the request along the chain
        # This is the core of the Chain of Responsibility pattern
        if self.next_handler:
            return self.next_handler.handle(page)
        # If we've reached the end of the chain, return success
        return True


# Concrete Handler 1: Validates the page title
class PageTitleValidator(Handler):
    def __init__(self, expected_title, next_handler=None):
        super().__init__(next_handler)
        self.expected_title = expected_title

    def handle(self, page):
        # Perform this handler's specific validation logic
        if page.title() != self.expected_title:
            print(f"❌ Invalid page title: {page.title()}")
            return False  # Return false to indicate validation failure
        print("✅ Page title is correct")
        # Call the parent's handle method to continue the chain
        return super().handle(page)


# Concrete Handler 2: Validates if a specific element exists on the page
class ElementValidator(Handler):
    def __init__(self, selector, description, next_handler=None):
        super().__init__(next_handler)
        self.selector = selector
        self.description = description

    def handle(self, page):
        # Perform this handler's specific validation logic
        if not page.locator(self.selector).is_visible():
            print(f"❌ {self.description} not found")
            return False  # Return false to indicate validation failure
        print(f"✅ {self.description} is visible")
        # Call the parent's handle method to continue the chain
        return super().handle(page)


# UI Test using Chain of Responsibility pattern
def test_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")

        # BENEFITS OF CHAIN OF RESPONSIBILITY PATTERN:
        # 1. Decoupling - Each validation is independent and can be reused
        # 2. Single Responsibility - Each handler does one specific task
        # 3. Open/Closed Principle - Add new validations without changing existing code
        # 4. Composition over inheritance - Chain handlers in different orders as needed

        # Define chain of responsibility by nesting handlers
        # The chain is built from the inside out:
        # 1. The password field validator is passed as the next_handler to the username validator
        # 2. The username validator is passed as the next_handler to the page title validator
        validation_chain = PageTitleValidator("Sign In - Microblog",
                                              ElementValidator("#username", "Username textbox",
                                                               ElementValidator("#password", "Password textbox")
                                                               )
                                              )

        # Execute the first handler in the chain, which will propagate through all handlers
        if validation_chain.handle(page):
            print("🎉 UI Test Passed")
        else:
            print("❌ UI Test Failed")

        browser.close()


# Run test
test_ui()
