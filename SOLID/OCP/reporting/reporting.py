# VIOLATION OF OCP: This class must be modified every time a new report format is needed
class TestReportGenerator:
    def generate_report(self, test_results, format_type):
        # VIOLATION OF OCP: This method uses conditionals to determine behavior
        # Any new format requires modifying this existing method
        if format_type == "html":
            # Generates HTML report
            report = "<html><body>"
            for test in test_results:
                status = "Passed" if test["passed"] else "Failed"
                report += f"<p>Test: {test['name']} - Status: {status}</p>"
            report += "</body></html>"
            return report

        elif format_type == "json":
            # Generates JSON report
            return {
                "tests": [
                    {
                        "name": test["name"],
                        "status": "Passed" if test["passed"] else "Failed"
                    }
                    for test in test_results
                ]
            }

        elif format_type == "txt":
            # Generates plain text report
            report = "Test Results:\n"
            for test in test_results:
                status = "Passed" if test["passed"] else "Failed"
                report += f"Test: {test['name']} - Status: {status}\n"
            return report

        else:
            # Even error handling would need to be modified when adding new formats
            raise ValueError(f"Unsupported format: {format_type}")

# Example usage
test_results = [
    {"name": "Login Test", "passed": True},
    {"name": "Logout Test", "passed": False}
]

# VIOLATION OF OCP: Client code needs to work with format types as strings
# Makes the system more prone to errors (typos in format strings)
generator = TestReportGenerator()
html_report = generator.generate_report(test_results, "html")
json_report = generator.generate_report(test_results, "json")
txt_report = generator.generate_report(test_results, "txt")
print(html_report)
print(json_report)
print(txt_report)

"""
Without OCP:

TestReportGenerator class violates OCP because it must be modified every time a new report format is needed
The generate_report method uses conditionals (if/elif/else) to determine behavior
Adding a new format requires modifying existing code
"""