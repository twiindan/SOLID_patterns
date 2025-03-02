from abc import ABC, abstractmethod

# The Strategy Pattern defines a family of algorithms,
# encapsulates each one, and makes them interchangeable.

# Abstract Strategy - defines the interface that all concrete strategies must implement
class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, results):
        # All concrete strategies must implement this method
        pass


# Concrete Strategy 1 - Console output format
class ConsoleReport(ReportStrategy):
    def generate(self, results):
        # This strategy handles console output formatting
        print("Test Results:")
        for result in results:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['name']}")


# Concrete Strategy 2 - HTML output format
class HTMLReport(ReportStrategy):
    def generate(self, results):
        # This strategy handles HTML output formatting
        html = "<h1>Test Results</h1><ul>"
        for result in results:
            status = "PASS" if result["passed"] else "FAIL"
            html += f"<li>{result['name']}: {status}</li>"
        html += "</ul>"
        return html


# Concrete Strategy 3 - JSON output format
class JSONReport(ReportStrategy):
    def generate(self, results):
        # This strategy handles JSON output formatting
        import json
        return json.dumps(results)


# Context class - This class maintains a reference to a Strategy object
class TestResults:
    def __init__(self, report_strategy):
        # The strategy is injected via constructor - this is a form of dependency injection
        self.report_strategy = report_strategy
        self.test_results = []

    def add_result(self, test_name, passed):
        # Add test result to the collection
        self.test_results.append({"name": test_name, "passed": passed})

    def generate_report(self):
        # Delegate the report generation to the strategy
        # The context doesn't need to know how the report is generated
        return self.report_strategy.generate(self.test_results)


# Usage with Strategy Pattern
# Create context with console strategy
console_results = TestResults(ConsoleReport())
console_results.add_result("Login Test", True)
console_results.add_result("Logout Test", False)
console_results.generate_report()

# Easily switch to HTML report strategy
# No modification to TestResults class is needed to support different report types
html_results = TestResults(HTMLReport())
html_results.add_result("Login Test", True)
html_results.add_result("Logout Test", False)
html_results.generate_report()
