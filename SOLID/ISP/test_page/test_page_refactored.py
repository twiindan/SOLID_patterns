# After applying ISP
# Segregated interfaces for different testing responsibilities

# SOLUTION: The Interface Segregation Principle has been applied by splitting
# the single "fat" interface into smaller, focused interfaces based on responsibility

# Interface for UI-specific testing actions
# This separates the UI testing concerns from API testing
class UIActions:
    def click_element(self, locator):
        """Clicks on a web element"""
        pass

    def input_text(self, locator, text):
        """Inputs text into a web element"""
        pass

    def get_element_text(self, locator):
        """Gets text from a web element"""
        pass


# Interface for API-specific testing actions
# This separates the API testing concerns from UI testing
class APIActions:
    def make_api_get_request(self, endpoint):
        """Makes a GET API request"""
        pass

    def make_api_post_request(self, endpoint, payload):
        """Makes a POST API request"""
        pass

    def validate_api_response(self, response):
        """Validates API response"""
        pass


# BENEFIT: This test class now only implements the UI interface it needs
# It doesn't inherit any API methods, making the dependencies clear and focused
class LoginPageTest(UIActions):
    def test_login(self):
        self.input_text("username_field", "user1")
        self.input_text("password_field", "pass123")
        self.click_element("login_button")
        # Clean implementation with only needed UI methods
        # The class is now more focused, with clearer responsibilities
        # It's not coupled to any API-related functionality


# BENEFIT: This test class only implements the API interface it needs
# It's not burdened with UI methods that aren't relevant to its purpose
class UserAPITest(APIActions):
    def test_get_user(self):
        response = self.make_api_get_request("/api/users/1")
        self.validate_api_response(response)
        # Clean implementation with only needed API methods
        # The separation of concerns makes this class more maintainable
        # and prevents changes to UI methods from affecting API tests
