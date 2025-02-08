package com.selenium.testcases;

import org.testng.annotations.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.AfterMethod;
import com.selenium.utilities.BaseTest;
import com.selenium.utilities.ScreenshotUtil;
import org.testng.annotations.Parameters;

public class LoginTest extends BaseTest { // ✅ Extends BaseTest

    @BeforeMethod
    public void openLoginPage() {
        driver.get(baseUrl);  // ✅ Reuse the base URL from BaseTest
    }
public void clearField(WebElement element) {
    element.clear();
}   
    @Test
    @Parameters({"validUsername", "validPassword"})
    public void testValidLogin(String username, String password) {
        WebElement usernameField = driver.findElement(By.id("user-name"));
        WebElement passwordField = driver.findElement(By.id("password"));

        clearField(usernameField);
        clearField(passwordField);

        usernameField.sendKeys(username);
        passwordField.sendKeys(password);
        driver.findElement(By.id("login-button")).click();

        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.urlContains("inventory.html"));

        String expectedUrl = "https://www.saucedemo.com/inventory.html";
        Assert.assertEquals(driver.getCurrentUrl(), expectedUrl, "User is NOT on the expected page!");

        // ✅ Verify title of the page
        String expectedTitle = "Swag Labs";
        Assert.assertEquals(driver.getTitle(), expectedTitle, "Title does not match expected value!");


        // ✅ Capture Screenshot for Report
        ScreenshotUtil.captureScreenshot(driver, "ValidLogin");
    }

     @Test
    @Parameters({"invalidUsername", "invalidPassword"})
    public void testInvalidLogin(String username, String password) {
        WebElement usernameField = driver.findElement(By.id("user-name"));
        WebElement passwordField = driver.findElement(By.id("password"));

        // Ensure fields are cleared before entering new values
        clearField(usernameField);
        clearField(passwordField);

        usernameField.sendKeys(username);
        passwordField.sendKeys(password);
        driver.findElement(By.id("login-button")).click();

        // ✅ Verify user is NOT navigated to the correct page
        String unexpectedUrl = "https://www.saucedemo.com/inventory.html";
        Assert.assertNotEquals(driver.getCurrentUrl(), unexpectedUrl, "User should NOT be on the inventory page!");

        // ✅ Verify the title of the page remains the same (login page)
        String expectedTitle = "Swag Labs";
        Assert.assertEquals(driver.getTitle(), expectedTitle, "Title should remain the same on failed login!");

        // ✅ Validate error message is displayed
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
        WebElement errorMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("h3[data-test='error']")));
        Assert.assertTrue(errorMessage.isDisplayed(), "Expected error message not displayed for invalid login");

         ScreenshotUtil.captureScreenshot(driver, "InvalidLogin");
    }

    @AfterMethod
    public void cleanUp() {
        driver.manage().deleteAllCookies();
    }
}
