# Resultados de pruebas de accesibilidad

Proyecto: `qa-saucedemo-portfolio`  
Aplicación: https://www.saucedemo.com/  
Versión del documento: 1.0  
Fecha de línea base documental: 2026-10-08  
Estándar previsto: WCAG 2.2 A / AA

## Línea base actual

No hay resultados de ejecución de accesibilidad. Integración axe y seis casos TestNG de accesibilidad: Planned / Not Implemented. No se reportan PASS, FAIL, defectos de accesibilidad, capturas ni ejecución Allure de accesibilidad. Las observaciones de código de REF-02 no son resultados de accesibilidad. Los 15 tests funcionales existentes quedan fuera de estos conteos y no se reejecutaron aquí.

Los estados son idénticos en ambas ediciones: Implementation Status = Planned / Not Implemented (automatizado) o Planned (manual); Execution Status = Not Executed; Compliance Result = Not Evaluated. Ciclo manual: Planned / Not Executed. Applicable (aplicable) y To Be Confirmed (por confirmar) describen aplicabilidad preliminar, no conformidad.

## Resultados de casos automatizados

| ID | Caso | Escaneos previstos | Implementation Status | Execution Status | Resultado automatizado | Compliance Result | Evidencia |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A11Y-AUTO-001 | Login | 2 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | No disponible — sin ejecución |
| A11Y-AUTO-002 | Productos | 3 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | No disponible — sin ejecución |
| A11Y-AUTO-003 | Carrito con producto | 2 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | No disponible — sin ejecución |
| A11Y-AUTO-004 | Información de checkout | 4 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | No disponible — sin ejecución |
| A11Y-AUTO-005 | Resumen de checkout | 1 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | No disponible — sin ejecución |
| A11Y-AUTO-006 | Checkout completado | 1 | Planned / Not Implemented | Not Executed | Not Available | Not Evaluated | No disponible — sin ejecución |

Alcance planificado: seis tests y trece escaneos. No están disponibles conteos de ejecuciones completadas ni escaneos ejecutados. Los conteos planificados no son evidencia de ejecución.

## Violaciones, errores técnicos e incomplete

| Métrica | Valor actual | Motivo |
| --- | --- | --- |
| Violaciones axe y distribución por impacto | Not Available | No se ha ejecutado axe |
| Nodos afectados y conteos por regla | Not Available | Sin salida estructurada de escaneos |
| Errores técnicos | Not Available | Sin ejecución de accesibilidad |
| incomplete | Not Available | Sin salida de escaneos para revisar |
| passes / inapplicable | Not Available | Sin salida; ninguno establece conformidad WCAG |
| Defectos confirmados | Not Available | Sin evaluación ejecutada que permita reportar defectos |

Resultados ausentes no equivalen a cero violaciones. Al ejecutar, contar por separado violaciones, reglas distintas, nodos e incomplete, conservando estado. Documentar deduplicación entre estados. No contar errores técnicos como violaciones WCAG.

### Interpretación tras ejecución futura

PASS automatizado requiere que todos los escaneos obligatorios finalicen en el estado correcto con cero violaciones. Cualquier violación detectada produce FAIL, incluso en ejecuciones con errores técnicos o escaneos faltantes. Conservar y documentar violaciones, errores técnicos y ejecución incompleta por caso/estado. Reportar fallos de navegación, preparación, inyección, timeout o axe como Technical Error; nunca reportar PASS si falta un escaneo obligatorio o queda sin finalizar. Conservar axe incomplete por separado para revisión humana sin clasificarlo automáticamente como PASS o FAIL. PASS solo cubre reglas y estados ejecutados y no establece conformidad WCAG.

Registrar revisión de incomplete como Pending, Reviewed o Resolved independientemente de la aserción automatizada. PASS con cero violaciones e incomplete pendiente todavía requiere revisión humana y nunca cambia Compliance Result a conformidad. Conservar violaciones y cualquier error técnico en casos parcialmente ejecutados.

## Registro de ejecución y evidencia

| Campo | Valor actual / requisito futuro |
| --- | --- |
| ID / fecha-hora de ejecución | Not Available |
| Commit o referencia de versión desplegada | Not Available |
| OS / Chrome / viewport / zoom | Not Available |
| axe-core / Java integration / enabled tags and rules | Not Selected / Not Implemented |
| NVDA / manual tools | Not Recorded — Not Executed |
| Allure report URL / run reference | Not Available |
| Ubicación de evidencia | Not Available |

En la próxima ejecución real, adjuntar datos axe estructurados por caso/estado: URL, fecha-hora, versiones/configuración, regla, impacto, etiquetas/URL de ayuda, nodos y resumen de fallo, además de passes, incomplete e inapplicable. Incluir etapa/excepción de errores técnicos. Captura y URL deben identificar estado; no se proporcionan enlaces ficticios a evidencia.

## Registro de defectos

No se han creado entradas de defectos porque no se ha ejecutado evaluación de accesibilidad. Agregar filas solo ante un problema real. Los registros futuros incluirán ID, ejecución, caso/estado, título, regla/SC, impacto y prioridad de triage, URL, elemento, reproducción, esperado/real, evidencia, disposición y retest. Una violación de herramienta es evidencia para triage; no debe equipararse automáticamente a fallo del criterio completo sin revisar contexto.

