from playwright.sync_api import sync_playwright


# Base Handler
class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, page):
        if self.next_handler:
            return self.next_handler.handle(page)
        return True


# Concrete Handlers
class PageTitleValidator(Handler):
    def __init__(self, expected_title, next_handler=None):
        super().__init__(next_handler)
        self.expected_title = expected_title

    def handle(self, page):
        if page.title() != self.expected_title:
            print(f"❌ Invalid page title: {page.title()}")
            return False
        print("✅ Page title is correct")
        return super().handle(page)


class ElementValidator(Handler):
    def __init__(self, selector, description, next_handler=None):
        super().__init__(next_handler)
        self.selector = selector
        self.description = description

    def handle(self, page):
        if not page.locator(self.selector).is_visible():
            print(f"❌ {self.description} not found")
            return False
        print(f"✅ {self.description} is visible")
        return super().handle(page)


# UI Test using Chain of Responsibility
def test_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")

        # Define chain of responsibility
        validation_chain = PageTitleValidator("Sign In - Microblog",
                                              ElementValidator("#username", "Username textbox",
                                                               ElementValidator("#password", "Password textbox")
                                                               )
                                              )

        # Execute chain
        if validation_chain.handle(page):
            print("🎉 UI Test Passed")
        else:
            print("❌ UI Test Failed")

        browser.close()


# Run test
test_ui()
