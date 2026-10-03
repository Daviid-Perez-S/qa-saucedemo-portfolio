# Project Agent Instructions

## Project context

- Project: SauceDemo QA Automation Portfolio.
- Public repository: https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio.
- Application under test: https://www.saucedemo.com/.
- Current stack: Java, Maven, Selenium WebDriver, TestNG, Page Object Model, and Allure Report.
- The approved initial suite contains 15 functional test cases. Keep automation traceable to the approved test case IDs and keep the English and Spanish QA workbook editions aligned.
- Current documented environment: personal laptop, Windows 11 25H2, and Google Chrome 154.0.8037.93. Treat the Chrome version as a snapshot that may change.
- API testing is a separate project. Allure reporting and automatic failure evidence are implemented and verified. Accessibility testing and CI/CD with GitHub Actions are planned for later phases.

## Working guidelines

- Keep the implementation small, readable, and explainable. Avoid overengineering and unnecessary dependencies.
- Inspect the repository structure and current implementation before proposing or making architectural changes.
- Work incrementally; do not generate the complete framework in one step. Explain material design choices before changing architecture.
- Do not add Cucumber, PageFactory, ThreadLocal, Selenium Grid, Docker, or Jenkins unless David explicitly changes the project scope.
- Do not use `Thread.sleep()`; use explicit waits suited to the condition being checked.
- Create Chrome through `DriverFactory.createChromeDriver()` so password manager settings stay consistent across tests. `BaseTest` centralizes only the common WebDriver lifecycle: a fresh browser and initial navigation per test, followed by `quit()` and clearing the driver reference. Keep scenario-specific preparation, Page Objects, and assertions in the concrete test classes; do not expand `BaseTest` beyond this responsibility without an agreed need.
- `BaseTest.getDriver()` exposes the current instance's WebDriver to `FailureEvidenceListener`; keep reporting logic in the listener and preserve sequential execution with a fresh browser per test. Do not introduce parallel execution, a static driver, or a singleton.
- Use Allure TestNG 3.0.0, Allure Maven Plugin 3.1.0, and Allure Report 3.20.0. Keep Maven Surefire Plugin at 3.5.6 for its native TestNG provider: with 3.6.0, the JUnit Platform TestNG engine's discovery dry runs generated 45 Allure results for the 15-test suite. Version 3.5.6 was verified to generate exactly 15 unique results without adapters or result filters.
- Register `FailureEvidenceListener` centrally through ServiceLoader. Its `IInvokedMethodListener.afterInvocation()` captures only failed `@Test` methods, before Allure finalizes the result and before browser cleanup. Attempt a PNG screenshot and current URL independently; evidence errors must not replace or alter the original test failure. Keep tests and Page Objects free of reporting logic.
- Let TestNG/Allure provide the exception, error message, and stack trace. Do not add manual error attachments, screenshots for successful tests, page source, console/network logs, video, reporting-only logging, or automatic retries. Configuration-method failures are reported by the adapter without browser evidence.
- Store Allure results in `target/allure-results`, reports in `target/allure-report`, and keep `historyEnabled=false`. Generated `target/` content and the `.allure/` runtime cache stay ignored. Use `mvn clean test`, then `mvn allure:report` or `mvn allure:serve`; do not clean between a failed run and report generation.
- Do not invent SauceDemo behavior, requirements, or defects. Document defects only when they are observed.
- Do not copy code from other repositories. Use external material as reference and write project-specific implementation.
- Keep the English and Spanish project documents aligned when either version changes.
- Do not commit, push, publish, or change GitHub settings unless David asks.
- Update this file when project decisions or working conventions change; routine code progress does not require an automatic update.

## Documentation Maintenance

- Keep `README.md` and `README-spanish.md` synchronized.
- When a test case is successfully automated and verified, update its status in the README automation coverage table and update the automation progress counter.
- Do not duplicate detailed test steps, test data, or expected results in the README; keep those details in the QA test artifacts.
- Keep implementation details separate from test coverage information.
- Update documentation only when it reflects the actual verified state of the project.
