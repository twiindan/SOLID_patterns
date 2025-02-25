class TestPage:
    def click_element(self, locator):
        """Clicks on a web element"""
        pass

    def input_text(self, locator, text):
        """Inputs text into a web element"""
        pass

    def get_element_text(self, locator):
        """Gets text from a web element"""
        pass

    def make_api_get_request(self, endpoint):
        """Makes a GET API request"""
        pass

    def make_api_post_request(self, endpoint, payload):
        """Makes a POST API request"""
        pass

    def validate_api_response(self, response):
        """Validates API response"""
        pass


# Test class forced to implement unnecessary methods
class LoginPageTest(TestPage):
    def test_login(self):
        self.input_text("username_field", "user1")
        self.input_text("password_field", "pass123")
        self.click_element("login_button")
        # This class doesn't need API methods but inherits them anyway


class UserAPITest(TestPage):
    def test_get_user(self):
        response = self.make_api_get_request("/api/users/1")
        self.validate_api_response(response)
        # This class doesn't need UI methods but inherits them anyway

