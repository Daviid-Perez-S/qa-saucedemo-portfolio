package com.david.qa.tests;

import com.david.qa.pages.LoginPage;
import com.david.qa.pages.ProductsPage;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class LoginTest {
    private WebDriver driver;

    @BeforeMethod
    public void setUp() {
        driver = new ChromeDriver();
        driver.get("https://www.saucedemo.com/");
    }

    @Test(description = "TC-LOGIN-001: Login with valid credentials (TD-LOGIN-01)")
    public void standardUserCanLogin() {
        new LoginPage(driver).login("standard_user", "secret_sauce");

        ProductsPage productsPage = new ProductsPage(driver);
        productsPage.waitUntilLoaded();

        Assert.assertEquals(productsPage.getPath(), "/inventory.html",
                "Valid login should navigate to the inventory page.");
        Assert.assertEquals(productsPage.getTitle(), "Products",
                "The Products title should be displayed.");
        Assert.assertTrue(productsPage.getVisibleProductCount() > 0,
                "The product catalog should contain visible products.");
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
