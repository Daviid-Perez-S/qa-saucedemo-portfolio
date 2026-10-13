# SauceDemo QA Automation Portfolio

An early-stage QA portfolio project for planning and automating core user flows in the public SauceDemo demo store.

This English `README.md` is the primary GitHub landing page. [Read the Spanish version](README-spanish.md).

**Project owner:** David Pérez · **Status:** all 15 initial functional tests and six accessibility tests (thirteen scans) automated and verified; GitHub Actions CI, Allure reports and separate evidence artifacts verified on `feature/github-actions-ci`; integration into `master` pending.

## Project goals

- Document a focused set of 15 functional test cases with clear scenarios, steps, expected results, and test data.
- Build a maintainable Java UI automation project using Maven, Selenium WebDriver, TestNG, and Page Object Model.
- Automate the 15 agreed cases and record results and defects when found.
- Generate Allure reports with automatic browser evidence for failed tests.
- Maintain automated accessibility testing and GitHub Actions continuous integration with verifiable evidence.

API testing is planned as a separate portfolio project. The initial scope excludes performance, security, mobile, exhaustive cross-browser, backend, and real payment testing.

## Documentation

- [Test Plan — English](docs/test-plan/test-plan-english.md) · [QA workbook — English](docs/test-artifacts/qa-test-documentation-english.xlsx)
- [Plan de pruebas — Español](docs/test-plan/test-plan-spanish.md) · [Libro QA — Español](docs/test-artifacts/qa-test-documentation-spanish.xlsx)
- [Project instructions for coding agents](AGENTS.md)
- [README en español](README-spanish.md)

## Current technology

Java · Maven · Selenium WebDriver · TestNG · Page Object Model · Google Chrome · Allure Report · GitHub Actions

The documented local test environment is a personal laptop running Windows 11 25H2 and Google Chrome 154.0.8037.99. CI uses GitHub-hosted Ubuntu 24.04 runners, Temurin Java 25, Maven and Chrome headless. Maven and Chrome versions come from the runner image and are logged on every run; the local Chrome version is a snapshot and may change.

## Automation Coverage

**Automation progress: 15 / 15 test cases**

| Test Case ID | Scenario | Status |
|---|---|---|
| TC-LOGIN-001 | Login with valid credentials | Automated |
| TC-LOGIN-002 | Login with an incorrect password | Automated |
| TC-LOGIN-003 | Login with an unknown user | Automated |
| TC-LOGIN-004 | Login with a locked user | Automated |
| TC-PROD-001 | View the product catalog | Automated |
| TC-PROD-002 | Sort products by price, low to high | Automated |
| TC-PROD-003 | Add a product to the cart | Automated |
| TC-CART-001 | Verify an added product in the cart | Automated |
| TC-CART-002 | Remove a product from the cart | Automated |
| TC-CART-003 | Continue from the cart to checkout | Automated |
| TC-CHECK-001 | Complete checkout with valid information | Automated |
| TC-CHECK-002 | Validate missing first name | Automated |
| TC-CHECK-003 | Validate missing last name | Automated |
| TC-CHECK-004 | Validate missing postal code | Automated |
| TC-E2E-001 | Complete a purchase and log out | Automated |

Status reflects implementation in the code, not an execution result. See the [English QA workbook](docs/test-artifacts/qa-test-documentation-english.xlsx) for complete steps, test data, expected results, and execution records, and the [Test Plan](docs/test-plan/test-plan-english.md) for scope and approach.

## Automation Architecture

The project uses Page Object Model with a small separation of responsibilities:

- `LoginPage`, `ProductsPage`, `CartPage`, `CheckoutInformationPage`, `CheckoutOverviewPage`, and `CheckoutCompletePage` contain locators, interactions, explicit waits, and page state queries.
- `LoginTest`, `ProductsTest`, `CartTest`, `CheckoutTest`, and `EndToEndTest` contain the test scenarios and assertions, with each test linked to its approved test case ID.
- All five test classes extend `BaseTest`, which centralizes only the common WebDriver lifecycle. Its `@BeforeMethod` opens a fresh Chrome browser and navigates to SauceDemo before each test's specific preparation. Its `@AfterMethod(alwaysRun = true)` calls `quit()` when a driver exists, including after test failures, and clears the driver reference in `finally`.
- `ProductsTest` logs in and waits for Products during setup; its three cases run independently, each with a fresh browser.
- `CartTest` prepares a cart with one product for each independent case.
- `DriverFactory.createChromeDriver()` centralizes Chrome creation and disables password saving and compromised-password prompts in every test browser. Each call creates a new WebDriver; `BaseTest` owns the common lifecycle, while scenario-specific preparation and assertions stay in the concrete test classes.
- The sorting test explicitly waits for the displayed prices to reach ascending order before asserting the result. `CartPage.removeBackpack()` waits only for the backpack removal; the cart test explicitly waits for the empty-cart state and disappearing badge before its assertions. These scenario expectations remain in the test layer.
- `CheckoutTest` prepares checkout information with a product for each independent case, covering valid checkout and required-field validation. Its private assertion method checks the field-specific error and that checkout remains blocked; assertions stay in the test layer.
- `CheckoutInformationPage` supports field entry, `clickContinue()`, and error queries, as well as the destination check used by Cart. `clickContinue()` describes the action for both valid submissions and submissions blocked by validation. `CheckoutOverviewPage` supports reviewing the summary and finishing the order; `CheckoutCompletePage` exposes the confirmation state. `CheckoutCompletePage` also opens the menu and logs out; `LoginPage` waits for the login form after logout.
- `EndToEndTest` runs the complete purchase and logout flow in one independent browser session, reusing the existing Page Objects.
- Selenium Manager resolves ChromeDriver automatically.
- `FailureEvidenceListener` uses `IInvokedMethodListener.afterInvocation()` and is registered centrally through ServiceLoader. For failed `@Test` methods, it obtains the current instance's browser through `BaseTest.getDriver()` and independently attempts a PNG screenshot and current URL before cleanup. Evidence errors preserve the original failure. Execution remains sequential, with a fresh browser per test.

