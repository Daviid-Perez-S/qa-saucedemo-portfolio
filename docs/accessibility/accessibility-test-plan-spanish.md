# Plan de pruebas de accesibilidad

Proyecto: `qa-saucedemo-portfolio`  
Aplicación: https://www.saucedemo.com/  
Versión del documento: 1.1
Fecha de actualización: 2026-10-09
Línea base: WCAG 2.2 A / AA

## Propósito y estado actual

Definir la evaluación de accesibilidad del proceso principal de compra. La integración axe y los seis casos automatizados con trece scans fueron implementados y verificados el 2026-10-09. Consultar Test Results para resultados reales. La evaluación manual sigue pendiente y no se establece conformidad WCAG 2.2 AA.

Estados automatizados: Implementation Status = Implemented / Verified; Execution Status = Executed. Resultado automático separado de Compliance Result = Not Evaluated. Ciclo manual: Planned / Not Executed. Applicable y To Be Confirmed siguen siendo aplicabilidad preliminar.

Se verificó mediante Maven Java 25.0.4.1, Selenium 4.49.0, TestNG 7.12.0, Allure TestNG 3.0.0 y Surefire 3.5.6. Se utiliza com.deque.html.axe-core:selenium:4.13.0 y motor axe-core 4.13.0. Solo se excluye WebDriverManager. La mediación Maven selecciona Selenium directo 4.49.0 sobre el transitivo 4.13.0; se conserva DriverFactory/Selenium Manager.

## Alcance

Login → Products → Cart → Checkout Information → Checkout Overview → Checkout Complete.

Incluir páginas iniciales, error de credenciales inválidas, adición/eliminación del carrito, los tres errores individuales de campos obligatorios y menú lateral abierto. Los procedimientos manuales también examinan ordenamiento y transiciones dentro de estas páginas. El escaneo completo incluye el control PDF solo si está renderizado al finalizar.

Excluidos inicialmente: catálogos dinámicos adicionales, catálogo largo, detalle individual de producto, rutas Slider/Spinner adicionales, generación del PDF y accesibilidad del PDF generado. Abrir menú no autoriza navegar a rutas excluidas. Se conservan preguntas de aplicabilidad sobre contenido excluido sin ampliar ejecución.

## Revisión de la fuente y matriz de cobertura

El workbook reutiliza la matriz detallada de REF-02: 55 criterios A/AA vigentes, 37 Applicable y 18 To Be Confirmed, sin decisiones Not Applicable cerradas. Conserva nombres oficiales ingleses en ambas ediciones, niveles, métodos y relaciones con casos. Both significa automatización parcial más evaluación humana planificada. Se verificaron versión y etiquetas axe. La matriz registra ejecución parcial de reglas automáticas para 22 criterios; los 55 criterios permanecen Not Evaluated y la evaluación manual sigue pendiente.

Conciliación del alcance: 2.2.2 conserva aplicabilidad de la fuente para la aplicación ampliada porque su evidencia es el Slider excluido. El contenido que active el requisito en el flujo aprobado está To Be Confirmed y la ruta excluida queda diferida. En 2.4.5, revisar navegación aprobada y excepciones del proceso; diferir detalle/extensiones de catálogo. En 4.1.3, revisar errores/carrito dentro de alcance, no carga dinámica excluida. La matriz explicita estas distinciones.

No se incluyen criterios AAA ni 4.1.1 Parsing, eliminado en WCAG 2.2. Inapplicable de axe significa que una regla no encontró elementos coincidentes en ese escaneo. No equivale a N/A de WCAG.

Para cerrar Not Applicable, registrar alcance/estados inspeccionados, fecha, condición que activa el requisito y evidencia verificable de ausencia. Una función faltante, la etiqueta demo o inspección estática aislada no justifican N/A de toda la aplicación. Permanecen abiertos multimedia, instrucciones sensoriales, audio, imágenes de texto, contenido hover/focus, atajos, destellos, gestos, movimiento, arrastre, idiomas de partes, ayuda, efectos del pedido/datos y entrada redundante donde falta evidencia.

## Estrategia automatizada: seis casos TestNG

