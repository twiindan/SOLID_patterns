from playwright.sync_api import sync_playwright


# Observer class - implements the Observer pattern
# This class is responsible for monitoring events from the page (the "Subject")
class EventObserver:
    def __init__(self, page):
        self.page = page  # The page is the "Subject" being observed
        self.attach_listeners()  # Register as an observer for various events

    # Method to register this observer for different events on the page
    def attach_listeners(self):
        # Subscribe to various events from the page
        # When these events occur, the corresponding methods will be called
        self.page.on("request", self.on_request)     # Listen for network requests
        self.page.on("response", self.on_response)   # Listen for network responses
        self.page.on("pageerror", self.on_error)     # Listen for JavaScript errors

    # Event handler for request events
    # Static method because it doesn't need access to instance variables
    @staticmethod
    def on_request(request):
        print(f"➡️ Request: {request.method} {request.url}")

    # Event handler for response events
    @staticmethod
    def on_response(response):
        print(f"✅ Response: {response.status} {response.url}")

    # Event handler for error events
    @staticmethod
    def on_error(error):
        print(f"❌ ERROR: {error}")


# Playwright test using observer pattern
with sync_playwright() as p:
    # Initialize browser and page (these are the "Subjects" in Observer pattern)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Attach observer to monitor page events
    # This creates clear separation between the core functionality and the monitoring
    observer = EventObserver(page)

    # Core functionality - navigate to website
    # Note how there's no logging code here - the observer handles that automatically
    page.goto("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")

    # Perform actions - observers will automatically track events
    page.click("#submit")

    # Close browser
    browser.close()

    # BENEFITS OF THIS APPROACH:
    # 1. Clear separation between the core functionality and monitoring/logging
    # 2. Can add new observers or modify existing ones without changing core code
    # 3. Easy to enable/disable certain types of monitoring
    # 4. Can have multiple observers for different purposes (logging, analytics, etc.)
    # 5. The page (Subject) doesn't need to know details about its observers
