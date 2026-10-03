package com.david.qa.tests;

import com.david.qa.driver.DriverFactory;
import com.david.qa.pages.CartPage;
import com.david.qa.pages.CheckoutCompletePage;
import com.david.qa.pages.CheckoutInformationPage;
import com.david.qa.pages.CheckoutOverviewPage;
import com.david.qa.pages.LoginPage;
import com.david.qa.pages.ProductsPage;
import java.util.List;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class EndToEndTest {
    private WebDriver driver;

    @BeforeMethod
    public void setUp() {
        driver = DriverFactory.createChromeDriver();
        driver.get("https://www.saucedemo.com/");
    }

    @Test(description = "TC-E2E-001: Complete a purchase and log out (TD-LOGIN-01, TD-PROD-01, TD-CHECK-01)")
    public void userCanCompletePurchaseAndLogout() {
        LoginPage loginPage = new LoginPage(driver);
        loginPage.login("standard_user", "secret_sauce");
        ProductsPage productsPage = new ProductsPage(driver);
        productsPage.waitUntilLoaded();
        Assert.assertTrue(productsPage.getVisibleProductCount() > 0,
                "The user should see the product catalog after login.");
        productsPage.addBackpackToCart();
        productsPage.openCart();

        CartPage cartPage = new CartPage(driver);
        cartPage.waitUntilLoaded();
        Assert.assertEquals(cartPage.getItemNames(), List.of("Sauce Labs Backpack"),
                "The cart should contain the selected backpack before checkout.");
        cartPage.continueToCheckout();
        CheckoutInformationPage informationPage = new CheckoutInformationPage(driver);
        informationPage.waitUntilLoaded();
        informationPage.fillInformation("David", "Pérez", "01000");
        informationPage.continueToOverview();

        CheckoutOverviewPage overviewPage = new CheckoutOverviewPage(driver);
        overviewPage.waitUntilLoaded();
        Assert.assertEquals(overviewPage.getItemNames(), List.of("Sauce Labs Backpack"),
                "The order overview should contain the selected backpack.");
        overviewPage.finishOrder();
        CheckoutCompletePage completePage = new CheckoutCompletePage(driver);
        completePage.waitUntilLoaded();
        Assert.assertEquals(completePage.getPath(), "/checkout-complete.html",
                "The purchase should reach the order confirmation page.");
        Assert.assertEquals(completePage.getConfirmationHeader(), "Thank you for your order!",
                "The order confirmation should be displayed before logout.");

        completePage.logout();
        loginPage.waitUntilLoaded();
        Assert.assertEquals(loginPage.getPath(), "/",
                "Logout should return the user to the login page.");
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "The login form should be displayed after logout.");
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
