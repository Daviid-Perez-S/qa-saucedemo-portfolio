# Resultados de pruebas de accesibilidad

Versión: 1.1. Ejecución local: 2026-10-09 (UTC−06:00). Línea base: WCAG 2.2 A/AA.

Se implementaron y verificaron seis métodos TestNG y trece scans. Las ejecuciones finales no detectaron violaciones; todos los scans obligatorios terminaron en el estado esperado. Esto no establece conformidad WCAG 2.2 AA. Las diez categorías manuales permanecen Planned / Not Executed y Compliance Result permanece Not Evaluated.

## Ejecuciones verificadas

| Mode | Command | Tests | PASS | FAIL / Broken / Skipped | Scans | Allure results |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| Functional | `mvn clean test` | 15 | 15 | 0 / 0 / 0 | 0 | 15 |
| Accessibility | `mvn clean test "-Dtest=AccessibilityTest"` | 6 | 6 | 0 / 0 / 0 | 13 | 6 |
| All | `mvn clean test "-Dtest=*Test"` | 21 | 21 | 0 / 0 / 0 | 13 | 21 |

Los tres comandos terminaron con BUILD SUCCESS. Un resultado por método, sin resultados duplicados. Cada ejecución con accesibilidad conserva 13 JSON por scan y 6 manifiestos (19 adjuntos), sin screenshots de éxito. Se generó Allure Report 3.20.0 para la ejecución All.

## Resultados por caso

| ID | Required / completed scans | Implementation Status | Execution Status | Automated outcome | Compliance Result |
| --- | --- | --- | --- | --- | --- |
| A11Y-AUTO-001 | 2 / 2 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-002 | 3 / 3 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-003 | 2 / 2 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-004 | 4 / 4 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-005 | 1 / 1 | Implemented / Verified | Executed | PASS | Not Evaluated |
| A11Y-AUTO-006 | 1 / 1 | Implemented / Verified | Executed | PASS | Not Evaluated |

## Hallazgos por estado

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

Violaciones: 0, reglas distintas con violaciones: 0, nodos con violaciones: 0. Errores técnicos finales: 0. Hay 4 ocurrencias de regla incomplete en 4 estados, con 7 ocurrencias de nodos; no se deduplican entre estados. `color-contrast` requiere revisión humana de los elementos y fondos; no se transforma en PASS de contraste ni en defecto confirmado. Los selectores y checks completos están en los JSON. `passes` e `inapplicable` se conservan íntegros y no equivalen a conformidad ni a WCAG Not Applicable.

## Entorno y evidencia

