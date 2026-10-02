# SauceDemo QA Automation Portfolio — Test Plan

| Document field | Value |
|---|---|
| Version | 1.0 |
| Date | October 2026 |
| Author | David Pérez |
| Application under test | SauceDemo — https://www.saucedemo.com/ |
| Repository | https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio |
| Language | English |

## 1. Objective

Define a focused, traceable approach for evaluating the main SauceDemo shopping flows through manual functional testing and UI automation. This portfolio project demonstrates practical QA analysis, test design, automation, and clear reporting without adding unnecessary process or framework complexity.

## 2. Application under test

SauceDemo is a publicly available web application that simulates an online store. This plan covers authentication, product browsing and sorting, cart operations, checkout, order confirmation, and the logout step at the end of the end-to-end flow.

## 3. Scope

The initial suite contains 15 functional test cases. All 15 are intended to be automated in the project.

| Module | Coverage | Test case IDs | Count |
|---|---|---|---:|
| Login | Valid login, incorrect password, unknown user, locked user | TC-LOGIN-001–004 | 4 |
| Products | View catalog, sort by price, add a product | TC-PROD-001–003 | 3 |
| Cart | Verify an item, remove an item, continue to checkout | TC-CART-001–003 | 3 |
| Checkout | Complete checkout; validate missing first name, last name, and postal code | TC-CHECK-001–004 | 4 |
| End-to-End | Complete a purchase and log out | TC-E2E-001 | 1 |
| **Total** |  |  | **15** |

Detailed scenarios, steps, expected results, execution fields, and test data are maintained in [the English QA workbook](../test-artifacts/qa-test-documentation-english.xlsx). The Spanish version is [the Spanish QA workbook](../test-artifacts/qa-test-documentation-spanish.xlsx).

## 4. Out of scope

- Performance, load, and stress testing.
- Security and penetration testing.
- Mobile-device testing and exhaustive cross-browser coverage.
- Backend, API, infrastructure, and real payment-provider testing. API testing is planned as a separate portfolio project.
- Accessibility testing in this initial test cycle; accessibility testing is planned for a later project phase.

## 5. Test approach

- Use functional, positive, negative, regression, and end-to-end testing for the cases listed in scope.
- Perform exploratory manual checks to understand the application and investigate unexpected behavior; record defects when they are identified.
- Automate all 15 defined cases with Java, Maven, Selenium WebDriver, TestNG, and Page Object Model. Keep the design small enough to explain and maintain.
- Record execution status, actual result, and a defect reference in the QA workbook when applicable. Do not assume or invent defects before execution.
- Add test reporting and CI/CD with GitHub Actions in later project phases.

## 6. Test environment

- Device: David Pérez's personal laptop.
- Operating system: Windows 11 25H2.
- Browser: Google Chrome 154.0.8037.93, the version available when this plan was prepared (October 2026). The installed browser version may change.
- Application: SauceDemo public demo site.
- Planned automation stack: Java, Maven, Selenium WebDriver, and TestNG.

## 7. Test data

Use SauceDemo's public demo accounts and non-sensitive sample checkout information. The public demo username and password are recorded in the Test Data sheet of each QA workbook, with a source reference and a note explaining that they are intentionally public demo credentials, not a security defect. Negative cases use clearly identified synthetic invalid values.

## 8. Test scenarios and traceability

The QA workbook maps each high-level scenario to its test cases and test data. The suite is grouped into Login, Products, Cart, Checkout, and End-to-End. Test case IDs are stable references for future automation methods and execution results.

## 9. Entry criteria

- SauceDemo is reachable from the test laptop.
- The public test accounts and sample data needed by the cases are available.
- The scope, scenarios, and expected results are documented.
- Before automated execution, the local Java/Maven test project and browser setup are ready.

## 10. Exit criteria

- All 15 test cases have an execution result for the planned test cycle.
- Results and any observed defects are recorded in the workbook.
- Automated cases have been run and their outcomes reviewed when the automation phase is ready.
- Any blocked or unexecuted case is identified with a reason; no pass-rate threshold is assumed.

## 11. Risks and assumptions

- SauceDemo is an external demo service; availability and behavior are outside this project's control.
- Application updates may change page behavior or locators and require test maintenance.
- Public demo accounts and the simulated purchase flow do not represent production credentials or real payments.
- The defined suite covers selected user flows and does not claim exhaustive product coverage.
- Chrome's installed version can change; the environment field records the version at plan preparation time.

## 12. Deliverables and future work

**Initial deliverables:** this Test Plan in English and Spanish, the bilingual QA test workbooks, project instructions in `AGENTS.md`, and an initial bilingual README.

**Later project phases:** Java/Maven automation framework and all 15 automated cases; execution and defect reporting; accessibility testing; and CI/CD with GitHub Actions. API testing will be developed separately.

## 13. Document maintenance

Update this plan when the agreed scope, test environment, or project approach changes. Keep the English and Spanish files aligned and update the version/date when a material revision is made.
