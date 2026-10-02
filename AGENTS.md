# Project Agent Instructions

## Project context

- Project: SauceDemo QA Automation Portfolio.
- Public repository: https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio.
- Application under test: https://www.saucedemo.com/.
- Planned stack: Java, Maven, Selenium WebDriver, TestNG, and Page Object Model.
- The approved initial suite contains 15 functional test cases. Keep automation traceable to the approved test case IDs and keep the English and Spanish QA workbook editions aligned.
- Current documented environment: personal laptop, Windows 11 25H2, and Google Chrome 154.0.8037.93. Treat the Chrome version as a snapshot that may change.
- API testing is a separate project. Accessibility testing, reporting, and CI/CD with GitHub Actions are planned for later phases.

## Working guidelines

- Keep the implementation small, readable, and explainable. Avoid overengineering and unnecessary dependencies.
- Inspect the repository structure and current implementation before proposing or making architectural changes.
- Work incrementally; do not generate the complete framework in one step. Explain material design choices before changing architecture.
- Do not add Cucumber, PageFactory, ThreadLocal, Selenium Grid, Docker, or Jenkins unless David explicitly changes the project scope.
- Do not use `Thread.sleep()`; use explicit waits suited to the condition being checked.
- Do not invent SauceDemo behavior, requirements, or defects. Document defects only when they are observed.
- Do not copy code from other repositories. Use external material as reference and write project-specific implementation.
- Keep the English and Spanish project documents aligned when either version changes.
- Do not commit, push, publish, or change GitHub settings unless David asks.
- Update this file when project decisions or working conventions change; routine code progress does not require an automatic update.
