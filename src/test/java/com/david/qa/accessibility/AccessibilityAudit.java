package com.david.qa.accessibility;

import com.deque.html.axecore.args.AxeRuleOptions;
import com.deque.html.axecore.args.AxeRunOnlyOptions;
import com.deque.html.axecore.args.AxeRunOptions;
import com.deque.html.axecore.results.Results;
import com.deque.html.axecore.results.Rule;
import com.deque.html.axecore.selenium.AxeBuilder;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import org.openqa.selenium.HasCapabilities;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.ITestResult;
import org.testng.Reporter;

/** One method's required states, scan results and final decision; no Allure calls. */
public final class AccessibilityAudit {
    public static final String RESULT_ATTRIBUTE = AccessibilityAudit.class.getName();
    private static final List<String> TAGS = List.of("wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa");
    private static final List<String> EXPERIMENTAL = List.of("css-orientation-lock", "label-content-name-mismatch",
            "p-as-heading", "table-fake-caption", "td-has-header");
    private static final List<String> RESULT_TYPES = List.of("violations", "passes", "incomplete", "inapplicable");
    private final WebDriver driver;
    private final String caseId;
    private final String runId;
    private final String startedAt = Instant.now().toString();
    private final Map<String, Map<String, Object>> states = new LinkedHashMap<>();
    private final List<Throwable> errors = new ArrayList<>();
    private List<?> inventory = List.of();
    private boolean finished;
    private String lastVerifiedState;

    public AccessibilityAudit(WebDriver driver, String caseId, String... requiredStates) {
        if (requiredStates.length == 0 || new LinkedHashSet<>(List.of(requiredStates)).size() != requiredStates.length) {
            throw new IllegalArgumentException("Required scan states must be nonempty and unique");
        }
        this.driver = driver;
        this.caseId = caseId;
        ITestResult result = Reporter.getCurrentTestResult();
        Object existing = result.getTestContext().getAttribute(RESULT_ATTRIBUTE + ".runId");
        runId = existing == null ? UUID.randomUUID().toString() : existing.toString();
        result.getTestContext().setAttribute(RESULT_ATTRIBUTE + ".runId", runId);
        result.setAttribute(RESULT_ATTRIBUTE, this);
        for (String key : requiredStates) {
            Map<String, Object> state = new LinkedHashMap<>();
            state.put("stateKey", key);
            state.put("preparationCompleted", false);
            state.put("executionStatus", "Not Executed");
            states.put(key, state);
        }
    }

    public void scan(String stateKey, Runnable prepareAndVerify) {
        Map<String, Object> state = states.get(stateKey);
        if (state == null || !state.get("executionStatus").equals("Not Executed")) {
            throw new IllegalArgumentException("Unknown or repeated required state: " + stateKey);
        }
        String stage = "preparation";
        state.put("startedAt", Instant.now().toString());
        try {
            prepareAndVerify.run();
            waitForRendering();
            state.put("preparationCompleted", true);
            lastVerifiedState = stateKey;
            state.put("url", driver.getCurrentUrl());
            state.put("environment", environment());
            stage = "axe execution / integrity";
            Duration scriptTimeout = driver.manage().timeouts().getScriptTimeout();
            Duration pageTimeout = driver.manage().timeouts().getPageLoadTimeout();
            Results results;
            Throwable original = null;
            try {
                AxeBuilder builder = new AxeBuilder().withOptions(options()).setTimeout(30);
                builder.setInjectAxe(this::verifyEngine);
                results = builder.analyze(driver);
                // Retain even invalid/error results for diagnosis; never reinterpret them as empty success.
                if (results != null) state.put("axe", results);
                validate(results);
            } catch (RuntimeException | Error exception) {
                original = exception;
                throw exception;
            } finally {
                RuntimeException restoration = null;
                try { driver.manage().timeouts().scriptTimeout(scriptTimeout); }
                catch (RuntimeException exception) { restoration = exception; }
                try { driver.manage().timeouts().pageLoadTimeout(pageTimeout); }
                catch (RuntimeException exception) {
                    if (restoration == null) restoration = exception;
                    else restoration.addSuppressed(exception);
                }
                if (restoration != null) {
                    if (original != null) original.addSuppressed(restoration);
                    else throw restoration;
                }
            }
            state.put("executionStatus", "Completed");
            state.put("incompleteReviewStatus", results.getIncomplete().isEmpty() ? "Not Required" : "Pending");
        } catch (RuntimeException exception) {
            state.put("executionStatus", "Technical Error");
            state.put("technicalError", error(stage, exception));
            errors.add(exception);
        } finally {
            state.put("finishedAt", Instant.now().toString());
        }
    }

