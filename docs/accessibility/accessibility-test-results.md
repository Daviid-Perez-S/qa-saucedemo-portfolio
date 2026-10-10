# Accessibility Test Results

Version: 1.1. Local execution: 2026-10-09 (UTC−06:00). Baseline: WCAG 2.2 A/AA.

Six TestNG methods and thirteen scans were implemented and verified. Final runs detected no violations; all required scans completed in the expected state. This does not establish WCAG 2.2 AA conformance. All ten manual categories remain Planned / Not Executed and Compliance Result remains Not Evaluated.

## Verified executions

| Mode | Command | Tests | PASS | FAIL / Broken / Skipped | Scans | Allure results |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| Functional | `mvn clean test` | 15 | 15 | 0 / 0 / 0 | 0 | 15 |
| Accessibility | `mvn clean test "-Dtest=AccessibilityTest"` | 6 | 6 | 0 / 0 / 0 | 13 | 6 |
| All | `mvn clean test "-Dtest=*Test"` | 21 | 21 | 0 / 0 / 0 | 13 | 21 |

All three commands ended with BUILD SUCCESS. One result per method, without duplicate results. Each accessibility-containing run retains 13 scan JSONs and 6 manifests (19 attachments), without successful-test screenshots. Allure Report 3.20.0 was generated for the All run.

## Case results

| ID | Required / completed scans | Implementation Status | Execution Status | Automated outcome | Compliance Result |
| --- | --- | --- | --- | --- | --- |
| A11Y-AUTO-001 | 2 / 2 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-002 | 3 / 3 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-003 | 2 / 2 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-004 | 4 / 4 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-005 | 1 / 1 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-006 | 1 / 1 | Implemented / Verified | Executed | PASS | Not Evaluated |

## Findings by state

| Case | State | Violations | incomplete rules / nodes | Review |
| --- | --- | ---: | --- | --- |
| A11Y-AUTO-001 | `login-initial` | 0 | 0 | Not Required |
| A11Y-AUTO-001 | `login-invalid-credentials` | 0 | color-contrast: 1 node(s) | Pending |
| A11Y-AUTO-002 | `products-initial` | 0 | color-contrast: 2 node(s) | Pending |
| A11Y-AUTO-002 | `products-product-added` | 0 | color-contrast: 2 node(s) | Pending |
| A11Y-AUTO-002 | `products-menu-open` | 0 | color-contrast: 2 node(s) | Pending |
| A11Y-AUTO-003 | `cart-with-product` | 0 | 0 | Not Required |
| A11Y-AUTO-003 | `cart-empty` | 0 | 0 | Not Required |
| A11Y-AUTO-004 | `checkout-information-initial` | 0 | 0 | Not Required |
| A11Y-AUTO-004 | `checkout-error-first-name` | 0 | 0 | Not Required |
| A11Y-AUTO-004 | `checkout-error-last-name` | 0 | 0 | Not Required |
| A11Y-AUTO-004 | `checkout-error-postal-code` | 0 | 0 | Not Required |
| A11Y-AUTO-005 | `checkout-overview` | 0 | 0 | Not Required |
| A11Y-AUTO-006 | `checkout-complete` | 0 | 0 | Not Required |

Violations: 0, distinct violated rules: 0, violated nodes: 0. Final technical errors: 0. There are 4 incomplete rule occurrences across 4 states, with 7 node occurrences; occurrences are not deduplicated across states. `color-contrast` requires human review of elements and backgrounds; it is not converted into a contrast PASS or a confirmed defect. Full selectors/checks are retained in JSON. `passes` and `inapplicable` are retained and do not establish conformance or WCAG Not Applicable.

## Environment and evidence

