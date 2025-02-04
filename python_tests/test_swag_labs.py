import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

def test_login_add_to_cart_logout(driver):
    helper = SeleniumHelper(driver)

    # Step 1: Open the URL
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    print("Opened SauceDemo")

    # Step 2: Verify 'SWAG LABS' logo is present
    title_element = helper.wait_for_element(By.CLASS_NAME, "app_logo")
    assert title_element.is_displayed(), "SWAG LABS logo not found!"

    # Debugging: Take a screenshot before entering credentials
    driver.save_screenshot("before_login.png")

    # Step 3: Wait for Username & Password fields, clear them, and enter credentials
    time.sleep(2)  # Ensures elements are fully loaded
    username = helper.wait_for_clickable(By.ID, "user-name")
    username.click()
    username.clear()
    username.send_keys("standard_user")

    password = helper.wait_for_clickable(By.ID, "password")
    password.click()
    password.clear()
    password.send_keys("secret_sauce")
    
    print("Entered credentials successfully.")

    # Step 4: Click Login Button (Try JavaScript Click if Needed)
    login_button = helper.wait_for_clickable(By.ID, "login-button")
    driver.execute_script("arguments[0].click();", login_button)
    print("Clicked Login.")

    # Step 5: Check for login error message
    try:
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container")
        if error_message.is_displayed():
            print(f"Login Failed: {error_message.text}")
            driver.save_screenshot("login_error.png")
            raise Exception("Login failed! Check 'login_error.png' for details.")
    except:
        print("No login error detected, proceeding...")

    # Step 6: Verify login success by checking 'Products' title
    product_title = helper.wait_for_element(By.CLASS_NAME, "title")
    assert product_title.text == "Products", "Login Failed!"
    print("Login successful.")

    # Step 7: Add item to cart
    add_to_cart = helper.wait_for_clickable(By.ID, "add-to-cart-sauce-labs-backpack")
    add_to_cart.click()
    print("Item added to cart.")

    # Step 8: Click on Cart Icon
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