    private AxeRunOptions options() {
        AxeRunOnlyOptions runOnly = new AxeRunOnlyOptions();
        runOnly.setType("tag");
        runOnly.setValues(TAGS);
        AxeRunOptions options = new AxeRunOptions();
        options.setRunOnly(runOnly);
        options.setResultTypes(RESULT_TYPES);
        Map<String, AxeRuleOptions> rules = new LinkedHashMap<>();
        List<String> enabled = new ArrayList<>(EXPERIMENTAL);
        enabled.add("target-size");
        for (String id : enabled) {
            AxeRuleOptions rule = new AxeRuleOptions();
            rule.setEnabled(true);
            rules.put(id, rule);
        }
        options.setRules(rules);
        return options;
    }

    private void verifyEngine(WebDriver browser) {
        JavascriptExecutor js = (JavascriptExecutor) browser;
        String version = String.valueOf(js.executeScript("return axe.version"));
        if (!version.equals("4.13.0")) throw new IllegalStateException("Unexpected axe engine: " + version);
        inventory = (List<?>) js.executeScript("return axe.getRules().map(r => ({id:r.ruleId,tags:r.tags}))");
        Set<String> ids = new LinkedHashSet<>();
        for (Object entry : inventory) ids.add(String.valueOf(((Map<?, ?>) entry).get("id")));
        for (String id : options().getRules().keySet()) {
            if (!ids.contains(id)) throw new IllegalStateException("Required axe rule unavailable: " + id);
        }
    }

    private void validate(Results results) {
        if (results == null) throw new IllegalStateException("axe returned no results");
        if (results.isErrored()) throw new IllegalStateException("axe execution failed", results.getError());
        if (results.getTestEngine() == null || !"4.13.0".equals(results.getTestEngine().getVersion())
                || results.getUrl() == null || !results.getUrl().equals(driver.getCurrentUrl())
                || results.getTimestamp() == null || results.getViolations() == null || results.getPasses() == null
                || results.getIncomplete() == null || results.getInapplicable() == null) {
            throw new IllegalStateException("Invalid axe result envelope");
        }
        Set<String> returned = new LinkedHashSet<>();
        for (List<Rule> rules : List.of(results.getViolations(), results.getPasses(),
                results.getIncomplete(), results.getInapplicable())) {
            Set<String> categoryIds = new LinkedHashSet<>();
            for (Rule rule : rules) {
                if (rule == null || rule.getId() == null || rule.getTags() == null || rule.getNodes() == null
                        || !categoryIds.add(rule.getId())) throw new IllegalStateException("Invalid/duplicate rule result within category");
                returned.add(rule.getId());
            }
        }
        for (Object entry : inventory) {
            Map<?, ?> rule = (Map<?, ?>) entry;
            List<?> tags = (List<?>) rule.get("tags");
            String id = String.valueOf(rule.get("id"));
            boolean selected = options().getRules().containsKey(id)
                    || (tags.stream().anyMatch(TAGS::contains) && !tags.contains("deprecated") && !tags.contains("experimental"));
            if (selected && !returned.contains(id)) throw new IllegalStateException("Missing selected rule result: " + id);
        }
    }

    private void waitForRendering() {
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(browser -> Boolean.TRUE.equals(
                ((JavascriptExecutor) browser).executeScript("return document.readyState === 'complete'"
                        + " && (!document.fonts || document.fonts.status === 'loaded')"
                        + " && [...document.images].filter(i => i.getClientRects().length && getComputedStyle(i).visibility !== 'hidden')"
                        + ".every(i => i.complete && i.naturalWidth > 0)")));
    }

    private Map<String, Object> environment() {
        Map<String, Object> env = new LinkedHashMap<>();
        env.put("java", System.getProperty("java.version"));
        env.put("os", System.getProperty("os.name") + " " + System.getProperty("os.version"));
        env.put("browser", ((HasCapabilities) driver).getCapabilities().asMap());
        env.put("viewport", ((JavascriptExecutor) driver).executeScript(
                "return {width:innerWidth,height:innerHeight,devicePixelRatio:devicePixelRatio,visualViewportScale:visualViewport ? visualViewport.scale : null}"));
        return env;
    }

