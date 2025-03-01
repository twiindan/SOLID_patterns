# Before applying ISP
# This example violates the Interface Segregation Principle by combining
# UI and API testing methods in a single interface

# PROBLEM: This class represents a "fat interface" that mixes UI testing and API testing
# responsibilities. It forces clients to depend on methods they don't use.
class TestPage:
    # UI-specific methods
    def click_element(self, locator):
        """Clicks on a web element"""
        pass

    def input_text(self, locator, text):
        """Inputs text into a web element"""
        pass

    def get_element_text(self, locator):
        """Gets text from a web element"""
        pass

    # API-specific methods
    def make_api_get_request(self, endpoint):
        """Makes a GET API request"""
        pass

    def make_api_post_request(self, endpoint, payload):
        """Makes a POST API request"""
        pass

    def validate_api_response(self, response):
        """Validates API response"""
        pass


# VIOLATION: This test class only uses UI methods but is forced to inherit
# the API methods it will never use, creating unnecessary dependencies
class LoginPageTest(TestPage):
    def test_login(self):
        self.input_text("username_field", "user1")
        self.input_text("password_field", "pass123")
        self.click_element("login_button")
        # This class doesn't need API methods but inherits them anyway
        # This violates ISP because the class depends on methods it doesn't use


# VIOLATION: Similarly, this API test class only needs API methods
# but inherits UI methods it doesn't use, creating tight coupling
# to functionality that's irrelevant for its purpose
class UserAPITest(TestPage):
    def test_get_user(self):
        response = self.make_api_get_request("/api/users/1")
        self.validate_api_response(response)
        # This class doesn't need UI methods but inherits them anyway
        # This creates maintenance overhead and potential confusion