Current automation structure:

```text
src/test/java/com/david/qa/
├── accessibility/
│   └── AccessibilityAudit.java
├── driver/
│   └── DriverFactory.java
├── listeners/
│   ├── FailureEvidenceListener.java
│   └── AccessibilityEvidenceListener.java
├── pages/
│   ├── LoginPage.java
│   ├── ProductsPage.java
│   ├── CartPage.java
│   ├── CheckoutInformationPage.java
│   ├── CheckoutOverviewPage.java
│   └── CheckoutCompletePage.java
└── tests/
    ├── BaseTest.java
    ├── LoginTest.java
    ├── ProductsTest.java
    ├── CartTest.java
    ├── CheckoutTest.java
    ├── EndToEndTest.java
    └── accessibility/
        └── AccessibilityTest.java
```

Test resources contain `allure.properties` and `META-INF/services/org.testng.ITestNGListener`.

The project uses Java 25, Selenium 4.49.0, TestNG 7.12.0, Maven Compiler Plugin 3.16.0, Maven Surefire Plugin 3.5.6, Allure TestNG 3.0.0, Allure Maven Plugin 3.1.0, and Allure Report 3.20.0.

Surefire 3.5.6 is a compatibility decision for the current TestNG + Allure integration. Surefire 3.6.0 uses the JUnit Platform TestNG engine, whose discovery dry runs generated 45 Allure results for 15 actual tests. The native TestNG provider in 3.5.6 was verified to produce exactly 15 unique results without adapters or result filters.

## Run the automated tests

Requirements: JDK 25, Maven, Google Chrome, and internet access to SauceDemo. Maven downloads dependencies; Selenium Manager may need internet access on the first run.

From the project root, run:

```shell
mvn clean test
```

Standard execution results are available in `target/surefire-reports/`.

Chrome opens with a graphical interface by default. Add `"-Dheadless=true"` to any test command to run without a visible browser window, as CI does:

```shell
mvn clean test "-Dheadless=true"
```

## Allure reporting and failure evidence

Raw Allure results are written to `target/allure-results/`. Generate the HTML report after running the tests:

```shell
mvn allure:report
```

The report is generated in `target/allure-report/`. To generate and view it on a local server:

```shell
mvn allure:serve
```

Stop the server with `Ctrl+C`. The plugin downloads its private Node.js runtime and Allure Report package into `.allure/` on first use; internet access is required for that download, but a global Node.js installation is not required. The runtime cache and generated results/reports are ignored by Git. Report history is initially disabled with `historyEnabled=false`.

View reports through a local HTTP server rather than opening `index.html` directly. For a downloaded CI report, extract the artifact and serve its `allure-report/` directory. On Windows, the existing private runtime can serve it without Python or a global Node.js installation (paths below match the current local cache; adjust if the cache changes):

```powershell
& ".allure/node-v24.14.1-win-x64/node.exe" ".allure/allure-3.20.0/node_modules/allure/cli.js" open "C:/path/to/extracted-artifact/allure-report"
```

Run this from the project root after the Maven plugin has initialized `.allure/`; stop the server with `Ctrl+C`.

If a test run fails, run the report command separately without running `clean` in between, so its results and evidence remain available. Use `mvn clean test` for a fresh execution to avoid mixing results from different runs.

Failed functional `@Test` methods receive a browser PNG screenshot and current URL as a text attachment, when the browser is available. TestNG/Allure supplies the original exception, message, and stack trace. Successful tests receive no browser evidence; configuration failures are reported without browser evidence. Tests and Page Objects contain no reporting logic. No retries, additional logging, page source, console/network logs, or video are collected.

Validation on October 2, 2026 confirmed 15 tests, 0 failures, 0 errors, and 0 skipped, with exactly 15 unique Allure results and no successful-test attachments. A temporary controlled failure in TC-LOGIN-001 produced one failed result with exactly two attachments (PNG and inventory URL) and the original `AssertionError` details. The temporary assertion was removed; the full suite passed again and the final report contains exactly 15 passed tests.


## Automated accessibility

