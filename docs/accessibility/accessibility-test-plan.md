# Accessibility Test Plan

Project: `qa-saucedemo-portfolio`  
Application: https://www.saucedemo.com/  
Document version: 1.1
Updated: 2026-10-09
Baseline: WCAG 2.2 A / AA

## Purpose and current state

Define accessibility evaluation of the main purchase process. Axe integration and six automated cases with thirteen scans were implemented and verified on 2026-10-09. See Test Results for actual outcomes. Manual evaluation remains pending and WCAG 2.2 AA conformance is not established.

Automated statuses: Implementation Status = Implemented / Verified; Execution Status = Executed. Automated outcome is separate from Compliance Result = Not Evaluated. Manual lifecycle remains Planned / Not Executed. Applicable and To Be Confirmed remain preliminary applicability.

Maven verification used Java 25.0.4.1, Selenium 4.49.0, TestNG 7.12.0, Allure TestNG 3.0.0 and Surefire 3.5.6. Integration is com.deque.html.axe-core:selenium:4.13.0 with axe-core 4.13.0. Only WebDriverManager is excluded. Maven mediation selects direct Selenium 4.49.0 over transitive 4.13.0; DriverFactory/Selenium Manager are retained.

## Scope

Login → Products → Cart → Checkout Information → Checkout Overview → Checkout Complete.

Include initial pages, invalid-credential error, cart addition/removal, all three individual required-field errors and the open side menu. Manual procedures also examine sorting and transitions inside these approved pages. Full-page scans include a PDF control only if it is rendered at completion.

Excluded initially: additional dynamic catalogs, long catalog, individual product detail, additional Slider/Spinner routes, PDF generation and accessibility of the generated PDF. Opening the menu does not authorize navigation into excluded routes. Applicability questions about excluded content remain recorded without expanding execution scope.

## Source review and coverage matrix

The workbook reuses REF-02’s detailed matrix: 55 current A/AA criteria, 37 Applicable and 18 To Be Confirmed, with no closed Not Applicable decisions. It retains official English criterion names in both editions, levels, evaluation methods and test relationships. Both means partial automation plus planned human evaluation. The selected release and rule tags were verified. The matrix records partial automated rule execution for 22 criteria; all 55 criteria remain Not Evaluated and manual evaluation remains pending.

Scope reconciliation: 2.2.2 retains source applicability for the broader application because its evidence concerns the excluded Slider. Triggering content in the approved flow remains To Be Confirmed, and the excluded route is deferred. For 2.4.5, inspect approved navigation and process exceptions while deferring detail/catalog extensions. For 4.1.3, planned review covers in-scope errors/cart changes, not excluded dynamic loading. These distinctions are explicit in the matrix.

No AAA criteria or 4.1.1 Parsing are included; Parsing was removed in WCAG 2.2. Inapplicable from axe means a rule had no matching elements in that scan. It is not a WCAG N/A decision.

To close Not Applicable, record the inspected scope and states, observation date, triggering requirement and verifiable absence evidence. A missing feature, a demo label or static code inspection alone does not justify an application-wide N/A. Multimedia, sensory instructions, audio, images of text, hover/focus content, shortcuts, flashes, gestures, motion, dragging, language parts, help, order/data effects and redundant entry remain open where the source lacks evidence.

## Automated strategy: six TestNG cases

| Case ID | Page | Required scan states | Scan count |
| --- | --- | --- | --- |
| A11Y-AUTO-001 | Login | login-initial, login-invalid-credentials | 2 |
| A11Y-AUTO-002 | Products | products-initial, products-product-added, products-menu-open | 3 |
| A11Y-AUTO-003 | Cart with product | cart-with-product, cart-empty | 2 |
| A11Y-AUTO-004 | Checkout Information | checkout-information-initial, checkout-error-first-name, checkout-error-last-name, checkout-error-postal-code | 4 |
| A11Y-AUTO-005 | Checkout Overview | checkout-overview | 1 |
| A11Y-AUTO-006 | Checkout Complete | checkout-complete | 1 |

Total: 13 required axe scans inside exactly six TestNG tests. State keys are evidence identifiers, not new test-case IDs. No additional locked-user, sorting, submenu or filled-form scan is required initially.

Application available. Fresh Chrome browser, known session/cart state. Axe version and rule configuration are pinned in AccessibilityAudit. Wait explicitly for the expected state, images and fonts before scanning the full rendered page.

Prepare every case independently using public demo credentials and synthetic checkout data from Test Data. Reach Overview and Complete through the actual process. Reset form values before each missing-field variant so that only one required field is absent. Confirm the expected page/state before each scan. Collect all reachable required-state results before the final assertion where feasible; a first violation should not conceal later evidence.

