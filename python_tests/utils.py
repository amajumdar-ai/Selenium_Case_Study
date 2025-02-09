import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumHelper:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        """Wait until an element is visible and return it."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except Exception as e:
            print(f"Error: Element {value} not found using {by}. Exception: {e}")
            self.take_screenshot("error_wait_for_element")
            raise

    def click_element(self, by, value, timeout=10):
        """Click an element after waiting for it."""
        try:
            element = self.wait_for_element(by, value, timeout)
            element.click()
        except Exception as e:
            print(f"Error: Could not click element {value} using {by}. Exception: {e}")
            self.take_screenshot("error_click_element")
            raise

    def enter_text(self, by, value, text, timeout=10):
        """Clear and enter text in an input field."""
        try:
            element = self.wait_for_element(by, value, timeout)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            print(f"Error: Could not enter text in {value} using {by}. Exception: {e}")
            self.take_screenshot("error_enter_text")
            raise

    def take_screenshot(self, test_name):
        """Take a screenshot and save it in the 'screenshots' folder."""
        try:
            # Ensure the 'screenshots' folder exists
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")

            screenshot_path = f"screenshots/{test_name}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Error: Could not take screenshot. Exception: {e}")
