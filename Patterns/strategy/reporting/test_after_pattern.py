from abc import ABC, abstractmethod


class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, results):
        pass


class ConsoleReport(ReportStrategy):
    def generate(self, results):
        print("Test Results:")
        for result in results:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['name']}")


class HTMLReport(ReportStrategy):
    def generate(self, results):
        html = "<h1>Test Results</h1><ul>"
        for result in results:
            status = "PASS" if result["passed"] else "FAIL"
            html += f"<li>{result['name']}: {status}</li>"
        html += "</ul>"
        return html


class JSONReport(ReportStrategy):
    def generate(self, results):
        import json
        return json.dumps(results)


class TestResults:
    def __init__(self, report_strategy):
        self.report_strategy = report_strategy
        self.test_results = []

    def add_result(self, test_name, passed):
        self.test_results.append({"name": test_name, "passed": passed})

    def generate_report(self):
        return self.report_strategy.generate(self.test_results)


# Usage with Strategy
console_results = TestResults(ConsoleReport())
console_results.add_result("Login Test", True)
console_results.add_result("Logout Test", False)
console_results.generate_report()

# Easily switch to HTML report
html_results = TestResults(HTMLReport())
html_results.add_result("Login Test", True)
html_results.add_result("Logout Test", False)
html_results.generate_report()
