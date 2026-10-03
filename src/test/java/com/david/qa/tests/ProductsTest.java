package com.david.qa.tests;

import com.david.qa.pages.LoginPage;
import com.david.qa.pages.ProductsPage;
import java.math.BigDecimal;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class ProductsTest extends BaseTest {
    private ProductsPage productsPage;

    @BeforeMethod
    public void setUp() {
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
        List<BigDecimal> actualPrices = new WebDriverWait(driver, Duration.ofSeconds(10))
                .withMessage("The displayed product prices should reach ascending order after sorting.")
                .until(driver -> {
                    List<BigDecimal> prices = productsPage.getProductPrices();
                    List<BigDecimal> sortedPrices = new ArrayList<>(prices);
                    sortedPrices.sort(Comparator.naturalOrder());
                    return prices.size() > 1 && prices.equals(sortedPrices) ? prices : null;
                });
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
}