    public long violationCount() {
        return states.values().stream().map(s -> (Results) s.get("axe")).filter(r -> r != null && r.getViolations() != null)
                .mapToLong(r -> r.getViolations().size()).sum();
    }

    public void finish() {
        finished = true;
        for (Map<String, Object> state : states.values()) {
            if (state.get("executionStatus").equals("Not Executed")) {
                IllegalStateException exception = new IllegalStateException("Required scan not executed: " + state.get("stateKey"));
                state.putIfAbsent("technicalError", error("missing scan", exception));
                errors.add(exception);
            }
        }
        if (violationCount() > 0) {
            AssertionError failure = new AssertionError(caseId + ": " + violationCount()
                    + " rule violations across required states; see scan JSON and manifest");
            errors.forEach(failure::addSuppressed);
            throw failure;
        }
        if (!errors.isEmpty()) {
            IllegalStateException failure = new IllegalStateException(caseId + ": incomplete/invalid accessibility execution", errors.getFirst());
            errors.stream().skip(1).forEach(failure::addSuppressed);
            throw failure;
        }
    }

    /** Called by the listener if scenario code aborts before the final decision. */
    public void recordUnexpected(Throwable original) {
        if (!finished) {
            errors.add(original);
            for (Map<String, Object> state : states.values()) {
                if (state.get("executionStatus").equals("Not Executed")) {
                    state.put("technicalError", error("unexpected method termination", original));
                }
            }
        }
    }

    public boolean isFinished() {
        return finished;
    }

    public void recordEvidenceError(RuntimeException exception) {
        errors.add(exception);
    }

    public Map<String, Object> manifest() {
        Map<String, Object> manifest = new LinkedHashMap<>();
        manifest.put("runId", runId);
        manifest.put("caseId", caseId);
        manifest.put("startedAt", startedAt);
        manifest.put("finishedAt", Instant.now().toString());
        manifest.put("integrationVersion", "4.13.0");
        manifest.put("configuration", options());
        manifest.put("experimentalEnabledRules", EXPERIMENTAL);
        manifest.put("targetSizePolicy", "Enabled explicitly; stable rule disabled by default, not tagged experimental");
        manifest.put("excludedRulePolicy", "AAA, best-practice, obsolete and deprecated outside selected baseline; no impact/node suppression");
        manifest.put("availableRules", inventory);
        manifest.put("lastVerifiedState", lastVerifiedState);
        try { manifest.put("captureContextUrl", driver.getCurrentUrl()); }
        catch (RuntimeException exception) { manifest.put("captureContextError", error("capture context", exception)); }
        manifest.put("captureContextNote", "Failure screenshot/URL captured at method end; last verified state is not proof of screenshot state");
        manifest.put("requiredScans", states.size());
        manifest.put("completedScans", states.values().stream().filter(s -> s.get("executionStatus").equals("Completed")).count());
        manifest.put("violationRuleOccurrences", violationCount());
        manifest.put("outcome", violationCount() > 0 ? "FAIL" : errors.isEmpty() && states.values().stream()
                .allMatch(s -> s.get("executionStatus").equals("Completed")) ? "PASS" : "Technical Error");
        manifest.put("technicalErrors", errors.stream().map(e -> error("case", e)).toList());
        manifest.put("states", states.values().stream().map(s -> {
            Map<String, Object> summary = new LinkedHashMap<>(s);
            summary.remove("axe");
            return summary;
        }).toList());
        return manifest;
    }

    public List<Map<String, Object>> scanEvidence() {
        return states.values().stream().filter(s -> s.containsKey("startedAt")).map(s -> {
            Map<String, Object> evidence = new LinkedHashMap<>(s);
            evidence.put("caseId", caseId);
            evidence.put("runId", runId);
            evidence.put("configuration", options());
            evidence.put("experimentalEnabledRules", EXPERIMENTAL);
            return evidence;
        }).toList();
    }

    private Map<String, Object> error(String stage, Throwable exception) {
        StringWriter trace = new StringWriter();
        exception.printStackTrace(new PrintWriter(trace));
        Map<String, Object> details = new LinkedHashMap<>();
        details.put("stage", stage);
        details.put("exception", exception.getClass().getName());
        details.put("message", String.valueOf(exception.getMessage()));
        details.put("stackTrace", trace.toString());
        return details;
    }
}
