from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigate to shopping site
    print("Navigating to shopping page")
    page.goto("https://example.com/shop")

    # Add first item to cart
    print("Adding first item to cart")
    page.click("#item-1 .add-to-cart")

    # Add second item to cart
    print("Adding second item to cart")
    page.click("#item-2 .add-to-cart")

    # Remove first item from cart
    print("Removing first item from cart")
    page.click("#item-1 .remove-from-cart")

    # Checkout
    print("Proceeding to checkout")
    page.click("#checkout")

    browser.close()
