package com.david.qa.pages;

import java.net.URI;
import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class CheckoutCompletePage {
    private final WebDriver driver;
    private final WebDriverWait wait;
    private final By title = By.cssSelector("[data-test='title']");
    private final By confirmationHeader = By.cssSelector("[data-test='complete-header']");
    private final By menuButton = By.id("react-burger-menu-btn");
    private final By logoutLink = By.id("logout_sidebar_link");

    public CheckoutCompletePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void waitUntilLoaded() {
        wait.until(ExpectedConditions.urlContains("/checkout-complete.html"));
        wait.until(ExpectedConditions.visibilityOfElementLocated(title));
        wait.until(ExpectedConditions.visibilityOfElementLocated(confirmationHeader));
    }

    public String getPath() {
        return URI.create(driver.getCurrentUrl()).getPath();
    }

    public String getTitle() {
        return driver.findElement(title).getText();
    }

    public String getConfirmationHeader() {
        return driver.findElement(confirmationHeader).getText();
    }

    public void logout() {
        wait.until(ExpectedConditions.elementToBeClickable(menuButton)).click();
        wait.until(ExpectedConditions.elementToBeClickable(logoutLink)).click();
    }
}
