package com.david.qa.listeners;

import com.david.qa.tests.BaseTest;
import io.qameta.allure.Allure;
import io.qameta.allure.AttachmentOptions;
import java.io.ByteArrayInputStream;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.IInvokedMethod;
import org.testng.IInvokedMethodListener;
import org.testng.ITestResult;

public final class FailureEvidenceListener implements IInvokedMethodListener {
    @Override
    public void afterInvocation(IInvokedMethod method, ITestResult result) {
        if (!method.isTestMethod() || result.getStatus() != ITestResult.FAILURE
                || !(result.getInstance() instanceof BaseTest test)) {
            return;
        }

        WebDriver driver = test.getDriver();
        if (driver == null) {
            return;
        }

        try {
            byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            Allure.attachment("Browser screenshot", "image/png",
                    new ByteArrayInputStream(screenshot), AttachmentOptions.withFileExtension(".png"));
        } catch (RuntimeException ignored) {
            // Evidence is best effort; preserve the original failure and still attempt the URL.
        }

        try {
            Allure.attachment("Current URL", "text/plain", driver.getCurrentUrl(),
                    AttachmentOptions.withFileExtension(".txt"));
        } catch (RuntimeException ignored) {
            // Evidence must not replace the original test failure or prevent browser cleanup.
        }
    }
}
