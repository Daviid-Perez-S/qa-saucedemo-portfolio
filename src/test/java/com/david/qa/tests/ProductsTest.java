package com.david.qa.tests;

import com.david.qa.pages.LoginPage;
import com.david.qa.pages.ProductsPage;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class ProductsTest {
    private WebDriver driver;
    private ProductsPage productsPage;

    @BeforeMethod
    public void setUp() {
        driver = new ChromeDriver();
        driver.get("https://www.saucedemo.com/");
        new LoginPage(driver).login("standard_user", "secret_sauce");
        productsPage = new ProductsPage(driver);
        productsPage.waitUntilLoaded();
    }

    @Test(description = "TC-PROD-001: View the product catalog (TD-LOGIN-01)")
    public void catalogDisplaysProductDetails() {
        Assert.assertEquals(productsPage.getTitle(), "Products",
                "The catalog should be displayed on Products.");
        Assert.assertTrue(productsPage.getVisibleProductCount() > 0,
                "The catalog should contain visible products.");
        Assert.assertTrue(productsPage.areProductDetailsDisplayed(),
                "Each product should have a visible name, description, price, and available action.");
    }

    @Test(description = "TC-PROD-002: Sort products by price, low to high")
    public void productsCanBeSortedByAscendingPrice() {
        productsPage.sortByPriceLowToHigh();
        List<BigDecimal> actualPrices = productsPage.getProductPrices();
        Assert.assertTrue(actualPrices.size() > 1,
                "At least two prices are needed to check ordering.");

        List<BigDecimal> expectedPrices = new ArrayList<>(actualPrices);
        expectedPrices.sort(Comparator.naturalOrder());
        Assert.assertEquals(actualPrices, expectedPrices,
                "Displayed product prices should be in ascending order.");
    }

    @Test(description = "TC-PROD-003: Add a product to the cart (TD-PROD-01)")
    public void backpackCanBeAddedToCart() {
        productsPage.addBackpackToCart();
        Assert.assertEquals(productsPage.getBackpackActionText(), "Remove",
                "The selected backpack should offer removal after being added.");
        Assert.assertEquals(productsPage.getCartBadgeText(), "1",
                "Adding the backpack should show one item in the cart badge.");
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
