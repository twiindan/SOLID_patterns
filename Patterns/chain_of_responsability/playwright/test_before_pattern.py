from playwright.sync_api import sync_playwright


def test_ui():
    # Initialize Playwright and create a browser instance
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        # Navigate to the target website
        page.goto("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")

        # PROBLEM: Monolithic validation function with sequential checks
        # This approach has several drawbacks:
        # 1. Poor maintainability - adding new validations requires modifying this function
        # 2. No reusability - validation logic cannot be easily reused in other tests
        # 3. Early returns create a rigid control flow
        # 4. Difficult to extend without making the function more complex

        # Check 1: Validate page title
        if page.title() != "Sign In - Microblog":
            print("❌ Invalid page title")
            return

        # Check 2: Validate username field exists
        if not page.locator("#username").is_visible():
            print("❌ Username field not found")
            return

        # Check 3: Validate password field exists
        if not page.locator("#password").is_visible():
            print("❌ Password field not found")
            return

        # Check 4: Validate login button exists
        if not page.locator("#submit").is_visible():
            print("❌ Login button not found")
            return

        # If all checks pass, report success
        print("✅ UI Test Passed")
        browser.close()


# Run test
test_ui()
