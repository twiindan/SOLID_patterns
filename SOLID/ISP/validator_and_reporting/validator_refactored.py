# Segregated interfaces for different types of validations and reporting

# SOLUTION: The Interface Segregation Principle has been applied by breaking down
# the monolithic TestValidator into smaller, focused interfaces based on responsibility

# Interface for database validation
class DatabaseValidator:
    def validate_database_record(self, query_result):
        """Validates database query results"""
        pass


# Interface for PDF validation
class PDFValidator:
    def validate_pdf_content(self, pdf_file):
        """Validates PDF file content"""
        pass


# Interface for Excel validation
class ExcelValidator:
    def validate_excel_data(self, excel_file):
        """Validates Excel file data"""
        pass


# Interface for HTML report generation
class HTMLReporter:
    def generate_html_report(self):
        """Generates HTML test report"""
        pass


# Interface for Slack notifications
class SlackNotifier:
    def send_slack_notification(self, message):
        """Sends test results to Slack"""
        pass


# Interface for test management tool integration
class TestManagementUpdater:
    def update_test_management_tool(self, result):
        """Updates test case status in test management tool"""
        pass


# BENEFIT: This test class now only implements the interfaces it actually needs
# It has clear dependencies only on database validation and HTML reporting
class DatabaseTest(DatabaseValidator, HTMLReporter):
    def test_user_creation(self):
        self.validate_database_record("SELECT * FROM users")
        self.generate_html_report()
        # Clean implementation with only needed validation and reporting
        # No unnecessary methods inherited, reducing coupling and potential issues


# BENEFIT: This test class only implements PDF validation and Slack notification
# It's not burdened with other validation or reporting methods it doesn't need
class PDFReportTest(PDFValidator, SlackNotifier):
    def test_pdf_generation(self):
        self.validate_pdf_content("report.pdf")
        self.send_slack_notification("PDF test completed")
        # Only PDF validation and Slack notification capabilities
        # No dependency on database, Excel, HTML reports, or test management


# BENEFIT: Multiple inheritance allows composition of only the needed interfaces
# More complex test classes can still inherit multiple capabilities as needed
class ComplexReportTest(PDFValidator, ExcelValidator, HTMLReporter, TestManagementUpdater):
    def test_report_conversion(self):
        # Validate source Excel
        self.validate_excel_data("source.xlsx")

        # Validate generated PDF
        self.validate_pdf_content("output.pdf")

        # Report results
        self.generate_html_report()
        self.update_test_management_tool("PASSED")
        # This class needs multiple validation and reporting mechanisms
        # But still avoids inheriting the database validation and Slack notification
        # that it doesn't need, keeping dependencies minimal and explicit
