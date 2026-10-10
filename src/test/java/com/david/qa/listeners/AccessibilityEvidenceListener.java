package com.david.qa.listeners;

import com.david.qa.accessibility.AccessibilityAudit;
import com.deque.html.axecore.selenium.AxeReporter;
import io.qameta.allure.Allure;
import io.qameta.allure.AttachmentOptions;
import java.util.Map;
import org.testng.IInvokedMethod;
import org.testng.IInvokedMethodListener;
import org.testng.ITestResult;

public final class AccessibilityEvidenceListener implements IInvokedMethodListener {
    @Override
    public void afterInvocation(IInvokedMethod method, ITestResult result) {
        if (!method.isTestMethod() || !(result.getAttribute(AccessibilityAudit.RESULT_ATTRIBUTE)
                instanceof AccessibilityAudit audit)) return;
        if (!audit.isFinished()) {
            Throwable original = result.getThrowable();
            if (original != null) audit.recordUnexpected(original);
            try {
                audit.finish();
            } catch (RuntimeException | AssertionError decision) {
                // A violation stays primary in mixed failures; the unexpected exception remains in its trace.
                if (original == null || audit.violationCount() > 0) result.setThrowable(decision);
                result.setStatus(ITestResult.FAILURE);
            }
        }
        // Always attempt each available scan and the manifest independently.
        for (Map<String, Object> scan : audit.scanEvidence()) {
            attach(scan.get("caseId") + " / " + scan.get("stateKey"), scan, result);
        }
        attach("Accessibility manifest", audit.manifest(), result);
    }

    private void attach(String name, Object evidence, ITestResult result) {
        try {
            Allure.attachment(name, "application/json", AxeReporter.serialize(evidence),
                    AttachmentOptions.withFileExtension(".json"));
        } catch (RuntimeException exception) {
            ((AccessibilityAudit) result.getAttribute(AccessibilityAudit.RESULT_ATTRIBUTE)).recordEvidenceError(exception);
            // Preserve the original failure; evidence errors must not turn a failed scan into success.
            if (result.getThrowable() != null) result.getThrowable().addSuppressed(exception);
            else {
                result.setThrowable(new IllegalStateException("Cannot retain accessibility evidence: " + name, exception));
                result.setStatus(ITestResult.FAILURE);
            }
        }
    }
}
