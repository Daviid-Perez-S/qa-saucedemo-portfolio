package com.david.qa.pages;

import java.math.BigDecimal;
import java.time.Duration;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class CartPage {
    private final WebDriver driver;
    private final WebDriverWait wait;
    private final By title = By.cssSelector("[data-test='title']");
    private final By cartItems = By.cssSelector(".cart_item");
    private final By itemNames = By.cssSelector("[data-test='inventory-item-name']");
    private final By itemPrice = By.cssSelector("[data-test='inventory-item-price']");
    private final By removeBackpackButton = By.id("remove-sauce-labs-backpack");
    private final By cartBadge = By.cssSelector("[data-test='shopping-cart-badge']");
    private final By checkoutButton = By.id("checkout");

    public CartPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void waitUntilLoaded() {
        wait.until(ExpectedConditions.urlContains("/cart.html"));
        wait.until(ExpectedConditions.visibilityOfElementLocated(title));
        wait.until(ExpectedConditions.elementToBeClickable(checkoutButton));
    }

    public int getItemCount() {
        return driver.findElements(cartItems).size();
    }

    public List<String> getItemNames() {
        return driver.findElements(itemNames).stream().map(element -> element.getText()).toList();
    }

    public BigDecimal getBackpackPrice() {
        return driver.findElements(cartItems).stream()
                .filter(item -> item.findElement(itemNames).getText().equals("Sauce Labs Backpack"))
                .map(item -> new BigDecimal(item.findElement(itemPrice).getText().replace("$", "").trim()))
                .findFirst().orElseThrow(() -> new IllegalStateException("Backpack not found in the cart."));
    }

    public void removeBackpack() {
        wait.until(ExpectedConditions.elementToBeClickable(removeBackpackButton)).click();
        wait.until(ExpectedConditions.invisibilityOfElementLocated(removeBackpackButton));
    }

    public boolean isCartBadgeDisplayed() {
        return driver.findElements(cartBadge).stream().anyMatch(element -> element.isDisplayed());
    }

    public void continueToCheckout() {
        wait.until(ExpectedConditions.elementToBeClickable(checkoutButton)).click();
    }
}
