package com.selenium.utilities;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import java.io.File;
import java.io.IOException;

public class ScreenshotUtil {
    public static void captureScreenshot(WebDriver driver, String testName) {
        try {
            File screenshotDir = new File("screenshots/");
            if (!screenshotDir.exists()) {
                screenshotDir.mkdirs();  // ✅ Create directory if not present
            }

            File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            FileUtils.copyFile(src, new File(screenshotDir + "/" + testName + ".png"));

            System.out.println("Screenshot saved: " + testName);
        } catch (IOException e) {
            System.out.println("Screenshot capture failed: " + e.getMessage());
        }
    }
}