| ID del caso | Página | Estados obligatorios | N.º de escaneos |
| --- | --- | --- | --- |
| A11Y-AUTO-001 | Login | login-initial, login-invalid-credentials | 2 |
| A11Y-AUTO-002 | Productos | products-initial, products-product-added, products-menu-open | 3 |
| A11Y-AUTO-003 | Carrito con producto | cart-with-product, cart-empty | 2 |
| A11Y-AUTO-004 | Información de checkout | checkout-information-initial, checkout-error-first-name, checkout-error-last-name, checkout-error-postal-code | 4 |
| A11Y-AUTO-005 | Resumen de checkout | checkout-overview | 1 |
| A11Y-AUTO-006 | Checkout completado | checkout-complete | 1 |

Total: 13 escaneos axe obligatorios dentro de exactamente seis tests TestNG. Las claves de estado identifican evidencia, no nuevos casos. No se requiere inicialmente escaneo adicional de usuario bloqueado, ordenamiento, submenú ni formulario completo.

Aplicación disponible. Chrome nuevo y estado conocido de sesión/carrito. La versión y configuración axe están fijadas en AccessibilityAudit. Esperar explícitamente el estado esperado, imágenes y fuentes antes de escanear la página renderizada completa.

Preparar cada caso de forma independiente con credenciales públicas y datos sintéticos de Test Data. Llegar a Resumen y Confirmación por el proceso real. Restablecer campos antes de cada variante para omitir solo uno. Confirmar página/estado antes de cada escaneo. Recopilar resultados de todos los estados obligatorios alcanzables antes de la aserción final cuando sea posible; una primera violación no debe ocultar evidencia posterior.

