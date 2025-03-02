from playwright.sync_api import sync_playwright

# This file demonstrates code WITHOUT using the Observer pattern
# It shows a simple, procedural approach to browser automation

with sync_playwright() as p:
    # Initialize the browser and create a new page
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Logging manually - this is a primitive form of "observation"
    # The code directly mixes logging with the actual browser operations
    print("Navigating to https://example.com")
    page.goto("https://example.com")

    # Again, logging is hardcoded into the main execution flow
    # This approach tightly couples the logging with the browser actions
    print("Clicking the submit button")
    page.click("#submit")

    # No separation of concerns - logging and browser automation are mixed together
    # This makes it difficult to modify the logging behavior without changing the core functionality
    print("Closing browser")
    browser.close()

    # PROBLEMS WITH THIS APPROACH:
    # 1. No separation between core functionality and monitoring/logging
    # 2. To add new types of events to monitor, we would need to modify the main code
    # 3. No way to enable/disable certain types of monitoring without code changes
    # 4. Difficult to extend with new monitoring capabilities
