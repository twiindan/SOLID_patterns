from playwright.sync_api import sync_playwright

# PROBLEM: This approach lacks a formal structure for UI actions
# Issues with this implementation:
# 1. No way to track actions for potential undoing
# 2. Direct coupling between the test script and the UI interactions
# 3. Actions are not encapsulated and cannot be reused
# 4. Fixed sequence of operations that cannot be easily changed
# 5. No history of actions performed

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigate to shopping site
    print("Navigating to shopping page")
    page.goto("https://example.com/shop")

    # Adding items to cart is done directly by clicking UI elements
    # Each action is tightly coupled with the page implementation
    print("Adding first item to cart")
    page.click("#item-1 .add-to-cart")

    # Another item is added in the same way
    print("Adding second item to cart")
    page.click("#item-2 .add-to-cart")

    # Removing an item requires direct interaction with a specific element
    print("Removing first item from cart")
    page.click("#item-1 .remove-from-cart")

    # Proceeding to checkout is another direct UI interaction
    print("Proceeding to checkout")
    page.click("#checkout")

    browser.close()
