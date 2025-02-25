class TestReportGenerator:
    def generate_report(self, test_results, format_type):
        if format_type == "html":
            # Genera reporte HTML
            report = "<html><body>"
            for test in test_results:
                status = "Passed" if test["passed"] else "Failed"
                report += f"<p>Test: {test['name']} - Status: {status}</p>"
            report += "</body></html>"
            return report

        elif format_type == "json":
            # Genera reporte JSON
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
            # Genera reporte texto plano
            report = "Test Results:\n"
            for test in test_results:
                status = "Passed" if test["passed"] else "Failed"
                report += f"Test: {test['name']} - Status: {status}\n"
            return report

        else:
            raise ValueError(f"Unsupported format: {format_type}")

test_results = [
    {"name": "Login Test", "passed": True},
    {"name": "Logout Test", "passed": False}
]

generator = TestReportGenerator()
html_report = generator.generate_report(test_results, "html")
json_report = generator.generate_report(test_results, "json")
txt_report = generator.generate_report(test_results, "txt")
print(html_report)
print(json_report)
print(txt_report)