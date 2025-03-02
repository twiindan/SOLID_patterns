# BEFORE: Without Strategy Pattern
# This implementation uses conditions to handle different report types
# which violates the Open/Closed Principle as adding new report formats
# requires modifying this class

class TestResults:
    def __init__(self, report_type):
        # The report type is just a string identifier
        self.report_type = report_type
        self.test_results = []

    def add_result(self, test_name, passed):
        # Add test result to the collection
        self.test_results.append({"name": test_name, "passed": passed})

    def generate_report(self):
        # This method contains all the logic for different report formats
        # Using if-elif statements makes it hard to maintain and extend
        if self.report_type == "console":
            # Print to console - Console output logic is mixed with data handling
            print("Test Results:")
            for result in self.test_results:
                status = "✅" if result["passed"] else "❌"
                print(f"{status} {result['name']}")

        elif self.report_type == "html":
            # Generate HTML report - HTML generation logic is mixed with data handling
            html = "<h1>Test Results</h1><ul>"
            for result in self.test_results:
                status = "PASS" if result["passed"] else "FAIL"
                html += f"<li>{result['name']}: {status}</li>"
            html += "</ul>"
            return html

        elif self.report_type == "json":
            # Generate JSON report - JSON generation logic is mixed with data handling
            import json
            return json.dumps(self.test_results)
        # Note: Adding a new report type would require modifying this method


# Simple usage example
test_results = TestResults("console")
test_results.add_result('login', True)
test_results.add_result('logout', False)
test_results.generate_report()