- Java `25.0.4.1`; Selenium `4.49.0`; TestNG `7.12.0`; Allure TestNG `3.0.0`; Surefire `3.5.6` (native TestNG provider).
- axe Java integration / engine `4.13.0`; Allure Maven Plugin `3.1.0`; Report `3.20.0`.
- Effective transitive dependencies: deque `utilities 4.13.0`, `commons-io 2.22.0`, `commons-lang3 3.20.0`, Jackson `databind/core 2.22.1` and `annotations 2.22`. Only WebDriverManager was excluded; Maven selected direct Selenium `4.49.0` over transitive `4.13.0`.
- Windows 11 10.0; Chrome `154.0.8037.99`; viewport `1036×647` CSS px; devicePixelRatio `1.25`; visualViewportScale `1`.
- Tags: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`.
- Experimental enabled: `css-orientation-lock`, `label-content-name-mismatch`, `p-as-heading`, `table-fake-caption`, `td-has-header`.
- `target-size`: enabled explicitly; disabled by default, **not experimental** in the selected engine.
- All run ID: `1c39d6a1-dbad-4010-b900-7f92101f27a8`. UTC scan timestamps: `2026-10-10T01:35:49.403Z` to `2026-10-10T01:36:11.155Z`.
- Baseline commit: `332af2851839bd4f906998b7ae5a362176a3b6fd` plus uncommitted implementation; source hashes recorded in the summary.

[Verifiable execution summary](accessibility-execution-summary.json) records case IDs, versions, hashes, audit configuration, state results and pending human reviews. Local Allure identifiers and attachment filenames are omitted from this public summary. Local All evidence: `target/allure-results/`; report: `target/allure-report/`. Local archives for the three modes: `.accessibility-verification/functional-final/`, `.accessibility-verification/accessibility-final/` and `.accessibility-verification/all-final/`, ignored by Git. No report URL was published. `clean` removes target: preserve/export evidence before another run.

## Contract verification and limitations

Eight synthetic checks, outside the approved suites and real SauceDemo evidence, verified PASS, violations, technical error, missing scan, invalid result, mixed outcome, continuation after a violation and unexpected termination. Allure classified AssertionError as failed and technical errors as broken; the unexpected case retained the original exception. A separate synthetic page with two 8×8 CSS px buttons produced serious target-size findings on two nodes. These findings are not SauceDemo defects.

During development, the initial integrity check rejected a rule occurring in different categories; it was corrected to permit different node outcomes. A technical preparation error also occurred when chaining checkout variants with clear(): the form advanced to Overview. Keyboard selection/deletion corrected the preparation, and final runs completed all four variants. FailureEvidenceListener remained unchanged; its screenshot/URL were verified during the real development technical failure.

Chrome 154 emitted a CDP warning (Selenium provides 153); WebDriver flows and scans completed and do not use CDP. SLF4J reported no provider; no logging dependency was added. No final technical errors remain. visualViewport scale was recorded; Chrome desktop zoom was not independently measured. The four incomplete findings, experimental rules and ten manual categories require attention before conclusions about accessibility.

## Defect register

No confirmed accessibility defects are documented. Zero automated violations does not resolve incomplete findings or manual evaluation.

## Manual evaluation status

| ID | Category | Implementation Status | Execution Status | Lifecycle | Compliance Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-MAN-001 | Keyboard Accessibility | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-002 | Focus Visibility, Order and Obscuring | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-003 | Screen Reader Navigation with NVDA | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-004 | Accessible Names, Roles and States | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-005 | Forms, Labels and Error Identification | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-006 | Images and Non-text Content | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-007 | Headings, Structure and Meaningful Sequence | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-008 | Zoom, Resize, Reflow and Text Spacing | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-009 | Visual Presentation, Contrast and Target Size | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-010 | Dynamic Content, Status and Error Communication | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |

Expected results in the workbook are future acceptance objectives, not observed outcomes. No manual category has passed or failed.

## Preserved coverage

Scope remains six cases, thirteen states and 55 A/AA criteria: 37 Applicable and 18 To Be Confirmed; no closed N/A. Excluded routes and generated-PDF evaluation remain excluded. A rendered PDF control is included only in the Complete scan. Matrix relationships indicate partial coverage, not conformance evidence. NVDA and manual evaluation were not executed.

The matrix records partial automated rule execution for 22 criteria, including axe inapplicable results; this does not determine WCAG applicability or fully evaluate a criterion. All 55 criteria remain Not Evaluated.
