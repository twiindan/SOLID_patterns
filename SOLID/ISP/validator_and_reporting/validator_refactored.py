# Segregated interfaces for different types of validations and reporting

class DatabaseValidator:
    def validate_database_record(self, query_result):
        """Validates database query results"""
        pass


class PDFValidator:
    def validate_pdf_content(self, pdf_file):
        """Validates PDF file content"""
        pass


class ExcelValidator:
    def validate_excel_data(self, excel_file):
        """Validates Excel file data"""
        pass


class HTMLReporter:
    def generate_html_report(self):
        """Generates HTML test report"""
        pass


class SlackNotifier:
    def send_slack_notification(self, message):
        """Sends test results to Slack"""
        pass


class TestManagementUpdater:
    def update_test_management_tool(self, result):
        """Updates test case status in test management tool"""
        pass


# Now test classes only implement what they need
class DatabaseTest(DatabaseValidator, HTMLReporter):
    def test_user_creation(self):
        self.validate_database_record("SELECT * FROM users")
        self.generate_html_report()
        # Clean implementation with only needed validation and reporting


class PDFReportTest(PDFValidator, SlackNotifier):
    def test_pdf_generation(self):
        self.validate_pdf_content("report.pdf")
        self.send_slack_notification("PDF test completed")
        # Only PDF validation and Slack notification capabilities


# Complex test case that needs multiple validators
class ComplexReportTest(PDFValidator, ExcelValidator, HTMLReporter, TestManagementUpdater):
    def test_report_conversion(self):
        # Validate source Excel
        self.validate_excel_data("source.xlsx")

        # Validate generated PDF
        self.validate_pdf_content("output.pdf")

        # Report results
        self.generate_html_report()
        self.update_test_management_tool("PASSED")