| ID de defecto | Caso / estado | SC / regla | Comportamiento real | Evidencia | Estado / retest |
| --- | --- | --- | --- | --- | --- |


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

## Cobertura y limitaciones

| ID del caso | Página | Estados obligatorios | N.º de escaneos |
| --- | --- | --- | --- |
| A11Y-AUTO-001 | Login | login-initial, login-invalid-credentials | 2 |
| A11Y-AUTO-002 | Productos | products-initial, products-product-added, products-menu-open | 3 |
| A11Y-AUTO-003 | Carrito con producto | cart-with-product, cart-empty | 2 |
| A11Y-AUTO-004 | Información de checkout | checkout-information-initial, checkout-error-first-name, checkout-error-last-name, checkout-error-postal-code | 4 |
| A11Y-AUTO-005 | Resumen de checkout | checkout-overview | 1 |
| A11Y-AUTO-006 | Checkout completado | checkout-complete | 1 |

La matriz conserva 55 criterios A/AA: 37 preliminarmente Applicable y 18 To Be Confirmed. No se cierra N/A. En 2.2.2 la evidencia de la fuente corresponde al Slider excluido; la aplicabilidad ampliada no crea cobertura realizada ni inicial de esa ruta. Referencias al detalle de producto de 2.4.5 quedan diferidas. Seis tests futuros cubren estados representativos del flujo principal, no todos los requisitos WCAG ni toda la aplicación.

Excluidos: catálogos adicionales dinámicos/largo, detalle, Slider/Spinner adicionales, generación y accesibilidad del PDF generado. Control PDF renderizado en Confirmación se incluye en ese escaneo. Teclado, foco, anuncios NVDA, reflow, espaciado, tiempo y adecuación semántica requieren evaluación humana planificada. Observaciones estáticas de lang, título, ARIA o alternativas no establecen conformidad.

## Procedimiento de actualización

1. Implementar/verificar integración y selecciones Maven independientes: Functional=15, Accessibility=6, All=21. Añadir comandos definitivos solo tras validarlos.
2. Registrar ejecución/entorno reales y resultados de los trece estados, con evidencia Allure.
3. Actualizar implementación, ejecución y resultado automatizado por separado de conformidad.
4. Revisar violaciones/errores reales, incomplete y vincular defectos/retests reales.
5. Ejecutar categorías manuales por separado; actualizar solo las realizadas y conservar preguntas de aplicabilidad no verificadas.
6. Sincronizar ediciones y filas por IDs estables. Reportar “sin violaciones detectadas por las reglas y estados ejecutados” solo con respaldo. No afirmar conformidad WCAG 2.2 AA de SauceDemo.

## Referencias

- REF-01: Contrato aprobado incorporado. Solo documentación para qa-saucedemo-portfolio: 15 tests funcionales existentes con Java 25, Selenium, TestNG, Maven, Page Object Model y Allure. Alcance inicial: Login → Products → Cart → Checkout Information → Checkout Overview → Checkout Complete, incluidos errores definidos, cambios del carrito y menú lateral abierto. Exactamente seis casos automatizados con trece escaneos obligatorios, diez categorías manuales, cuatro hojas por workbook y cincuenta y cinco criterios WCAG 2.2 A/AA; selecciones Maven futuras: Functional=15, Accessibility=6, All=21. Se excluyen catálogos adicionales dinámicos/largo, detalle, Slider/Spinner, generación del PDF y accesibilidad del PDF generado; se incluye el control PDF renderizado. Conservar clasificación provisional 37 Applicable / 18 To Be Confirmed, línea base Not Executed / Not Evaluated, dimensiones de estado separadas y equivalencia bilingüe. No implica implementación, evidencia de ejecución ni conformidad.
- REF-02: Línea base técnica histórica incorporada, no verificación actual. §1 Observaciones del proyecto: 15 tests funcionales; Selenium 4.49.0, TestNG 7.12.0, Allure TestNG 3.0.0 y Surefire 3.5.6; sin integración axe ni selecciones independientes de suites. El listener funcional registra captura/URL de fallo, no datos axe; DriverFactory restringe asistencia del administrador de contraseñas. §2 Observaciones estáticas: lang=en, título Swag Labs, imágenes de productos/confirmación y controles gráficos, cambios de badge/nombre del carrito, menú/submenú, validación obligatoria y errores role=alert con control para descartarlos. Se reportaron cookie de sesión de 600 segundos y rutas protegidas; Slider excluido actualiza cada dos segundos y Spinner usa role=status. Confirmación renderiza un control PDF de forma condicional. La WCAG Coverage Matrix reproduce observaciones por criterio y límites de alcance; no son resultados de estados renderizados. La interacción en navegador no estuvo disponible y no se registraron fecha ni referencia de versión inspeccionada. §3 Credenciales públicas de demo y datos sintéticos de checkout se reproducen en Test Data. No se verifican nuevamente estas observaciones históricas en esta revisión; REF-03 proporciona requisitos normativos públicos.
- REF-03: [Especificación W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/), consultada el 2026-10-08 para nombres, niveles y requisitos normativos.
- REF-04: [Reglas de axe-core](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md) y [API de axe-core](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md). La relación futura usará la versión seleccionada, no una rama de desarrollo sin fijar.
