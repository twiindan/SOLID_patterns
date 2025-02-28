# BEFORE: Without Strategy Pattern
class TestResults:
    def __init__(self, report_type):
        self.report_type = report_type
        self.test_results = []

    def add_result(self, test_name, passed):
        self.test_results.append({"name": test_name, "passed": passed})

    def generate_report(self):
        if self.report_type == "console":
            # Print to console
            print("Test Results:")
            for result in self.test_results:
                status = "✅" if result["passed"] else "❌"
                print(f"{status} {result['name']}")

        elif self.report_type == "html":
            # Generate HTML report
            html = "<h1>Test Results</h1><ul>"
            for result in self.test_results:
                status = "PASS" if result["passed"] else "FAIL"
                html += f"<li>{result['name']}: {status}</li>"
            html += "</ul>"
            return html

        elif self.report_type == "json":
            # Generate JSON report
            import json
            return json.dumps(self.test_results)


test_results = TestResults("console")
test_results.add_result('login', True)
test_results.add_result('logout', False)
test_results.generate_report()
