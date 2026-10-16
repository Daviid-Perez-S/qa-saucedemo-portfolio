# SauceDemo QA Automation Portfolio

Functional and automated accessibility testing for SauceDemo, with Java, Selenium, Allure evidence and GitHub Actions.

[![SauceDemo CI](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/ci.yml)
[![Allure Pages](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/pages.yml/badge.svg?branch=master)](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/pages.yml)

**[View the public Allure report](https://daviid-perez-s.github.io/qa-saucedemo-portfolio/)**

**English (primary)** · [Español](README-spanish.md)

**Contents**

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Test Coverage](#test-coverage)
- [Framework Architecture](#framework-architecture)
- [Getting Started](#getting-started)
- [CI & Reporting](#ci--reporting)
- [QA Documentation](#qa-documentation)
- [Project Status & Limitations](#project-status--limitations)

## Project Overview

This portfolio demonstrates test analysis, traceable case design, UI automation, accessibility checks and evidence-based reporting against [SauceDemo](https://www.saucedemo.com/), a public demo store.

The shopping flow covers login, products, cart, checkout, confirmation and logout. The framework uses Page Object Model, explicit waits and independent tests. GitHub Actions runs both suites and publishes a consolidated Allure report through GitHub Pages.

Test data uses public demo accounts and synthetic checkout details.

## Tech Stack

| Technology | Responsibility |
|---|---|
| Java 25 | Test implementation |
| Maven / Surefire 3.5.6 | Dependencies, build and test selection |
| Selenium 4.49.0 / Chrome | Browser automation; Selenium Manager resolves ChromeDriver |
| TestNG 7.12.0 | Test lifecycle and assertions |
| axe-core 4.13.0 | Automated accessibility scans via the Java Selenium integration |
| Allure Report 3.20.0 | Results, attachments and HTML reports |
| GitHub Actions / Pages | CI execution and public report hosting |

See [pom.xml](pom.xml) for pinned dependencies and plugins, including Allure TestNG 3.0.0 and Allure Maven Plugin 3.1.0.

## Test Coverage

**Functional automation: 15 / 15 approved cases.**

| Area | Coverage | Tests |
|---|---|---:|
| Login | Valid, invalid-password, unknown-user and locked-user access | 4 |
| Products | Catalog, ascending price order and cart addition | 3 |
| Cart | Item details, removal and checkout navigation | 3 |
| Checkout | Valid completion and three required-field errors | 4 |
| End-to-end | Purchase and logout | 1 |
| **Total** | | **15** |

The [functional QA workbook](docs/test-artifacts/qa-test-documentation-english.xlsx) contains case details and execution records. Test descriptions retain approved IDs for traceability.

**Automated accessibility: six tests containing thirteen full-page axe scans.**

| Page / states | Tests | Scans |
|---|---:|---:|
| Login: initial and invalid credentials | 1 | 2 |
| Products: initial, product added and menu open | 1 | 3 |
| Cart: with product and empty | 1 | 2 |
| Checkout information: initial and three required-field errors | 1 | 4 |
| Checkout overview | 1 | 1 |
| Checkout complete | 1 | 1 |
| **Total** | **6** | **13** |

There are **21 automated tests in total**; scans are contained within the six accessibility tests. Counts describe implemented coverage, not a permanent pass rate.

Scans use the configured WCAG 2.2 A/AA rule baseline. All required states must complete without violations or technical errors for an automated PASS. axe `incomplete` findings remain separate and require human review. See [accessibility results and limitations](docs/accessibility/accessibility-test-results.md).

## Framework Architecture

| Component | Responsibility |
|---|---|
| [Page Objects](src/test/java/com/david/qa/pages) | Locators, interactions, explicit waits and page-state queries |
| [TestNG tests](src/test/java/com/david/qa/tests) | Scenario preparation and assertions |
| [DriverFactory](src/test/java/com/david/qa/driver/DriverFactory.java) | Chrome creation, password-manager preferences and optional headless mode |
| [BaseTest](src/test/java/com/david/qa/tests/BaseTest.java) | Fresh browser, initial navigation and browser cleanup per test |
| [AccessibilityAudit](src/test/java/com/david/qa/accessibility/AccessibilityAudit.java) | Rule configuration, state/result integrity and aggregate outcome |
| [Listeners](src/test/java/com/david/qa/listeners) / Allure | Failure evidence and structured accessibility attachments |

Tests run sequentially with a fresh browser per method. Reporting stays in listeners, registered through ServiceLoader.

Failed tests receive a PNG screenshot and URL when available, before browser cleanup; configuration failures have no browser evidence. Accessibility scan JSON and case manifests are attached for passed and failed tests. TestNG/Allure supplies exception details. Successful tests have no screenshots.

## Getting Started

### Prerequisites

Install JDK 25, Maven and Chrome. Run commands from the project root. Internet access is required for SauceDemo, dependency downloads and initial Selenium Manager/Allure setup. Global Node.js is unnecessary.

### Run tests

Choose one mode:

**Functional — 15 tests**

```shell
mvn clean test
```

**Accessibility — 6 tests, 13 scans**

```shell
mvn clean test "-Dtest=AccessibilityTest"
```

**Combined — 21 tests**

```shell
mvn clean test "-Dtest=*Test"
```

Each `clean test` replaces previous `target/` results. Separate suite runs do not consolidate results. Preserve evidence before another run.

Chrome opens graphically by default. Add `"-Dheadless=true"` to any test command; for example:

```shell
mvn clean test "-Dheadless=true"
```

### View Allure locally

After testing, generate HTML:

```shell
mvn allure:report
```

Or generate and view the report through a local server:

```shell
mvn allure:serve
```

Stop the server with `Ctrl+C`. View the report through HTTP rather than opening `index.html` directly.

**After a failed run, generate the report without running `clean` first**, preserving results and attachments.

| Output | Location |
|---|---|
| Surefire results | `target/surefire-reports/` |
| Raw Allure results | `target/allure-results/` |
| Generated HTML | `target/allure-report/` |

Generated output and the `.allure/` runtime cache are ignored by Git. Report history is disabled.

## CI & Reporting

### Test execution — SauceDemo CI

[ci.yml](.github/workflows/ci.yml) runs on pushes to `feature/github-actions-ci` and `master`, PRs targeting `master`, and manual dispatch. Two independent jobs use Ubuntu 24.04, Temurin Java 25, Maven caching and headless Chrome. Jobs may run simultaneously; tests within each job remain sequential.

CI validates 15 functional and six accessibility results, including thirteen scans and six manifests. Validation requires passed tests and consistent evidence. Report generation and artifact upload are attempted after failures unless cancelled, without concealing failed steps.

| Artifact | Suite |
|---|---|
| `functional-evidence` | Functional |
| `accessibility-evidence` | Accessibility |

Download both artifacts from the originating CI run within **14 days**. They include Surefire reports, raw Allure results and HTML when generation succeeds.

### Report publication — Allure Pages

[pages.yml](.github/workflows/pages.yml) runs after eligible completed CI executions from `master`, originating from a push or manual dispatch. PR results are not published.

It verifies original artifacts, validates and consolidates 21 results, then generates and checks HTML and attachments before deployment. Original CI metadata stays visible; older candidates cannot replace newer confirmed publications.

**Valid, complete evidence can be published even when tests fail.** Publication validation permits documented `failed`/`broken` results, but rejects skipped tests, missing scans and inconsistent evidence. A successful deployment confirms publication, not test success. Workflow badges show workflow status; inspect the report for test outcomes.

## QA Documentation

| Topic | Documents |
|---|---|
| Functional testing | [Initial test plan](docs/test-plan/test-plan-english.md) · [QA workbook](docs/test-artifacts/qa-test-documentation-english.xlsx) |
| Accessibility | [Test plan](docs/accessibility/accessibility-test-plan.md) · [Cases and WCAG matrix](docs/accessibility/accessibility-test-cases.xlsx) |
| Local accessibility baseline, 2026-10-09 | [Results and limitations](docs/accessibility/accessibility-test-results.md) · [Execution summary](docs/accessibility/accessibility-execution-summary.json) |
| Evidence and publication | [Validator](scripts/validate-ci-evidence.py) · [Consolidation](scripts/consolidate-allure-results.py) · [Publication checks](scripts/pages-publication.py) |

The functional plan records the initial scope; dated documents describe historical execution baselines. Consult the public report and workflows for subsequent results.

## Project Status & Limitations

**The defined objectives for functional automation, automated accessibility, reporting and CI/CD are implemented and verified.**

- Manual accessibility evaluation is **postponed indefinitely, with no scheduled date**, outside the completed scope. Its ten documented categories remain Planned / Not Executed.
- Automated results do not establish WCAG 2.2 AA conformance or constitute a comprehensive accessibility evaluation. `incomplete` findings require human review.
- Coverage targets selected Chrome flows; external service availability and application changes can affect execution.
- Performance, security, mobile, exhaustive cross-browser, backend and real-payment testing are outside scope. API testing belongs to a separate project.

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

**Project owner:** [David Pérez](https://www.linkedin.com/in/david-perez-s/).
