package com.david.qa.tests;

import com.david.qa.pages.CartPage;
import com.david.qa.pages.CheckoutInformationPage;
import com.david.qa.pages.LoginPage;
import com.david.qa.pages.ProductsPage;
import java.math.BigDecimal;
import java.time.Duration;
import java.util.List;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class CartTest extends BaseTest {
    private CartPage cartPage;
    private BigDecimal backpackCatalogPrice;

    @BeforeMethod
    public void setUp() {
        new LoginPage(driver).login("standard_user", "secret_sauce");
        ProductsPage productsPage = new ProductsPage(driver);
        productsPage.waitUntilLoaded();
        backpackCatalogPrice = productsPage.getBackpackPrice();
        productsPage.addBackpackToCart();
        productsPage.openCart();
        cartPage = new CartPage(driver);
        cartPage.waitUntilLoaded();
    }

    @Test(description = "TC-CART-001: Verify an added product in the cart (TD-PROD-01)")
    public void cartContainsSelectedBackpack() {
        Assert.assertEquals(cartPage.getItemCount(), 1,
                "The cart should contain the one added product.");
        Assert.assertEquals(cartPage.getItemNames(), List.of("Sauce Labs Backpack"),
                "The cart should contain the selected backpack.");
        Assert.assertEquals(cartPage.getBackpackPrice(), backpackCatalogPrice,
                "The cart price should match the selected product's catalog price.");
    }

    @Test(description = "TC-CART-002: Remove a product from the cart (TD-PROD-01)")
    public void backpackCanBeRemovedFromCart() {
        cartPage.removeBackpack();
        new WebDriverWait(driver, Duration.ofSeconds(10))
                .withMessage("Removing the only product should leave an empty cart without a badge.")
                .until(driver -> cartPage.getItemCount() == 0 && !cartPage.isCartBadgeDisplayed());
        Assert.assertEquals(cartPage.getItemCount(), 0,
                "Removing the only product should leave the cart empty.");
        Assert.assertTrue(cartPage.getItemNames().isEmpty(),
                "The removed backpack should no longer be listed.");
        Assert.assertFalse(cartPage.isCartBadgeDisplayed(),
                "The cart badge should disappear when the cart is empty.");
    }

    @Test(description = "TC-CART-003: Continue from the cart to checkout (TD-PROD-01)")
    public void cartCanContinueToCheckoutInformation() {
        cartPage.continueToCheckout();
        CheckoutInformationPage checkoutPage = new CheckoutInformationPage(driver);
        checkoutPage.waitUntilLoaded();
        Assert.assertEquals(checkoutPage.getPath(), "/checkout-step-one.html",
                "Checkout should navigate to the information page.");
        Assert.assertEquals(checkoutPage.getTitle(), "Checkout: Your Information",
                "The checkout information title should be displayed.");
        Assert.assertTrue(checkoutPage.isInformationFormDisplayed(),
                "The checkout information fields should be visible.");
    }
}
