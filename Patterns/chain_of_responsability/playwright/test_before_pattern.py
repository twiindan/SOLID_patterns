from playwright.sync_api import sync_playwright


def test_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")

        # Validate page loaded
        if page.title() != "Sign In - Microblog":
            print("❌ Invalid page title")
            return

        # Validate username field exists
        if not page.locator("#username").is_visible():
            print("❌ Username field not found")
            return

        # Validate password field exists
        if not page.locator("#password").is_visible():
            print("❌ Password field not found")
            return

        # Validate login button exists
        if not page.locator("#submit").is_visible():
            print("❌ Login button not found")
            return

        print("✅ UI Test Passed")
        browser.close()


# Run test
test_ui()
