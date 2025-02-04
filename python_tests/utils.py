from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumHelper:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        """Wait until an element is visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def click_element(self, by, value):
        """Click an element after waiting for it."""
        self.wait_for_element(by, value).click()

    def enter_text(self, by, value, text):
        """Clear and enter text in an input field."""
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)

    def take_screenshot(self, test_name):
        """Take a screenshot and save it in screenshots folder."""
        self.driver.save_screenshot(f"screenshots/{test_name}.png")
