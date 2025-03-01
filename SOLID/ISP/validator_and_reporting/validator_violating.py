# Before applying ISP
# This class violates ISP by combining different types of validations and reporting

# PROBLEM: Example of a "fat interface" that violates the Interface
# Segregation Principle by combining multiple unrelated responsibilities:
# - Different types of data validation (database, PDF, Excel)
# - Different reporting mechanisms (HTML, Slack, test management tool)
class TestValidator:
    # Database validation methods
    def validate_database_record(self, query_result):
        """Validates database query results"""
        pass

    # PDF validation methods
    def validate_pdf_content(self, pdf_file):
        """Validates PDF file content"""
        pass

    # Excel validation methods
    def validate_excel_data(self, excel_file):
        """Validates Excel file data"""
        pass

    # HTML reporting methods
    def generate_html_report(self):
        """Generates HTML test report"""
        pass

    # Slack notification methods
    def send_slack_notification(self, message):
        """Sends test results to Slack"""
        pass

    # Test management tool integration
    def update_test_management_tool(self, result):
        """Updates test case status in test management tool"""
        pass


# VIOLATION: This test class only needs database validation and HTML reporting,
# but it's forced to inherit all other validation and reporting methods it will never use
class DatabaseTest(TestValidator):
    def test_user_creation(self):
        # Only needs database validation but gets all other methods
        self.validate_database_record("SELECT * FROM users")
        self.generate_html_report()  # Uses HTML reporting
        # But still inherits PDF/Excel validation and other reporting methods
        # This creates unnecessary dependencies and potential maintenance issues


# VIOLATION: Similarly, this class only needs PDF validation and Slack notifications,
# but inherits methods for database/Excel validation and other reporting mechanisms
class PDFReportTest(TestValidator):
    def test_pdf_generation(self):
        # Only needs PDF validation but inherits unnecessary database and Excel methods
        self.validate_pdf_content("report.pdf")
        self.send_slack_notification("PDF test completed")
        # This class has no need for database validation, Excel validation,
        # HTML reporting, or test management tool updates
