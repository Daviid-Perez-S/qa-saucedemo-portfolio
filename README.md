# SauceDemo QA Automation Portfolio

An early-stage QA portfolio project for planning and automating core user flows in the public SauceDemo demo store.

This English `README.md` is the primary GitHub landing page. [Read the Spanish version](README-spanish.md).

**Project owner:** David Pérez · **Status:** QA documentation prepared; all 15 initial functional test cases automated and verified.

## Project goals

- Document a focused set of 15 functional test cases with clear scenarios, steps, expected results, and test data.
- Build a maintainable Java UI automation project using Maven, Selenium WebDriver, TestNG, and Page Object Model.
- Automate the 15 agreed cases and record results and defects when found.
- Add accessibility testing, test reporting, and GitHub Actions CI/CD in later phases.

API testing is planned as a separate portfolio project. The initial scope excludes performance, security, mobile, exhaustive cross-browser, backend, and real payment testing.

## Documentation

- [Test Plan — English](docs/test-plan/test-plan-english.md) · [QA workbook — English](docs/test-artifacts/qa-test-documentation-english.xlsx)
- [Plan de pruebas — Español](docs/test-plan/test-plan-spanish.md) · [Libro QA — Español](docs/test-artifacts/qa-test-documentation-spanish.xlsx)
- [Project instructions for coding agents](AGENTS.md)
- [README en español](README-spanish.md)

## Planned technology

Java · Maven · Selenium WebDriver · TestNG · Page Object Model · Google Chrome

The test environment currently documented is a personal laptop running Windows 11 25H2 and Google Chrome 154. The Chrome version is a snapshot and may change.

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

Current automation structure:

```text
src/test/java/com/david/qa/
├── driver/
│   └── DriverFactory.java
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
    └── EndToEndTest.java
```

The project uses Java 25, Selenium 4.49.0, TestNG 7.12.0, Maven Compiler Plugin 3.16.0, and Maven Surefire Plugin 3.6.0.

## Run the automated tests

Requirements: JDK 25, Maven, Google Chrome, and internet access to SauceDemo. Maven downloads dependencies; Selenium Manager may need internet access on the first run.

From the project root, run:

```shell
mvn test
```

Standard execution results are available in `target/surefire-reports/`.

## Application under test

[Open SauceDemo](https://www.saucedemo.com/)

Public SauceDemo demo credentials are documented in the workbook's Test Data sheet and labeled as intentionally public test data.

## Owner

[David Pérez on LinkedIn](https://www.linkedin.com/in/david-perez-s/)
