package com.david.qa.tests;

import com.david.qa.driver.DriverFactory;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

public abstract class BaseTest {
    protected WebDriver driver;

    public final WebDriver getDriver() {
        return driver;
    }

    @BeforeMethod
    public void openBrowser() {
        driver = DriverFactory.createChromeDriver();
        driver.get("https://www.saucedemo.com/");
    }

    @AfterMethod(alwaysRun = true)
    public void closeBrowser() {
        try {
            if (driver != null) {
                driver.quit();
            }
        } finally {
            driver = null;
        }
    }
}
