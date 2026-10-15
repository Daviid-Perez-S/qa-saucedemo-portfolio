# Codex Repository Instructions

## Project Scope

- Maintain the completed SauceDemo QA Automation Portfolio: Java 25, Maven, Selenium, TestNG, Page Object Model, axe-core, Allure, GitHub Actions and Pages.
- Preserve the approved baseline: 15 functional tests, six accessibility tests containing 13 axe scans, and 21 tests total. For authorized coverage changes, update affected tests, validators, reporting expectations and bilingual QA documentation together.
- Keep API testing in its separate project. Manual accessibility evaluation is postponed indefinitely, with no scheduled date; automated results alone do not establish WCAG 2.2 AA conformance.

## Agent Workflow and Authorization

- Inspect existing code, configuration and working-tree changes before editing. Preserve user changes and limit edits to the authorized task.
- Make small, coherent changes; reuse existing components and avoid unnecessary abstractions or dependencies. Do not copy code from other repositories.
- Unless already explicitly authorized, propose architectural decisions or coverage expansions and obtain approval before implementing them. Do not request repeated confirmation for routine edits already authorized.
- Do not introduce Cucumber, PageFactory, ThreadLocal, Selenium Grid, Docker or Jenkins without an explicitly approved scope change.
- Do not create branches, commits or Pull Requests, push, deploy or change remote settings without explicit authorization. The user normally manages Git through GitHub Desktop.
- Keep ordinary repository reads and edits sandboxed. Run browser-based Maven tests and Allure commands opening a browser/server with required execution escalation, reusing approved prefixes; do not first attempt these in a restricted-network session.
- If another command fails because of sandbox restrictions, use the approval mechanism. Never alter application code, Windows ACLs or firewall rules to bypass restrictions.
- Distinguish static inspection, tests actually executed and historical evidence. Report actual changes, checks, failures and unresolved limitations; never invent application behavior, requirements, defects or results.

## Architecture and Browser Lifecycle

- Preserve Page Object Model: pages own locators, navigation, interactions, explicit waits and state queries; concrete tests own scenario preparation and assertions; listeners own Allure reporting.
- Create Chrome through `DriverFactory.createChromeDriver()`; preserve password-manager preferences and Selenium Manager. Keep local execution graphical by default and headless opt-in through `-Dheadless=true`.
- Keep `BaseTest` limited to common WebDriver lifecycle: a fresh browser and initial navigation per test, followed by `quit()` and clearing the reference even after failures. Preserve `getDriver()` for evidence listeners.
- Keep tests sequential and independent, without a static driver or singleton. Use condition-specific explicit waits; do not use `Thread.sleep()`.

## Test Selection and Validation

- Preserve the versions pinned in [pom.xml](pom.xml). Keep Surefire 3.5.6 with its native TestNG provider and one unique Allure result per test. Validate compatibility and result uniqueness for authorized dependency changes.
- Preserve test-case IDs and meaningful assertions. Keep default Surefire inclusion functional and accessibility selection independent; do not introduce profiles, suite XML or automatic retries.

| Selection | Command | Baseline tests |
|---|---|---:|
| Functional | `mvn clean test` | 15 |
| Accessibility | `mvn clean test "-Dtest=AccessibilityTest"` | 6 |
| Combined | `mvn clean test "-Dtest=*Test"` | 21 |

- Match validation to changed contracts. Use static checks for documentation-only changes; run affected suites for behavioral changes, respecting task restrictions and execution permissions.
- After the corresponding suite, run `python scripts/validate-ci-evidence.py functional` or `python scripts/validate-ci-evidence.py accessibility` (`python3` in CI). Validate separate suite outputs; the validator has no combined mode.
- When changing evidence validation, consolidation or publication logic, run existing Python contract checks: `python -B -m unittest discover -s scripts -p "test_*.py"`. Keep synthetic checks separate from real SauceDemo execution evidence.

## Accessibility Contracts

