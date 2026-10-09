# Accessibility Test Results

Project: `qa-saucedemo-portfolio`  
Application: https://www.saucedemo.com/  
Document version: 1.0  
Documentation baseline date: 2026-10-08  
Evaluation target: WCAG 2.2 A / AA

## Current baseline

No accessibility execution results are available. Axe integration and the six accessibility TestNG cases are Planned / Not Implemented. No PASS, FAIL, accessibility defect, screenshot or Allure accessibility run is reported. Source-code observations in REF-02 are not accessibility test results. The 15 existing functional tests are outside the accessibility result counts and were not rerun here.

Status values are identical in both editions: Implementation Status = Planned / Not Implemented (automated) or Planned (manual); Execution Status = Not Executed; Compliance Result = Not Evaluated. Manual lifecycle is Planned / Not Executed. Applicable and To Be Confirmed describe preliminary applicability, not compliance.

## Automated case results

| ID | Case | Required scans | Implementation Status | Execution Status | Automated outcome | Compliance Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A11Y-AUTO-001 | Login | 2 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | Not available — no run |
| A11Y-AUTO-002 | Products | 3 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | Not available — no run |
| A11Y-AUTO-003 | Cart with product | 2 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | Not available — no run |
| A11Y-AUTO-004 | Checkout Information | 4 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | Not available — no run |
| A11Y-AUTO-005 | Checkout Overview | 1 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | Not available — no run |
| A11Y-AUTO-006 | Checkout Complete | 1 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | Not available — no run |

Planned scope: six tests and thirteen scans. Completed run count and executed scan count are not available. Planned counts are not execution evidence.

## Violations, technical errors and incomplete

| Metric | Current value | Reason |
| --- | --- | --- |
| Axe violations and impact breakdown | Not Available | Axe has not been executed |
| Affected nodes and rule counts | Not Available | No structured scan output |
| Technical errors | Not Available | No accessibility run |
| incomplete | Not Available | No scan output to review |
| passes / inapplicable | Not Available | No scan output; neither establishes WCAG conformance |
| Confirmed defects | Not Available | No executed evaluation from which to report defects |

Missing results are not zero violations. On execution, count violations, distinct rules, affected nodes and incomplete separately, retaining state identity. Document any deduplication used across states. Technical errors must never be counted as WCAG violations.

### Interpretation after future execution

Automated PASS requires every mandatory scan to complete in the correct state with zero violations. Any detected violation produces FAIL, including runs with technical errors or missing scans. Retain and document violations, technical errors and incomplete execution by case/state. Report navigation, setup, injection, timeout or axe failures as Technical Error; never report PASS if a mandatory scan is missing or unfinished. Preserve axe incomplete separately for human review without automatically classifying it as PASS or FAIL. A PASS covers only executed rules and states and does not establish WCAG conformance.

Track incomplete review as Pending, Reviewed or Resolved independently of the automated assertion. A zero-violation automated PASS with pending incomplete still requires human review and never changes Compliance Result to conformant. Preserve both detected violations and any technical error in a partially completed case.

## Run and evidence register

| Field | Current value / future requirement |
| --- | --- |
| Run ID / execution timestamp | Not Available |
| Commit or deployed build reference | Not Available |
| OS / Chrome / viewport / zoom | Not Available |
| axe-core / Java integration / enabled tags and rules | Not Selected / Not Implemented |
| NVDA / manual tools | Not Recorded — Not Executed |
| Allure report URL / run reference | Not Available |
| Evidence location | Not Available |

For the next real run, attach structured axe data for every case/state: URL, timestamp, versions/configuration, rule ID, impact, tags/help URL, affected nodes and failure summaries, plus passes, incomplete and inapplicable. Include stage and exception details for technical errors. A screenshot and URL must identify the captured state; no placeholder evidence links are provided.

## Defect register

No defect entries have been created because no accessibility evaluation has been executed. Add rows only when a real issue is identified. Future records must include defect ID, run, case and state, title, rule/SC, impact and triage priority, URL, affected element, reproduction steps, expected/actual behavior, evidence link, disposition and retest outcome. A tool violation is evidence for triage; it must not be silently equated with whole-criterion failure without contextual review.

| Defect ID | Case / state | SC / rule | Actual behavior | Evidence | Status / retest |
| --- | --- | --- | --- | --- | --- |


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

## Coverage and limitations

