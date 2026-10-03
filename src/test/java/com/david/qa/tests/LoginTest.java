package com.david.qa.tests;

import com.david.qa.pages.LoginPage;
import com.david.qa.pages.ProductsPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class LoginTest extends BaseTest {

    @Test(description = "TC-LOGIN-001: Login with valid credentials (TD-LOGIN-01)")
    public void standardUserCanLogin() {
        new LoginPage(driver).login("standard_user", "secret_sauce");

        ProductsPage productsPage = new ProductsPage(driver);
        productsPage.waitUntilLoaded();

        Assert.assertEquals(productsPage.getPath(), "/inventory.html",
                "Valid login should navigate to the inventory page.");
        Assert.assertEquals(productsPage.getTitle(), "Products",
                "The Products title should be displayed.");
        Assert.assertTrue(productsPage.getVisibleProductCount() > 0,
                "The product catalog should contain visible products.");
    }

    @Test(description = "TC-LOGIN-002: Login with an incorrect password (TD-LOGIN-02)")
    public void incorrectPasswordIsRejected() {
        LoginPage loginPage = new LoginPage(driver);
        loginPage.login("standard_user", "invalid_password");

        Assert.assertEquals(loginPage.getErrorMessage(),
                "Epic sadface: Username and password do not match any user in this service",
                "An incorrect password should produce a clear credentials error.");
        Assert.assertEquals(loginPage.getPath(), "/",
                "Rejected login should keep the user on the login page.");
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "The login form should remain visible after access is denied.");
    }

    @Test(description = "TC-LOGIN-003: Login with an unknown user (TD-LOGIN-03)")
    public void unknownUserIsRejected() {
        LoginPage loginPage = new LoginPage(driver);
        loginPage.login("non_existing_user", "secret_sauce");

        Assert.assertEquals(loginPage.getErrorMessage(),
                "Epic sadface: Username and password do not match any user in this service",
                "An unknown user should produce a clear credentials error.");
        Assert.assertEquals(loginPage.getPath(), "/",
                "Rejected login should keep the user on the login page.");
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "The login form should remain visible after access is denied.");
    }

    @Test(description = "TC-LOGIN-004: Login with a locked user (TD-LOGIN-04)")
    public void lockedUserIsRejected() {
        LoginPage loginPage = new LoginPage(driver);
        loginPage.login("locked_out_user", "secret_sauce");

        Assert.assertEquals(loginPage.getErrorMessage(),
                "Epic sadface: Sorry, this user has been locked out.",
                "A locked user should receive the specific locked-user message.");
        Assert.assertEquals(loginPage.getPath(), "/",
                "Rejected login should keep the user on the login page.");
        Assert.assertTrue(loginPage.isLoginFormDisplayed(),
                "The login form should remain visible after access is denied.");
    }
}
