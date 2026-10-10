package com.david.qa.tests.accessibility;

import com.david.qa.accessibility.AccessibilityAudit;
import com.david.qa.pages.LoginPage;
import com.david.qa.pages.ProductsPage;
import com.david.qa.pages.CartPage;
import com.david.qa.pages.CheckoutInformationPage;
import com.david.qa.pages.CheckoutOverviewPage;
import com.david.qa.pages.CheckoutCompletePage;
import com.david.qa.tests.BaseTest;
import java.time.Duration;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.Test;

public class AccessibilityTest extends BaseTest {
    @Test(description = "A11Y-AUTO-001: Login accessibility (2 required scans)")
    public void auditLogin() {
        AccessibilityAudit audit = new AccessibilityAudit(driver, "A11Y-AUTO-001",
                "login-initial", "login-invalid-credentials");
        LoginPage login = new LoginPage(driver);
        audit.scan("login-initial", () -> {
            login.waitUntilLoaded();
            require(login.isLoginFormDisplayed(), "Initial login form missing");
        });
        audit.scan("login-invalid-credentials", () -> {
            login.waitUntilLoaded();
            login.login("standard_user", "invalid_password");
            new WebDriverWait(driver, Duration.ofSeconds(10)).until(d -> login.getErrorMessage()
                    .equals("Epic sadface: Username and password do not match any user in this service"));
            require(login.getPath().equals("/") && login.isLoginFormDisplayed(), "Invalid-credential state missing");
        });
        audit.finish();
    }

    @Test(description = "A11Y-AUTO-002: Products accessibility (3 required scans)")
    public void auditProducts() {
        AccessibilityAudit audit = new AccessibilityAudit(driver, "A11Y-AUTO-002",
                "products-initial", "products-product-added", "products-menu-open");
        ProductsPage products = new ProductsPage(driver);
        audit.scan("products-initial", () -> {
            loginToProducts();
            require(products.areProductDetailsDisplayed(), "Product catalog not ready");
            require(driver.findElements(org.openqa.selenium.By.cssSelector("[data-test='shopping-cart-badge']")).isEmpty(), "Initial cart is not empty");
        });
        audit.scan("products-product-added", () -> {
            products.waitUntilLoaded();
            products.addBackpackToCart();
            require(products.getBackpackActionText().equals("Remove") && products.getCartBadgeText().equals("1"), "Product-added state missing");
        });
        audit.scan("products-menu-open", () -> {
            products.waitUntilLoaded();
            require(products.getCartBadgeText().equals("1"), "Product missing before menu scan");
            products.openMenu();
        });
        audit.finish();
    }

    @Test(description = "A11Y-AUTO-003: Cart accessibility (2 required scans)")
    public void auditCart() {
        AccessibilityAudit audit = new AccessibilityAudit(driver, "A11Y-AUTO-003", "cart-with-product", "cart-empty");
        CartPage cart = new CartPage(driver);
        audit.scan("cart-with-product", () -> {
            prepareCart();
            require(cart.getItemCount() == 1 && cart.getItemNames().equals(java.util.List.of("Sauce Labs Backpack")), "Cart product missing");
        });
        audit.scan("cart-empty", () -> {
            cart.waitUntilLoaded();
            cart.removeBackpack();
            new WebDriverWait(driver, Duration.ofSeconds(10)).until(d -> cart.getItemCount() == 0 && !cart.isCartBadgeDisplayed());
        });
        audit.finish();
    }

    @Test(description = "A11Y-AUTO-004: Checkout Information accessibility (4 required scans)")
    public void auditCheckoutInformation() {
        AccessibilityAudit audit = new AccessibilityAudit(driver, "A11Y-AUTO-004", "checkout-information-initial",
                "checkout-error-first-name", "checkout-error-last-name", "checkout-error-postal-code");
        CheckoutInformationPage checkout = new CheckoutInformationPage(driver);
        audit.scan("checkout-information-initial", () -> {
            prepareCheckout();
            require(checkout.isInformationFormDisplayed(), "Checkout form missing");
        });
        audit.scan("checkout-error-first-name", () -> missingField(checkout, "", "Pérez", "01000", "Error: First Name is required"));
        audit.scan("checkout-error-last-name", () -> missingField(checkout, "David", "", "01000", "Error: Last Name is required"));
        audit.scan("checkout-error-postal-code", () -> missingField(checkout, "David", "Pérez", "", "Error: Postal Code is required"));
        audit.finish();
    }

    @Test(description = "A11Y-AUTO-005: Checkout Overview accessibility (1 required scan)")
    public void auditCheckoutOverview() {
        AccessibilityAudit audit = new AccessibilityAudit(driver, "A11Y-AUTO-005", "checkout-overview");
        audit.scan("checkout-overview", this::prepareOverview);
        audit.finish();
    }

    @Test(description = "A11Y-AUTO-006: Checkout Complete accessibility (1 required scan)")
    public void auditCheckoutComplete() {
        AccessibilityAudit audit = new AccessibilityAudit(driver, "A11Y-AUTO-006", "checkout-complete");
        audit.scan("checkout-complete", () -> {
            prepareOverview();
            new CheckoutOverviewPage(driver).finishOrder();
            CheckoutCompletePage complete = new CheckoutCompletePage(driver);
            complete.waitUntilLoaded();
            require(complete.getPath().equals("/checkout-complete.html")
                    && complete.getConfirmationHeader().equals("Thank you for your order!"), "Completion state missing");
        });
        audit.finish();
    }

    private void loginToProducts() {
        LoginPage login = new LoginPage(driver);
        login.waitUntilLoaded();
        login.login("standard_user", "secret_sauce");
        new ProductsPage(driver).waitUntilLoaded();
    }

    private void prepareCart() {
        loginToProducts();
        ProductsPage products = new ProductsPage(driver);
        products.addBackpackToCart();
        require(products.getCartBadgeText().equals("1"), "Expected one cart product");
        products.openCart();
        new CartPage(driver).waitUntilLoaded();
    }

    private void prepareCheckout() {
        prepareCart();
        new CartPage(driver).continueToCheckout();
        new CheckoutInformationPage(driver).waitUntilLoaded();
    }

    private void prepareOverview() {
        prepareCheckout();
        CheckoutInformationPage checkout = new CheckoutInformationPage(driver);
        checkout.fillInformation("David", "Pérez", "01000");
        checkout.clickContinue();
        CheckoutOverviewPage overview = new CheckoutOverviewPage(driver);
        overview.waitUntilLoaded();
        require(overview.getItemNames().equals(java.util.List.of("Sauce Labs Backpack"))
                && overview.getTotalText().startsWith("Total: $"), "Overview contents missing");
    }

    private void missingField(CheckoutInformationPage checkout, String first, String last, String postal, String error) {
        checkout.waitUntilLoaded();
        checkout.fillInformation(first, last, postal);
        checkout.clickContinue();
        checkout.waitForErrorMessage(error);
        require(checkout.getPath().equals("/checkout-step-one.html") && checkout.isInformationFormDisplayed(), "Required-field state missing");
    }

    private void require(boolean condition, String message) {
        if (!condition) throw new IllegalStateException(message);
    }
}
