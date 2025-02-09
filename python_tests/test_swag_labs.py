import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumHelper:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and return it"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def wait_for_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable and return it"""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))

@pytest.fixture
def driver():
    """Setup WebDriver before test and quit after test"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def take_screenshot(driver, name="screenshot"):
    """Helper function to take a screenshot"""
    driver.save_screenshot(f"{name}.png")

def test_login_add_to_cart_logout(driver):
    helper = SeleniumHelper(driver)

    try:
        # Step 1: Open the URL
        driver.get("https://www.saucedemo.com/")
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        print("Opened SauceDemo")

        # Step 2: Verify 'SWAG LABS' logo is present
        title_element = helper.wait_for_element(By.CLASS_NAME, "login_logo")
        assert title_element.is_displayed(), "SWAG LABS logo not found!"

        # Debugging: Take a screenshot before entering credentials
        take_screenshot(driver, "before_login")

        # Step 3: Enter Username & Password
        time.sleep(2)
        username = helper.wait_for_clickable(By.ID, "user-name")
        username.clear()
        username.send_keys("standard_user")

        password = helper.wait_for_clickable(By.ID, "password")
        password.clear()
        password.send_keys("secret_sauce")
        print("Entered credentials successfully.")

        # Step 4: Click Login Button
        login_button = helper.wait_for_clickable(By.ID, "login-button")
        driver.execute_script("arguments[0].click();", login_button)
        print("Clicked Login.")

        # Step 5: Check for login error message
        try:
            error_message = driver.find_element(By.CLASS_NAME, "error-message-container")
            if error_message.is_displayed():
                print(f"Login Failed: {error_message.text}")
                take_screenshot(driver, "login_error")
                raise Exception("Login failed! Check 'login_error.png' for details.")
        except Exception as e:
            print(f"No login error detected: {e}")

        # Step 6: Verify login success
        product_title = helper.wait_for_element(By.CLASS_NAME, "title")
        assert product_title.text == "Products", "Login Failed!"
        print("Login successful.")

        # Step 7: Add item to cart
        add_to_cart = helper.wait_for_clickable(By.ID, "add-to-cart-sauce-labs-backpack")
        add_to_cart.click()
        print("Item added to cart.")

        # Step 8: Open Cart
        cart_icon = helper.wait_for_clickable(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        print("Opened Cart.")

        # Step 9: Verify item is in cart
        cart_item = helper.wait_for_element(By.CLASS_NAME, "inventory_item_name")
        assert cart_item.text == "Sauce Labs Backpack", "Item not found in cart!"
        print("Item verified in cart.")

        # Step 10: Logout process
        menu_button = helper.wait_for_clickable(By.ID, "react-burger-menu-btn")
        menu_button.click()
        logout_button = helper.wait_for_clickable(By.ID, "logout_sidebar_link")
        logout_button.click()
        print("Logged out successfully.")

        # Step 11: Verify user is logged out
        helper.wait_for_element(By.ID, "login-button")
        print("Test Passed: User successfully logged out.")

    except Exception as e:
        print(f"Test failed: {e}")
        take_screenshot(driver, "failure_screenshot")
        raise
