from typing import Dict
from selenium import webdriver


class WebTest:

    def setup(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/")
        self.driver.maximize_window()

    def execute(self) -> bool:
        # Implementation
        return True

    def teardown(self) -> None:
        self.driver.quit()


class APITest(WebTest):  # LSP violation, not need a driver
    def setup(self) -> None:
        raise NotImplementedError("API tests don't need browser setup")  # ❌  LSP violation

    def execute(self) -> Dict:  # ❌ The return is different
        return {"status": "success", "response": {}}