Configuración fijada en AccessibilityAudit: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`. Habilitación explícita de target-size y las experimentales `css-orientation-lock`, `label-content-name-mismatch`, `p-as-heading`, `table-fake-caption`, `td-has-header`. target-size está deshabilitada por defecto y no es experimental. Las reglas deprecadas, AAA, best-practice y obsolete quedan fuera de la línea base. No se filtran impactos ni nodos. Se comprueban motor, inventario y presencia de resultados de todas las reglas seleccionadas. Se conservan violations, passes, incomplete e inapplicable.

### Regla del resultado automatizado

PASS automatizado requiere que todos los escaneos obligatorios finalicen en el estado correcto con cero violaciones. Cualquier violación detectada produce FAIL, incluso en ejecuciones con errores técnicos o escaneos faltantes. Conservar y documentar violaciones, errores técnicos y ejecución incompleta por caso/estado. Reportar fallos de navegación, preparación, inyección, timeout o axe como Technical Error; nunca reportar PASS si falta un escaneo obligatorio o queda sin finalizar. Conservar axe incomplete por separado para revisión humana sin clasificarlo automáticamente como PASS o FAIL. PASS solo cubre reglas y estados ejecutados y no establece conformidad WCAG.

Separar resultado automatizado y revisión humana de incomplete. Cero violaciones puede satisfacer la aserción configurada mientras incomplete sigue pendiente; no establece conformidad de un criterio ni de toda la aplicación. Una ejecución parcial nunca obtiene PASS del caso. Si coexisten violaciones y errores técnicos, conservar ambos; reportar FAIL por las violaciones y registrar ejecución incompleta/error técnico.

## Estrategia manual: diez categorías planificadas

| ID | Categoría | Ciclo | Criterios WCAG relacionados |
| --- | --- | --- | --- |
| A11Y-MAN-001 | Accesibilidad mediante teclado | Planned / Not Executed | 1.4.13, 2.1.1, 2.1.2, 2.1.4, 2.4.1, 2.5.1, 2.5.4, 2.5.7, 3.2.1, 3.2.2, 3.3.8 |
| A11Y-MAN-002 | Visibilidad, orden y ocultamiento del foco | Planned / Not Executed | 1.4.11, 1.4.13, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 3.2.1 |
| A11Y-MAN-003 | Navegación con lector de pantalla NVDA | Planned / Not Executed | 1.3.1, 1.3.2, 2.4.1, 2.4.2, 2.4.4, 2.4.5, 3.1.1, 3.1.2, 3.2.3, 3.2.6, 4.1.2, 4.1.3 |
| A11Y-MAN-004 | Nombres, roles y estados accesibles | Planned / Not Executed | 1.1.1, 2.4.4, 2.5.3, 3.2.4, 4.1.2 |
| A11Y-MAN-005 | Formularios, etiquetas e identificación de errores | Planned / Not Executed | 1.3.1, 1.3.3, 1.3.5, 1.4.1, 2.4.6, 2.5.3, 3.2.2, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7, 3.3.8 |
| A11Y-MAN-006 | Imágenes y contenido no textual | Planned / Not Executed | 1.1.1, 1.2.1, 1.2.2, 1.2.3, 1.2.4, 1.2.5, 1.4.2, 1.4.5 |
| A11Y-MAN-007 | Encabezados, estructura y secuencia significativa | Planned / Not Executed | 1.3.1, 1.3.2, 1.3.3, 2.4.1, 2.4.2, 2.4.5, 2.4.6, 3.1.2, 3.2.3, 3.2.6 |
| A11Y-MAN-008 | Zoom, ampliación, reflow y espaciado del texto | Planned / Not Executed | 1.3.4, 1.4.4, 1.4.10, 1.4.12, 2.4.11 |
| A11Y-MAN-009 | Presentación visual, contraste y tamaño de objetivos | Planned / Not Executed | 1.4.1, 1.4.3, 1.4.5, 1.4.11, 2.2.2, 2.3.1, 2.5.1, 2.5.2, 2.5.4, 2.5.7, 2.5.8 |
| A11Y-MAN-010 | Contenido dinámico y comunicación de estados y errores | Planned / Not Executed | 1.2.1, 1.2.4, 1.4.1, 1.4.2, 1.4.13, 2.2.1, 2.2.2, 2.3.1, 3.2.2, 3.3.1, 3.3.3, 3.3.4, 3.3.7, 4.1.2, 4.1.3 |

Los procedimientos futuros y resultados esperados detallados están en Manual Accessibility. Las diez categorías permanecen Planned / Not Executed. Las relaciones están sincronizadas con la matriz, incluidas las condicionales que requieren confirmar aplicabilidad. M009 no incorpora el criterio AAA 1.4.8.

Usar Chrome con NVDA, interacción solo por teclado, inspección de propiedades accesibles y medición de contraste/objetivos. Registrar SO, navegador, NVDA, viewport, zoom y versiones reales. Evaluar asistencia de autenticación con configuración que la permita: las restricciones del administrador de contraseñas reportadas en DriverFactory funcional no prueban soporte ni ausencia de soporte para 3.3.8.

Condiciones manuales medibles: texto hasta 200%; reflow vertical a 320 CSS px de ancho (horizontal a 256 CSS px de alto); interlineado 1,5×, párrafos 2×, letras 0,12× y palabras 0,16× del tamaño de fuente. Contraste normal ≥4,5:1, texto grande ≥3:1 (18 pt regular o 14 pt negrita), componentes/gráficos pertinentes ≥3:1. Objetivos de 24×24 CSS px o excepción permitida documentada, incluido espaciado. Aplicar excepciones de cada criterio.

## Contrato de evidencia y Allure

Por caso y escaneo conservar: ID de ejecución, fecha/hora, ID del caso, clave de estado, URL, entorno, versión/configuración axe, preparación y estado de ejecución. Adjuntar salida axe estructurada con violations, passes, incomplete e inapplicable. Las violaciones incluyen regla, etiquetas WCAG, impacto, descripción/URL de ayuda, nodos/selectores/HTML y resumen de fallo. Asociar captura/URL al estado donde se obtuvo evidencia. Conservar errores técnicos con etapa, excepción, mensaje y traza. Las capturas apoyan evidencia pero no sustituyen salida estructurada.

AccessibilityEvidenceListener registra JSON por scan y manifiesto por caso antes del cierre Allure, incluso si el método aborta. FailureEvidenceListener conserva sus screenshots/URL sin modificaciones. Los errores originales se conservan. Reporting permanece fuera de Page Objects y tests; los tests solo preparan estados y solicitan análisis.

## Modos de ejecución verificados y cierre

| Modo | Tests previstos | Implementación |
| --- | --- | --- |
| Functional | 15 | Verified |
| Accessibility | 6 | Verified |
| All | 21 | Verified |

Modos verificados sin perfiles ni suite XML: Functional `mvn clean test` (15); Accessibility `mvn clean test "-Dtest=AccessibilityTest"` (6); All `mvn clean test "-Dtest=*Test"` (21). Surefire 3.5.6 incluye por defecto com/david/qa/tests/*Test.java y -Dtest sustituye esa inclusión. Ejecutar mvn allure:report o mvn allure:serve después del test, sin clean intermedio. Cada nuevo modo empieza con clean test; conservar evidencia antes de limpiar. La ejecución manual sigue pendiente.

## Entregables y referencias

Inglés es la documentación principal del repositorio; español es traducción equivalente. Cada workbook contiene exactamente cuatro hojas: Automated Accessibility, Manual Accessibility, Test Data y WCAG Coverage Matrix. Consultar Test Results de la misma edición para línea base de ejecución. Los seis archivos son editables.

- REF-01 (línea base histórica del 2026-10-08): Contrato aprobado incorporado. Solo documentación para qa-saucedemo-portfolio: 15 tests funcionales existentes con Java 25, Selenium, TestNG, Maven, Page Object Model y Allure. Alcance inicial: Login → Products → Cart → Checkout Information → Checkout Overview → Checkout Complete, incluidos errores definidos, cambios del carrito y menú lateral abierto. Exactamente seis casos automatizados con trece escaneos obligatorios, diez categorías manuales, cuatro hojas por workbook y cincuenta y cinco criterios WCAG 2.2 A/AA; selecciones Maven futuras: Functional=15, Accessibility=6, All=21. Se excluyen catálogos adicionales dinámicos/largo, detalle, Slider/Spinner, generación del PDF y accesibilidad del PDF generado; se incluye el control PDF renderizado. Conservar clasificación provisional 37 Applicable / 18 To Be Confirmed, línea base Not Executed / Not Evaluated, dimensiones de estado separadas y equivalencia bilingüe. No implica implementación, evidencia de ejecución ni conformidad.
- REF-02: Línea base técnica histórica incorporada, no verificación actual. §1 Observaciones del proyecto: 15 tests funcionales; Selenium 4.49.0, TestNG 7.12.0, Allure TestNG 3.0.0 y Surefire 3.5.6; sin integración axe ni selecciones independientes de suites. El listener funcional registra captura/URL de fallo, no datos axe; DriverFactory restringe asistencia del administrador de contraseñas. §2 Observaciones estáticas: lang=en, título Swag Labs, imágenes de productos/confirmación y controles gráficos, cambios de badge/nombre del carrito, menú/submenú, validación obligatoria y errores role=alert con control para descartarlos. Se reportaron cookie de sesión de 600 segundos y rutas protegidas; Slider excluido actualiza cada dos segundos y Spinner usa role=status. Confirmación renderiza un control PDF de forma condicional. La WCAG Coverage Matrix reproduce observaciones por criterio y límites de alcance; no son resultados de estados renderizados. La interacción en navegador no estuvo disponible y no se registraron fecha ni referencia de versión inspeccionada. §3 Credenciales públicas de demo y datos sintéticos de checkout se reproducen en Test Data. No se verifican nuevamente estas observaciones históricas en esta revisión; REF-03 proporciona requisitos normativos públicos.
- REF-03: [Especificación W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/), consultada el 2026-10-08 para nombres, niveles y requisitos normativos.
- REF-04: [Reglas de axe-core](https://github.com/dequelabs/axe-core/blob/v4.13.0/doc/rule-descriptions.md) y [API de axe-core](https://github.com/dequelabs/axe-core/blob/v4.13.0/doc/API.md). Inventario verificado con la versión fijada 4.13.0; las relaciones de criterios siguen siendo cobertura parcial.
