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

public class CheckoutTest {
    private WebDriver driver;
    private CheckoutInformationPage checkoutPage;

    @BeforeMethod
    public void setUp() {
        driver = DriverFactory.createChromeDriver();
        driver.get("https://www.saucedemo.com/");
        new LoginPage(driver).login("standard_user", "secret_sauce");
        ProductsPage productsPage = new ProductsPage(driver);
        productsPage.waitUntilLoaded();
        productsPage.addBackpackToCart();
        productsPage.openCart();
        CartPage cartPage = new CartPage(driver);
        cartPage.waitUntilLoaded();
        cartPage.continueToCheckout();
        checkoutPage = new CheckoutInformationPage(driver);
        checkoutPage.waitUntilLoaded();
    }

    @Test(description = "TC-CHECK-001: Complete checkout with valid information (TD-CHECK-01)")
    public void validInformationCompletesCheckout() {
        checkoutPage.fillInformation("David", "Pérez", "01000");
        checkoutPage.continueToOverview();
        CheckoutOverviewPage overviewPage = new CheckoutOverviewPage(driver);
        overviewPage.waitUntilLoaded();
        Assert.assertEquals(overviewPage.getTitle(), "Checkout: Overview",
                "Valid information should navigate to the checkout overview.");
        Assert.assertEquals(overviewPage.getItemNames(), List.of("Sauce Labs Backpack"),
                "The overview should show the selected product.");
        Assert.assertFalse(overviewPage.getTotalText().isBlank(),
                "The order total should be displayed before finishing.");

        overviewPage.finishOrder();
        CheckoutCompletePage completePage = new CheckoutCompletePage(driver);
        completePage.waitUntilLoaded();
        Assert.assertEquals(completePage.getPath(), "/checkout-complete.html",
                "Finishing checkout should navigate to the order confirmation.");
        Assert.assertEquals(completePage.getTitle(), "Checkout: Complete!",
                "The checkout completion title should be displayed.");
        Assert.assertEquals(completePage.getConfirmationHeader(), "Thank you for your order!",
                "The order confirmation message should be displayed.");
    }

    @Test(description = "TC-CHECK-002: Validate missing first name (TD-CHECK-02)")
    public void missingFirstNameBlocksCheckout() {
        checkoutPage.fillInformation("", "Pérez", "01000");
        checkoutPage.continueToOverview();
        assertCheckoutBlocked("Error: First Name is required");
    }

    @Test(description = "TC-CHECK-003: Validate missing last name (TD-CHECK-02)")
    public void missingLastNameBlocksCheckout() {
        checkoutPage.fillInformation("David", "", "01000");
        checkoutPage.continueToOverview();
        assertCheckoutBlocked("Error: Last Name is required");
    }

    @Test(description = "TC-CHECK-004: Validate missing postal code (TD-CHECK-02)")
    public void missingPostalCodeBlocksCheckout() {
        checkoutPage.fillInformation("David", "Pérez", "");
        checkoutPage.continueToOverview();
        assertCheckoutBlocked("Error: Postal Code is required");
    }

    private void assertCheckoutBlocked(String expectedError) {
        Assert.assertEquals(checkoutPage.getErrorMessage(), expectedError,
                "The validation message should identify the missing required field.");
        Assert.assertEquals(checkoutPage.getPath(), "/checkout-step-one.html",
                "Invalid information should keep the user on checkout information.");
        Assert.assertTrue(checkoutPage.isInformationFormDisplayed(),
                "The information form should remain visible after validation fails.");
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
