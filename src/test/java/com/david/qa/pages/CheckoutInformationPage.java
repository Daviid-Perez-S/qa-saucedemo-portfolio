package com.david.qa.pages;

import java.net.URI;
import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class CheckoutInformationPage {
    private final WebDriver driver;
    private final WebDriverWait wait;
    private final By title = By.cssSelector("[data-test='title']");
    private final By firstNameInput = By.id("first-name");
    private final By lastNameInput = By.id("last-name");
    private final By postalCodeInput = By.id("postal-code");

    public CheckoutInformationPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void waitUntilLoaded() {
        wait.until(ExpectedConditions.urlContains("/checkout-step-one.html"));
        wait.until(ExpectedConditions.visibilityOfElementLocated(title));
        wait.until(ExpectedConditions.visibilityOfElementLocated(firstNameInput));
        wait.until(ExpectedConditions.visibilityOfElementLocated(lastNameInput));
        wait.until(ExpectedConditions.visibilityOfElementLocated(postalCodeInput));
    }

    public String getPath() {
        return URI.create(driver.getCurrentUrl()).getPath();
    }

    public String getTitle() {
        return driver.findElement(title).getText();
    }

    public boolean isInformationFormDisplayed() {
        return driver.findElement(firstNameInput).isDisplayed()
                && driver.findElement(lastNameInput).isDisplayed()
                && driver.findElement(postalCodeInput).isDisplayed();
    }
}