- Preserve the approved case/state mapping in `AccessibilityTest` and [the validator](scripts/validate-ci-evidence.py), subject to authorized coverage changes. Use full-page scans without impact/node suppression or exclusions that hide violations.
- Keep the axe Java integration and bundled engine aligned at 4.13.0; preserve the WebDriverManager-only exclusion and direct Selenium dependency. Coordinate authorized version changes with engine and evidence checks.
- Preserve [AccessibilityAudit](src/test/java/com/david/qa/accessibility/AccessibilityAudit.java) configuration: WCAG A/AA tags, all five documented experimental rules and explicitly enabled `target-size` (disabled by default, not experimental).
- Keep state preparation in tests; keep configuration, state/result integrity checks and aggregate decisions in AccessibilityAudit. Retain `passes`, `violations`, `incomplete` and `inapplicable` results.
- Never PASS missing, unfinished or invalid scans. Confirmed violations produce FAIL, including mixed outcomes; retain technical errors, original diagnostics and later reachable scans.
- Keep `incomplete` findings pending human review, separate from automated outcomes and manual evaluation. Do not interpret axe `inapplicable` as a confirmed WCAG applicability decision.

## Reporting and Evidence

- Register `FailureEvidenceListener` and `AccessibilityEvidenceListener` centrally through ServiceLoader; keep Allure calls out of tests and pages.
- In `FailureEvidenceListener.afterInvocation()`, capture only failed `@Test` methods before Allure finalization and browser cleanup. Attempt PNG screenshot and current URL independently; capture errors must not replace or alter the original failure. Configuration failures receive no browser evidence.
- Attach available accessibility scan JSONs and case manifests for passed and failed tests, including unexpected termination. Preserve original exceptions and mixed-outcome diagnostics; attachment errors must not turn failure into success.
- Do not duplicate screenshots or add standalone error attachments. Let TestNG/Allure supply exception details. Do not add successful-test screenshots, page source, console/network logs, video or reporting-only logging. A method-end screenshot does not prove earlier scan states.
- Store results in `target/allure-results` and HTML in `target/allure-report`; preserve `historyEnabled=false`. Keep `target/`, `.allure/` and `.accessibility-verification/` ignored.
- Start fresh runs with `clean test`; preserve evidence before another run. Generate reports with `mvn allure:report` or `mvn allure:serve` without an intervening `clean`, especially after failures.

## CI and Pages Publication

- Keep [SauceDemo CI](.github/workflows/ci.yml) separate from [Allure Pages](.github/workflows/pages.yml). Preserve CI's two independent Ubuntu 24.04/Temurin Java 25 jobs, Maven cache and headless Chrome. Jobs may overlap; tests within each job remain sequential.
- Preserve CI `contents: read`, push triggers for `feature/github-actions-ci`/`master`, PRs targeting `master` and `workflow_dispatch`; manual dispatch requires the workflow on the default branch.
- Keep strict CI acceptance separate from `--publication` eligibility: CI requires passed tests; publication permits documented `failed`/`broken` results but rejects skipped tests, incomplete scans and inconsistent evidence. Never weaken validation or hide failures with `continue-on-error`.
- Require unique, consistent Surefire/Allure identities and attachment references, all approved scans and one manifest per accessibility case.
- Attempt validation, Allure generation and upload after failures using `!cancelled()`, without cleaning results. Preserve `functional-evidence` and `accessibility-evidence`, their contents and 14-day retention.
- Publish only eligible completed `push`/`workflow_dispatch` CI attempts from the authorized repository's `master` through `workflow_run`. Preserve existing Pages permissions; use trusted `master` code and verify original attempt/artifact identities before publication validation and consolidation.
- Preserve original result and attachment bytes during consolidation; reject identity/filename collisions and inconsistent evidence. Verify rendered results and attachment bytes before deployment; retain safe original CI metadata.
- Treat workflow, job, step, artifact names and run-name formats consumed by [publication checks](scripts/pages-publication.py) as interfaces. Update consumers and contract checks together for authorized changes.
- Order publication by original `(run_number, run_attempt)` against confirmed successful `Deploy GitHub Pages` steps, including earlier successful publisher attempts. Later cancelled or invalid preparations must not block an older publishable candidate.
- Keep the final API gate and deployment under the same `allure-pages-master` concurrency group with `queue: max` and `cancel-in-progress: false`. Do not delete ordering history or add a publisher outside this protocol.
- Never equate successful publication with successful tests or accessibility conformance.

## Documentation Maintenance

- Keep `README.md` primary in English and `README-spanish.md` semantically equivalent. Synchronize affected bilingual QA documents: coverage, IDs, commands, versions, links and limitations.
- Update coverage summaries only for authorized, implemented and verified changes. Keep detailed cases, steps, data and expected results in existing QA artifacts; separate coverage from implementation details.
- Verify relative references. Distinguish dated plans/execution baselines from current implementation; do not present historical results as permanent statistics or claim unexecuted manual work is complete.
- Keep this file in English. Update it when approved project decisions or working conventions change, not for routine progress.
