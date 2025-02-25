# Before applying ISP
# This class violates ISP by combining different types of validations and reporting
class TestValidator:
    def validate_database_record(self, query_result):
        """Validates database query results"""
        pass

    def validate_pdf_content(self, pdf_file):
        """Validates PDF file content"""
        pass

    def validate_excel_data(self, excel_file):
        """Validates Excel file data"""
        pass

    def generate_html_report(self):
        """Generates HTML test report"""
        pass

    def send_slack_notification(self, message):
        """Sends test results to Slack"""
        pass

    def update_test_management_tool(self, result):
        """Updates test case status in test management tool"""
        pass


# Test classes forced to implement all validation and reporting methods
class DatabaseTest(TestValidator):
    def test_user_creation(self):
        # Only needs database validation but gets all other methods
        self.validate_database_record("SELECT * FROM users")
        self.generate_html_report()  # Forced to use unwanted reporting


class PDFReportTest(TestValidator):
    def test_pdf_generation(self):
        # Only needs PDF validation but inherits unnecessary database and Excel methods
        self.validate_pdf_content("report.pdf")
        self.send_slack_notification("PDF test completed")
