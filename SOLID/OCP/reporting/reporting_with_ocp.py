from abc import ABC, abstractmethod
from typing import List, Dict


# APPLYING OCP: A structured data class for test results
class TestResult:
    def __init__(self, name: str, passed: bool, execution_time: float = 0.0):
        self.name = name
        self.passed = passed


# APPLYING OCP: Abstract base class defining the interface for all report generators
# This is the key to OCP - it provides an extension point for new report formats
class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, test_results: List[TestResult]) -> str:
        # Abstract method that concrete generators will implement
        pass


# APPLYING OCP: Concrete implementation for HTML format
# Extends the system without modifying existing code
class HTMLReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> str:
        # HTML-specific implementation
        report = """
        <html>
        <head>
            <style>
                .passed { color: green; }
                .failed { color: red; }
            </style>
        </head>
        <body>
        <h1>Test Execution Report</h1>
        """

        for test in test_results:
            status_class = "passed" if test.passed else "failed"
            status_text = "Passed" if test.passed else "Failed"
            report += f"""
            <div class="{status_class}">
                <p>Test: {test.name}</p>
                <p>Status: {status_text}</p>
            </div>
            """

        report += "</body></html>"
        return report


# APPLYING OCP: Concrete implementation for JSON format
# Can be added without changing existing code
class JSONReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> Dict:
        # JSON-specific implementation
        return {
            "test_results": [
                {
                    "name": test.name,
                    "status": "Passed" if test.passed else "Failed",
                }
                for test in test_results
            ],
            "summary": {
                "total": len(test_results),
                "passed": sum(1 for test in test_results if test.passed),
                "failed": sum(1 for test in test_results if not test.passed)
            }
        }


# APPLYING OCP: Concrete implementation for text format
# Can be added without changing existing code
class TextReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> str:
        # Text-specific implementation
        report = "TEST EXECUTION REPORT\n" + "=" * 20 + "\n\n"

        for test in test_results:
            status = "PASSED" if test.passed else "FAILED"
            report += f"Test: {test.name}\n"
            report += f"Status: {status}\n"
            report += "-" * 20 + "\n"

        total_tests = len(test_results)
        passed_tests = sum(1 for test in test_results if test.passed)
        report += f"\nSummary:\n"
        report += f"Total Tests: {total_tests}\n"
        report += f"Passed: {passed_tests}\n"
        report += f"Failed: {total_tests - passed_tests}\n"

        return report


# APPLYING OCP: New format added without modifying existing code
# This demonstrates how OCP allows extension without modification
class XMLReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> str:
        # XML-specific implementation
        report = '<?xml version="1.0" encoding="UTF-8"?>\n'
        report += '<testResults>\n'

        for test in test_results:
            report += f'  <test>\n'
            report += f'    <name>{test.name}</name>\n'
            report += f'    <status>{"Passed" if test.passed else "Failed"}</status>\n'
            report += f'  </test>\n'

        report += '</testResults>'
        return report


# APPLYING OCP: Client class that uses polymorphism to work with any ReportGenerator
class TestReportingSystem:
    def __init__(self, generator: ReportGenerator):
        # Dependency injection allows swapping different generators
        self.generator = generator

    def generate_report(self, test_results: List[TestResult]):
        # Delegates to the injected generator without knowing its concrete type
        return self.generator.generate(test_results)


# Examples
if __name__ == "__main__":
    # Test data
    test_results = [
        TestResult("Login Test", True, 1.5),
        TestResult("Data Validation", True, 0.8),
        TestResult("Logout Test", False, 0.3)
    ]

    # APPLYING OCP: Create different report generators without modifying existing code
    # Client code works with abstract base class (ReportGenerator) not concrete implementations
    html_reporter = TestReportingSystem(HTMLReportGenerator())
    json_reporter = TestReportingSystem(JSONReportGenerator())
    text_reporter = TestReportingSystem(TextReportGenerator())
    xml_reporter = TestReportingSystem(XMLReportGenerator())  # New format added easily

    # Generate reports - client code remains unchanged when new formats are added
    html_output = html_reporter.generate_report(test_results)
    json_output = json_reporter.generate_report(test_results)
    text_output = text_reporter.generate_report(test_results)
    xml_output = xml_reporter.generate_report(test_results)  # Using the new format

    print("Text Report Example:")
    print(html_output)

"""
With OCP :

The code follows OCP by being open for extension (new formats) but closed for modification
An abstract base class ReportGenerator defines the interface
Each report format is a separate concrete class that implements the abstract method
New formats (like XML) can be added without changing existing code
Uses polymorphism through a consistent interface
Client code works with the abstract type, not concrete implementations
"""