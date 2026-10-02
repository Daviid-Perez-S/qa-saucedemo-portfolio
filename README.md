# SauceDemo QA Automation Portfolio

An early-stage QA portfolio project for planning and automating core user flows in the public SauceDemo demo store.

This English `README.md` is the primary GitHub landing page. [Read the Spanish version](README-spanish.md).

**Project owner:** David Pérez · **Status:** QA documentation prepared; Login and Products automation implemented.

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

**Automation progress: 7 / 15 test cases**

| Test Case ID | Scenario | Status |
|---|---|---|
| TC-LOGIN-001 | Login with valid credentials | Automated |
| TC-LOGIN-002 | Login with an incorrect password | Automated |
| TC-LOGIN-003 | Login with an unknown user | Automated |
| TC-LOGIN-004 | Login with a locked user | Automated |
| TC-PROD-001 | View the product catalog | Automated |
| TC-PROD-002 | Sort products by price, low to high | Automated |
| TC-PROD-003 | Add a product to the cart | Automated |
| TC-CART-001 | Verify an added product in the cart | Planned |
| TC-CART-002 | Remove a product from the cart | Planned |
| TC-CART-003 | Continue from the cart to checkout | Planned |
| TC-CHECK-001 | Complete checkout with valid information | Planned |
| TC-CHECK-002 | Validate missing first name | Planned |
| TC-CHECK-003 | Validate missing last name | Planned |
| TC-CHECK-004 | Validate missing postal code | Planned |
| TC-E2E-001 | Complete a purchase and log out | Planned |

Status reflects implementation in the code, not an execution result. See the [English QA workbook](docs/test-artifacts/qa-test-documentation-english.xlsx) for complete steps, test data, expected results, and execution records, and the [Test Plan](docs/test-plan/test-plan-english.md) for scope and approach.

## Automation Architecture

The project uses Page Object Model with a small separation of responsibilities:

- `LoginPage` and `ProductsPage` contain locators, interactions, explicit waits, and page state queries.
- `LoginTest` and `ProductsTest` contain the test scenarios and assertions, with each test linked to its approved test case ID.
- `@BeforeMethod` opens a fresh Chrome browser and navigates to SauceDemo for each test. `@AfterMethod(alwaysRun = true)` calls `quit()` when a driver exists, including after test failures.
- `ProductsTest` logs in and waits for Products during setup; its three cases run independently, each with a fresh browser.
- Selenium Manager resolves ChromeDriver automatically.

Current automation structure:

```text
src/test/java/com/david/qa/
├── pages/
│   ├── LoginPage.java
│   └── ProductsPage.java
└── tests/
    ├── LoginTest.java
    └── ProductsTest.java
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
