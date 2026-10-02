package com.david.qa.pages;

import java.net.URI;
import java.math.BigDecimal;
import java.time.Duration;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.Select;

public class ProductsPage {
    private final WebDriver driver;
    private final WebDriverWait wait;
    private final By title = By.cssSelector("[data-test='title']");
    private final By productItems = By.cssSelector("[data-test='inventory-item']");
    private final By productName = By.cssSelector("[data-test='inventory-item-name']");
    private final By productDescription = By.cssSelector("[data-test='inventory-item-desc']");
    private final By productPrice = By.cssSelector("[data-test='inventory-item-price']");
    private final By productAction = By.cssSelector("button");
    private final By sortDropdown = By.cssSelector("[data-test='product-sort-container']");
    private final By addBackpackButton = By.id("add-to-cart-sauce-labs-backpack");
    private final By removeBackpackButton = By.id("remove-sauce-labs-backpack");
    private final By cartBadge = By.cssSelector("[data-test='shopping-cart-badge']");

    public ProductsPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void waitUntilLoaded() {
        wait.until(ExpectedConditions.urlContains("/inventory.html"));
        wait.until(ExpectedConditions.visibilityOfElementLocated(title));
        wait.until(ExpectedConditions.visibilityOfAllElementsLocatedBy(productItems));
    }

    public String getPath() {
        return URI.create(driver.getCurrentUrl()).getPath();
    }

    public String getTitle() {
        return driver.findElement(title).getText();
    }

    public int getVisibleProductCount() {
        return (int) driver.findElements(productItems).stream()
                .filter(element -> element.isDisplayed()).count();
    }

    public boolean areProductDetailsDisplayed() {
        List<WebElement> items = driver.findElements(productItems);
        return !items.isEmpty() && items.stream().allMatch(item -> {
            WebElement name = item.findElement(productName);
            WebElement description = item.findElement(productDescription);
            WebElement price = item.findElement(productPrice);
            WebElement action = item.findElement(productAction);
            return name.isDisplayed() && !name.getText().isBlank()
                    && description.isDisplayed() && !description.getText().isBlank()
                    && price.isDisplayed() && !price.getText().isBlank()
                    && action.isDisplayed() && action.isEnabled() && !action.getText().isBlank();
        });
    }

    public void sortByPriceLowToHigh() {
        WebElement dropdown = wait.until(ExpectedConditions.elementToBeClickable(sortDropdown));
        new Select(dropdown).selectByValue("lohi");
        wait.until(driver -> new Select(driver.findElement(sortDropdown))
                .getFirstSelectedOption().getAttribute("value").equals("lohi"));
    }

    public List<BigDecimal> getProductPrices() {
        return driver.findElements(productPrice).stream()
                .map(element -> new BigDecimal(element.getText().replace("$", "").trim()))
                .toList();
    }

    public void addBackpackToCart() {
        wait.until(ExpectedConditions.elementToBeClickable(addBackpackButton)).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(removeBackpackButton));
    }

    public String getBackpackActionText() {
        return driver.findElement(removeBackpackButton).getText();
    }

    public String getCartBadgeText() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(cartBadge)).getText();
    }
}