| Case ID | Page | Required scan states | Scan count |
| --- | --- | --- | --- |
| A11Y-AUTO-001 | Login | login-initial, login-invalid-credentials | 2 |
| A11Y-AUTO-002 | Products | products-initial, products-product-added, products-menu-open | 3 |
| A11Y-AUTO-003 | Cart with product | cart-with-product, cart-empty | 2 |
| A11Y-AUTO-004 | Checkout Information | checkout-information-initial, checkout-error-first-name, checkout-error-last-name, checkout-error-postal-code | 4 |
| A11Y-AUTO-005 | Checkout Overview | checkout-overview | 1 |
| A11Y-AUTO-006 | Checkout Complete | checkout-complete | 1 |

The matrix retains 55 A/AA criteria, with 37 preliminarily Applicable and 18 To Be Confirmed. No N/A is closed. For 2.2.2, source evidence relates to the excluded Slider, so broader applicability does not create completed or planned initial-route coverage. Product detail references for 2.4.5 are deferred. Six future tests cover representative main-flow states, not all WCAG requirements or the entire application.

Excluded: additional dynamic/long catalogs, product detail, additional Slider/Spinner, PDF generation and generated-PDF accessibility. A PDF control rendered on Complete is included in that page scan. Keyboard behavior, focus, NVDA announcements, reflow, spacing, timing and semantic adequacy require the planned human evaluation. Static lang, title, ARIA or alternative-text observations do not establish compliance.

## Update procedure

1. Implement and verify accessibility integration and independent Maven selections: Functional=15, Accessibility=6, All=21. Add definitive commands only after validation.
2. Record the actual run/environment and all thirteen required state outcomes, with Allure evidence.
3. Update implementation, execution and automated outcomes independently of compliance.
4. Triage real violations and technical errors, review incomplete and link real defects/retests.
5. Perform manual categories separately; update only those actually executed and retain unverified applicability questions.
6. Synchronize both language editions and workbook rows by stable IDs. Report “no violations detected by the executed rules and states” only when supported. Do not claim SauceDemo WCAG 2.2 AA conformance.

## References

- REF-01: Embedded approved project contract. Documentation only for qa-saucedemo-portfolio: 15 existing functional tests using Java 25, Selenium, TestNG, Maven, Page Object Model and Allure. Initial scope: Login → Products → Cart → Checkout Information → Checkout Overview → Checkout Complete, including the defined errors, cart changes and open side menu. Exactly six automated cases with thirteen required scans, ten manual categories, four sheets per workbook and fifty-five WCAG 2.2 A/AA criteria; planned future Maven selections: Functional=15, Accessibility=6, All=21. Additional dynamic/long catalogs, product detail, Slider/Spinner, PDF generation and generated-PDF accessibility are excluded; a rendered PDF control is included. Preserve the provisional 37 Applicable / 18 To Be Confirmed classification, Not Executed / Not Evaluated baseline, separate status dimensions and bilingual equivalence. No implementation, execution evidence or conformance claim is implied.
- REF-02: Embedded historical technical baseline, not current verification. §1 Project observations: 15 functional tests; Selenium 4.49.0, TestNG 7.12.0, Allure TestNG 3.0.0 and Surefire 3.5.6; no axe integration or independent suite selections. The functional listener records failure screenshot/URL, not axe data; DriverFactory restricts password-manager assistance. §2 Static application observations: lang=en, title Swag Labs, product/confirmation images and graphical controls, cart badge/name changes, side menu/submenu, required-field validation and role=alert errors with a dismissal control. A 600-second session cookie and guarded routes were reported; the excluded Slider updates every two seconds and Spinner uses role=status. Completion conditionally renders a PDF control. Criterion-specific observations and scope limits are reproduced in the WCAG Coverage Matrix; they are not rendered-state test results. Browser interaction was unavailable, and inspection date/build reference were not recorded. §3 Public demo credentials and synthetic checkout data are reproduced in Test Data. These historical observations are not independently reverified in this revision; REF-03 provides the public normative requirements.
- REF-03: [W3C WCAG 2.2 specification](https://www.w3.org/TR/WCAG22/), consulted 2026-10-08 for criterion names, levels and normative requirements.
- REF-04: [axe-core rule descriptions](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md) and [axe-core API](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md). Future mapping must use the selected release, not an unpinned development branch.