Configuration pinned in AccessibilityAudit: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`. Explicitly enabled target-size and experimental rules `css-orientation-lock`, `label-content-name-mismatch`, `p-as-heading`, `table-fake-caption`, `td-has-header`. target-size is disabled by default and is not experimental. Deprecated, AAA, best-practice and obsolete rules are outside the baseline. No impact/node filtering is applied. Engine, inventory and results for all selected rules are checked. violations, passes, incomplete and inapplicable are retained.

### Automated result rule

Automated PASS requires every mandatory scan to complete in the correct state with zero violations. Any detected violation produces FAIL, including runs with technical errors or missing scans. Retain and document violations, technical errors and incomplete execution by case/state. Report navigation, setup, injection, timeout or axe failures as Technical Error; never report PASS if a mandatory scan is missing or unfinished. Preserve axe incomplete separately for human review without automatically classifying it as PASS or FAIL. A PASS covers only executed rules and states and does not establish WCAG conformance.

Keep the automated test outcome and the human-review status of incomplete separate. Zero violations can satisfy the configured automated assertion while incomplete remains pending; it cannot establish criterion compliance or whole-application conformance. A partial run never earns PASS for the case. If both violations and technical errors occur, preserve both; report FAIL for detected violations and explicitly record the incomplete execution and technical error.

## Manual strategy: ten planned categories

| ID | Category | Lifecycle | Related WCAG criteria |
| --- | --- | --- | --- |
| A11Y-MAN-001 | Keyboard Accessibility | Planned / Not Executed | 1.4.13, 2.1.1, 2.1.2, 2.1.4, 2.4.1, 2.5.1, 2.5.4, 2.5.7, 3.2.1, 3.2.2, 3.3.8 |
| A11Y-MAN-002 | Focus Visibility, Order and Obscuring | Planned / Not Executed | 1.4.11, 1.4.13, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 3.2.1 |
| A11Y-MAN-003 | Screen Reader Navigation with NVDA | Planned / Not Executed | 1.3.1, 1.3.2, 2.4.1, 2.4.2, 2.4.4, 2.4.5, 3.1.1, 3.1.2, 3.2.3, 3.2.6, 4.1.2, 4.1.3 |
| A11Y-MAN-004 | Accessible Names, Roles and States | Planned / Not Executed | 1.1.1, 2.4.4, 2.5.3, 3.2.4, 4.1.2 |
| A11Y-MAN-005 | Forms, Labels and Error Identification | Planned / Not Executed | 1.3.1, 1.3.3, 1.3.5, 1.4.1, 2.4.6, 2.5.3, 3.2.2, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7, 3.3.8 |
| A11Y-MAN-006 | Images and Non-text Content | Planned / Not Executed | 1.1.1, 1.2.1, 1.2.2, 1.2.3, 1.2.4, 1.2.5, 1.4.2, 1.4.5 |
| A11Y-MAN-007 | Headings, Structure and Meaningful Sequence | Planned / Not Executed | 1.3.1, 1.3.2, 1.3.3, 2.4.1, 2.4.2, 2.4.5, 2.4.6, 3.1.2, 3.2.3, 3.2.6 |
| A11Y-MAN-008 | Zoom, Resize, Reflow and Text Spacing | Planned / Not Executed | 1.3.4, 1.4.4, 1.4.10, 1.4.12, 2.4.11 |
| A11Y-MAN-009 | Visual Presentation, Contrast and Target Size | Planned / Not Executed | 1.4.1, 1.4.3, 1.4.5, 1.4.11, 2.2.2, 2.3.1, 2.5.1, 2.5.2, 2.5.4, 2.5.7, 2.5.8 |
| A11Y-MAN-010 | Dynamic Content, Status and Error Communication | Planned / Not Executed | 1.2.1, 1.2.4, 1.4.1, 1.4.2, 1.4.13, 2.2.1, 2.2.2, 2.3.1, 3.2.2, 3.3.1, 3.3.3, 3.3.4, 3.3.7, 4.1.2, 4.1.3 |

Detailed future procedures and expected results are in Manual Accessibility. All ten categories remain Planned / Not Executed. Mappings are synchronized with the coverage matrix, including conditional relationships that require applicability confirmation. M009 does not add AAA criterion 1.4.8.

Use Chrome with NVDA, keyboard-only interaction, accessible-property inspection and contrast/target measurement. Record actual OS, browser, NVDA, viewport, zoom and tool versions. Authentication assistance must be evaluated in a browser configuration that allows it: the password-manager restrictions reported for functional DriverFactory do not prove support or lack of support for 3.3.8.

Manual measurable conditions: text enlargement to 200%; vertical-flow reflow at 320 CSS px width (horizontal flow at 256 CSS px height); line height 1.5×, paragraph spacing 2×, letter spacing 0.12× and word spacing 0.16× font size. Normal text contrast ≥4.5:1, large text ≥3:1 (18 pt regular or 14 pt bold), required components/graphics ≥3:1. Pointer targets meet 24×24 CSS px or a permitted documented exception, including spacing. Apply the criterion-specific exceptions.

## Evidence and Allure contract

For each case and scan preserve: run ID, timestamp, case ID, state key, URL, environment, axe version/configuration, preparation completion and scan execution status. Attach structured axe output including violations, passes, incomplete and inapplicable. Violation records include rule ID, WCAG tags, impact, description/help URL, affected nodes/selectors/HTML and failure summaries. Identify screenshot/URL by the state where evidence was captured. Preserve technical errors with stage, exception, message and stack trace. Screenshots support evidence but do not substitute for the structured scan.

AccessibilityEvidenceListener attaches scan JSONs and case manifests before Allure closes the result, including unexpected method termination. FailureEvidenceListener retains its screenshot/URL behavior unchanged. Original errors are preserved. Reporting stays outside Page Objects and tests; tests prepare states and request audits.

## Verified execution modes and completion

| Mode | Expected tests | Implementation |
| --- | --- | --- |
| Functional | 15 | Verified |
| Accessibility | 6 | Verified |
| All | 21 | Verified |

Verified modes without profiles or suite XML: Functional `mvn clean test` (15); Accessibility `mvn clean test "-Dtest=AccessibilityTest"` (6); All `mvn clean test "-Dtest=*Test"` (21). Surefire 3.5.6 defaults to com/david/qa/tests/*Test.java; -Dtest overrides this inclusion. Run mvn allure:report or mvn allure:serve after testing without an intermediate clean. Each fresh mode starts with clean test; preserve evidence before cleaning. Manual execution remains pending.

## Deliverables and references

English is primary repository documentation; Spanish is the equivalent translation. Each workbook has exactly four sheets: Automated Accessibility, Manual Accessibility, Test Data and WCAG Coverage Matrix. Read the matching Test Results document for the initial execution baseline. All six files remain editable.

- REF-01 (historical 2026-10-08 baseline): Embedded approved project contract. Documentation only for qa-saucedemo-portfolio: 15 existing functional tests using Java 25, Selenium, TestNG, Maven, Page Object Model and Allure. Initial scope: Login → Products → Cart → Checkout Information → Checkout Overview → Checkout Complete, including the defined errors, cart changes and open side menu. Exactly six automated cases with thirteen required scans, ten manual categories, four sheets per workbook and fifty-five WCAG 2.2 A/AA criteria; planned future Maven selections: Functional=15, Accessibility=6, All=21. Additional dynamic/long catalogs, product detail, Slider/Spinner, PDF generation and generated-PDF accessibility are excluded; a rendered PDF control is included. Preserve the provisional 37 Applicable / 18 To Be Confirmed classification, Not Executed / Not Evaluated baseline, separate status dimensions and bilingual equivalence. No implementation, execution evidence or conformance claim is implied.
- REF-02: Embedded historical technical baseline, not current verification. §1 Project observations: 15 functional tests; Selenium 4.49.0, TestNG 7.12.0, Allure TestNG 3.0.0 and Surefire 3.5.6; no axe integration or independent suite selections. The functional listener records failure screenshot/URL, not axe data; DriverFactory restricts password-manager assistance. §2 Static application observations: lang=en, title Swag Labs, product/confirmation images and graphical controls, cart badge/name changes, side menu/submenu, required-field validation and role=alert errors with a dismissal control. A 600-second session cookie and guarded routes were reported; the excluded Slider updates every two seconds and Spinner uses role=status. Completion conditionally renders a PDF control. Criterion-specific observations and scope limits are reproduced in the WCAG Coverage Matrix; they are not rendered-state test results. Browser interaction was unavailable, and inspection date/build reference were not recorded. §3 Public demo credentials and synthetic checkout data are reproduced in Test Data. These historical observations are not independently reverified in this revision; REF-03 provides the public normative requirements.
- REF-03: [W3C WCAG 2.2 specification](https://www.w3.org/TR/WCAG22/), consulted 2026-10-08 for criterion names, levels and normative requirements.
- REF-04: [axe-core rule descriptions](https://github.com/dequelabs/axe-core/blob/v4.13.0/doc/rule-descriptions.md) and [axe-core API](https://github.com/dequelabs/axe-core/blob/v4.13.0/doc/API.md). Rule inventory verified against pinned release 4.13.0; criterion mappings remain partial coverage.
