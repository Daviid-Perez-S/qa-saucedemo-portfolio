# SauceDemo QA Automation Portfolio

An early-stage QA portfolio project for planning and automating core user flows in the public SauceDemo demo store.

This English `README.md` is the primary GitHub landing page. [Read the Spanish version](README-spanish.md).

**Project owner:** David Pérez · **Status:** QA documentation prepared; initial login automation implemented.

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

The test environment currently documented is a personal laptop running Windows 11 25H2 and Google Chrome 154.0.8037.93. The Chrome version is a snapshot and may change.

## Run the initial automated test

Requirements: JDK 25, Maven, Google Chrome, and internet access to SauceDemo. Maven downloads dependencies; Selenium Manager resolves ChromeDriver and may need internet access on the first run.

From the project root, run:

```shell
mvn test
```

The positive TestNG test implements `TC-LOGIN-001` using public test data `TD-LOGIN-01`: open Chrome, log in, verify the Products title, inventory path, and visible catalog, then close the browser even if the test fails. `TC-LOGIN-002` uses `TD-LOGIN-02` (`standard_user` / `invalid_password`) to verify the credentials error and that access is denied while the login page and form remain visible. `TC-LOGIN-003` uses `TD-LOGIN-03` (`non_existing_user` / `secret_sauce`) to verify that an unknown user is rejected with the credentials error and remains on the visible login form. `TC-LOGIN-004` uses `TD-LOGIN-04` (`locked_out_user` / `secret_sauce`) to verify that access is denied with the specific locked-user message and the login form remains visible. Each test opens and closes its own browser. Assertions are in `LoginTest`; `LoginPage` and `ProductsPage` contain locators, interactions, waits, and state queries.

The project uses Java 25, Selenium 4.49.0, TestNG 7.12.0, Maven Compiler Plugin 3.16.0, and Maven Surefire Plugin 3.6.0. The remaining 11 cases are pending. Standard execution results are available in `target/surefire-reports/`.

## Application under test

[Open SauceDemo](https://www.saucedemo.com/)

Public SauceDemo demo credentials are documented in the workbook's Test Data sheet and labeled as intentionally public test data.

## Owner

[David Pérez on LinkedIn](https://www.linkedin.com/in/david-perez-s/)
