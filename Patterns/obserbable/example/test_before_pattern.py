from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Logging manually
    print("Navigating to https://example.com")
    page.goto("https://example.com")

    print("Clicking the submit button")
    page.click("#submit")

    print("Closing browser")
    browser.close()