- Java `25.0.4.1`; Selenium `4.49.0`; TestNG `7.12.0`; Allure TestNG `3.0.0`; Surefire `3.5.6` (native TestNG provider).
- axe Java integration / engine `4.13.0`; Allure Maven Plugin `3.1.0`; Report `3.20.0`.
- Dependencias transitivas efectivas: deque `utilities 4.13.0`, `commons-io 2.22.0`, `commons-lang3 3.20.0`, Jackson `databind/core 2.22.1` y `annotations 2.22`. Solo se excluyó WebDriverManager; Maven seleccionó Selenium directo `4.49.0` sobre el transitivo `4.13.0`.
- Windows 11 10.0; Chrome `154.0.8037.99`; viewport `1036×647` CSS px; devicePixelRatio `1.25`; visualViewportScale `1`.
- Tags: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`.
- Experimental enabled: `css-orientation-lock`, `label-content-name-mismatch`, `p-as-heading`, `table-fake-caption`, `td-has-header`.
- `target-size`: enabled explicitly; disabled by default, **not experimental** in the selected engine.
- All run ID: `1c39d6a1-dbad-4010-b900-7f92101f27a8`. UTC scan timestamps: `2026-10-10T01:35:49.403Z` to `2026-10-10T01:36:11.155Z`.
- Baseline commit: `332af2851839bd4f906998b7ae5a362176a3b6fd` plus uncommitted implementation; source hashes recorded in the summary.

[Resumen de ejecución verificable](accessibility-execution-summary.json) con IDs de casos, versiones, hashes, configuración de auditoría, resultados por estado y revisiones humanas pendientes. Los identificadores locales de Allure y nombres de adjuntos se omiten de este resumen público. Evidencia local de All: `target/allure-results/`; reporte: `target/allure-report/`. Copias locales de las tres ejecuciones: `.accessibility-verification/functional-final/`, `.accessibility-verification/accessibility-final/` y `.accessibility-verification/all-final/`, ignoradas por Git. No se publicó URL de reporte. `clean` elimina target: conservar/exportar evidencia antes de una nueva ejecución.

## Verificación del contrato y limitaciones

Ocho comprobaciones sintéticas, fuera de las suites y evidencia real de SauceDemo, verificaron PASS, violaciones, error técnico, scan faltante, resultado inválido, resultado mixto, continuación tras una violación y aborto inesperado. Allure clasificó AssertionError como failed y errores técnicos como broken; conservó la excepción original en el caso inesperado. Una página sintética separada con dos botones de 8×8 CSS px produjo target-size serious en dos nodos. Estos hallazgos no son defectos de SauceDemo.

Durante el desarrollo, la validación inicial rechazó una regla presente en más de una categoría; se corrigió para permitir categorías distintas por nodo. También se observó un error técnico al encadenar variantes de checkout con clear(): el formulario avanzó a Overview. La selección y borrado por teclado corrigieron la preparación y las ejecuciones finales completaron las cuatro variantes. FailureEvidenceListener permaneció intacto y se verificó su captura/URL en el fallo técnico real de desarrollo.

Chrome 154 produjo una advertencia CDP (Selenium dispone de 153); los flujos WebDriver y scans terminaron correctamente y no utilizan CDP. SLF4J reportó ausencia de provider; no se añadió logging. No hay errores técnicos finales pendientes. La escala visualViewport se registró; el zoom de escritorio de Chrome no se midió por separado. Los cuatro incomplete, las reglas experimentales y las diez categorías manuales requieren atención antes de concluir sobre accesibilidad.

## Registro de defectos

No se documentan defectos de accesibilidad confirmados. Cero violaciones automáticas no cierra incomplete ni la evaluación manual.

## Estado de evaluación manual

| ID | Categoría | Implementation Status | Execution Status | Ciclo | Compliance Result | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-MAN-001 | Accesibilidad mediante teclado | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-002 | Visibilidad, orden y ocultamiento del foco | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-003 | Navegación con lector de pantalla NVDA | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-004 | Nombres, roles y estados accesibles | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-005 | Formularios, etiquetas e identificación de errores | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-006 | Imágenes y contenido no textual | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-007 | Encabezados, estructura y secuencia significativa | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-008 | Zoom, ampliación, reflow y espaciado del texto | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-009 | Presentación visual, contraste y tamaño de objetivos | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |
| A11Y-MAN-010 | Contenido dinámico y comunicación de estados y errores | Planned | Not Executed | Planned / Not Executed | Not Evaluated | Not Available |

Los resultados esperados del workbook son objetivos de aceptación futuros, no observaciones. Ninguna categoría manual ha aprobado o fallado.

## Cobertura conservada

Se mantienen seis casos, trece estados y 55 criterios A/AA: 37 Applicable y 18 To Be Confirmed; ningún N/A cerrado. Se conservan las rutas excluidas, incluida la evaluación del PDF generado. Un control PDF renderizado se incluye únicamente en el scan de Complete. Las relaciones de la matriz son cobertura parcial, no prueba de conformidad. No se ejecutó NVDA ni evaluación manual.

La matriz registra ejecución parcial de reglas automáticas para 22 criterios, incluidos resultados inapplicable de axe; esto no determina su aplicabilidad WCAG ni evalúa completamente un criterio. Los 55 criterios permanecen Not Evaluated.