The six approved cases and thirteen scans were implemented and verified with axe-core 4.13.0. Existing functional tests retain their fifteen methods.

```shell
mvn clean test
mvn clean test "-Dtest=AccessibilityTest"
mvn clean test "-Dtest=*Test"
```

Functional / Accessibility / All produced respectively 15 / 6 / 21 TestNG and Allure results on 2026-10-09. Final runs completed all thirteen states with zero violations and technical errors. Four states have color-contrast incomplete findings pending human review; WCAG conformance is not established.

AccessibilityAudit owns configuration, state/result validation and final assertion. AccessibilityEvidenceListener attaches scan JSONs and case manifests, including PASS cases; the failure listener retains screenshot/URL without duplication. BaseTest and the fifteen functional tests are unchanged. Consecutive checkout variants use keyboard deletion to update controlled-form state. Surefire remains 3.5.6, without profiles or parallel test execution. Manual accessibility evaluation is postponed indefinitely; all ten manual categories remain Planned / Not Executed. Automated success does not certify WCAG conformance, and `incomplete` findings remain pending human review.

[Results and limitations](docs/accessibility/accessibility-test-results.md) · [Verifiable summary](docs/accessibility/accessibility-execution-summary.json).

## Continuous integration

[`SauceDemo CI`](.github/workflows/ci.yml) prepares the environment, runs tests headlessly, validates evidence, generates Allure HTML reports and uploads artifacts. Runs on `feature/github-actions-ci` have been verified with 15 functional and six accessibility tests passing, zero failures, errors or skipped tests, and thirteen completed scans. There is no deployment or GitHub Pages publication.

Triggers are push to `feature/github-actions-ci` or `master`, Pull Requests targeting `master`, and manual activation (`workflow_dispatch`). Manual activation through **Actions → SauceDemo CI → Run workflow** requires the workflow to exist on the repository's default branch (`master`); it remains to be checked after integration. See [GitHub's manual-run instructions](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).

Each job has its own Ubuntu 24.04 runner, Temurin Java 25, Maven dependency cache keyed using `pom.xml`, and Chrome. The workflow grants only `contents: read`.

| Job ID / displayed name | Test command | Expected tests | Artifact |
|---|---|---|---|
| `environment-check` / Check Java, Maven and Chrome | `mvn --batch-mode --no-transfer-progress clean test -Dheadless=true` | 15 functional | `functional-evidence` |
| `accessibility` / Accessibility tests | `mvn --batch-mode --no-transfer-progress clean test "-Dtest=AccessibilityTest" -Dheadless=true` | 6 accessibility, 13 scans | `accessibility-evidence` |

The jobs have no `needs` dependency and may run simultaneously. Tests remain sequential within each job, with a fresh browser per test. These are two separate suite executions, totaling 21 tests; CI does not run the combined Maven mode.

The shared [evidence validator](scripts/validate-ci-evidence.py) uses only Python's standard library, provided on the runner. Jobs invoke it with `functional` or `accessibility`. It checks Surefire XML counts and successful outcomes; matches test identities to unique, passed Allure results; checks container references and existing, nonempty attachments, including nested attachments; and rejects duplicate attachment references. Accessibility validation additionally requires thirteen unique approved scans and six manifests from one run, consistent state metadata, completed preparation/scans, no technical errors or confirmed violations, and all four axe categories (`passes`, `violations`, `incomplete`, `inapplicable`). It reports `incomplete` occurrences without treating them as demonstrated conformance. Missing or inconsistent evidence returns exit code 1 and fails the job.

Validation, report generation and artifact upload use `if: ${{ !cancelled() }}` so they are attempted after test or integrity failures, without hiding those failures. A cancelled run does not guarantee evidence preservation. Allure generation does not run `clean`, preserving the test results.

To review a run:

1. Open [Actions → SauceDemo CI](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/ci.yml) and select the relevant commit and event.
2. Open each job's test step. Expect `Tests run: 15` or `Tests run: 6`, with `Failures: 0, Errors: 0, Skipped: 0`, and check the validator's `Evidence integrity PASS` message. Open failed steps for error logs; Success alone is not a substitute for checking the counts.
3. In the run summary's **Artifacts** section, download `functional-evidence` and `accessibility-evidence`. Retention is 14 days. Both contain `surefire-reports/`, `allure-results/` and `allure-report/`; report files depend on successful report generation.
4. Check Surefire `TEST-*.xml` and view the HTML report using the local-server instructions above. Functional Allure results contain 15 `*-result.json` files; accessibility contains six results and 19 JSON attachments (13 scans plus six manifests). Container files represent TestNG lifecycle groupings and are not additional tests; their count is not an acceptance criterion.

PR checks on the latest commit and execution on `master` remain to be verified during integration. Manual accessibility review and WCAG conformance certification are outside the current automated acceptance criteria.

## Application under test

[Open SauceDemo](https://www.saucedemo.com/)

Public SauceDemo demo credentials are documented in the workbook's Test Data sheet and labeled as intentionally public test data.

## Owner

[David Pérez on LinkedIn](https://www.linkedin.com/in/david-perez-s/)
