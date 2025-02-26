from playwright.sync_api import sync_playwright


# Observer class
class EventObserver:
    def __init__(self, page):
        self.page = page
        self.attach_listeners()

    def attach_listeners(self):
        self.page.on("request", self.on_request)
        self.page.on("response", self.on_response)
        self.page.on("pageerror", self.on_error)

    @staticmethod
    def on_request(request):
        print(f"➡️ Request: {request.method} {request.url}")

    @staticmethod
    def on_response(response):
        print(f"✅ Response: {response.status} {response.url}")

    @staticmethod
    def on_error(error):
        print(f"❌ ERROR: {error}")


# Playwright test using observer
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Attach observer
    observer = EventObserver(page)

    # Navigate to website
    page.goto("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")

    # Click a button
    page.click("#submit")

    # Close browser
    browser.close()
