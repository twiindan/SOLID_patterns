from abc import ABC, abstractmethod
from typing import List, Dict


class TestResult:
    def __init__(self, name: str, passed: bool, execution_time: float = 0.0):
        self.name = name
        self.passed = passed


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, test_results: List[TestResult]) -> str:
        pass


class HTMLReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> str:
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


class JSONReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> Dict:
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


class TextReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> str:
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


# New XML Generator
class XMLReportGenerator(ReportGenerator):
    def generate(self, test_results: List[TestResult]) -> str:
        report = '<?xml version="1.0" encoding="UTF-8"?>\n'
        report += '<testResults>\n'

        for test in test_results:
            report += f'  <test>\n'
            report += f'    <name>{test.name}</name>\n'
            report += f'    <status>{"Passed" if test.passed else "Failed"}</status>\n'
            report += f'  </test>\n'

        report += '</testResults>'
        return report


# Class to use to generate different reports
class TestReportingSystem:
    def __init__(self, generator: ReportGenerator):
        self.generator = generator

    def generate_report(self, test_results: List[TestResult]):
        return self.generator.generate(test_results)


# Examples
if __name__ == "__main__":
    # Datos de prueba
    test_results = [
        TestResult("Login Test", True, 1.5),
        TestResult("Data Validation", True, 0.8),
        TestResult("Logout Test", False, 0.3)
    ]

    # Generate different reporters
    html_reporter = TestReportingSystem(HTMLReportGenerator())
    json_reporter = TestReportingSystem(JSONReportGenerator())
    text_reporter = TestReportingSystem(TextReportGenerator())
    xml_reporter = TestReportingSystem(XMLReportGenerator())

    # Generate reports
    html_output = html_reporter.generate_report(test_results)
    json_output = json_reporter.generate_report(test_results)
    text_output = text_reporter.generate_report(test_results)
    xml_output = xml_reporter.generate_report(test_results)

    print("Text Report Example:")
    print(html_output)
