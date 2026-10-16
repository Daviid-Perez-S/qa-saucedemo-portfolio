# SauceDemo QA Automation Portfolio

Pruebas funcionales y de accesibilidad automatizada para SauceDemo, con Java, Selenium, evidencia Allure y GitHub Actions.

[![SauceDemo CI](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/ci.yml)
[![Allure Pages](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/pages.yml/badge.svg?branch=master)](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/pages.yml)

**[Consultar el reporte público de Allure](https://daviid-perez-s.github.io/qa-saucedemo-portfolio/)**

[English (principal)](README.md) · **Español**

**Índice**

- [Descripción general](#descripción-general)
- [Tecnologías](#tecnologías)
- [Cobertura de pruebas](#cobertura-de-pruebas)
- [Arquitectura](#arquitectura)
- [Ejecución local](#ejecución-local)
- [Integración continua y reportes](#integración-continua-y-reportes)
- [Documentación de QA](#documentación-de-qa)
- [Estado y limitaciones](#estado-y-limitaciones)
- [Licencia](#licencia)

## Descripción general

Este portafolio demuestra análisis de pruebas, diseño de casos trazables, automatización de interfaz, comprobaciones de accesibilidad y reportes respaldados por evidencia sobre [SauceDemo](https://www.saucedemo.com/), una tienda pública de demostración.

El flujo de compra cubre inicio de sesión, productos, carrito, checkout, confirmación y cierre de sesión. El framework utiliza Page Object Model, esperas explícitas y pruebas independientes. GitHub Actions ejecuta ambas suites y publica un reporte Allure consolidado mediante GitHub Pages.

Se utilizan cuentas públicas de demostración y datos sintéticos de checkout.

## Tecnologías

| Tecnología | Responsabilidad |
|---|---|
| Java 25 | Implementación de pruebas |
| Maven / Surefire 3.5.6 | Dependencias, compilación y selección de pruebas |
| Selenium 4.49.0 / Chrome | Automatización del navegador; Selenium Manager resuelve ChromeDriver |
| TestNG 7.12.0 | Ciclo de vida de pruebas y aserciones |
| axe-core 4.13.0 | Escaneos automáticos de accesibilidad mediante la integración Java con Selenium |
| Allure Report 3.20.0 | Resultados, adjuntos y reportes HTML |
| GitHub Actions / Pages | Ejecución de CI y alojamiento del reporte público |

Consultar [pom.xml](pom.xml) para las dependencias y plugins fijados, incluidos Allure TestNG 3.0.0 y Allure Maven Plugin 3.1.0.

## Cobertura de pruebas

**Automatización funcional: 15 / 15 casos aprobados en el alcance.**

| Área | Cobertura | Pruebas |
|---|---|---:|
| Inicio de sesión | Acceso válido, contraseña incorrecta, usuario inexistente y bloqueado | 4 |
| Productos | Catálogo, precios en orden ascendente y adición al carrito | 3 |
| Carrito | Detalles del producto, eliminación y navegación al checkout | 3 |
| Checkout | Finalización válida y tres errores de campos obligatorios | 4 |
| End-to-end | Compra y cierre de sesión | 1 |
| **Total** | | **15** |

El [libro QA funcional](docs/test-artifacts/qa-test-documentation-spanish.xlsx) contiene los casos detallados y registros de ejecución. Las descripciones de las pruebas conservan los IDs aprobados para mantener la trazabilidad.

**Accesibilidad automatizada: seis pruebas que contienen trece escaneos axe de página completa.**

| Página / estados | Pruebas | Escaneos |
|---|---:|---:|
| Inicio de sesión: inicial y credenciales inválidas | 1 | 2 |
| Productos: inicial, producto agregado y menú abierto | 1 | 3 |
| Carrito: con producto y vacío | 1 | 2 |
| Información de checkout: inicial y tres errores de campos obligatorios | 1 | 4 |
| Resumen de checkout | 1 | 1 |
| Checkout completado | 1 | 1 |
| **Total** | **6** | **13** |

Hay **21 pruebas automatizadas en total**; los escaneos están contenidos en las seis pruebas de accesibilidad. Las cantidades describen la cobertura implementada, no una tasa permanente de aprobación.

Los escaneos utilizan la configuración de reglas basada en WCAG 2.2 A/AA. Para obtener PASS automatizado, todos los estados obligatorios deben completarse sin violaciones ni errores técnicos. Los hallazgos `incomplete` de axe se conservan por separado y requieren revisión humana. Consultar los [resultados y limitaciones de accesibilidad](docs/accessibility/accessibility-test-results-spanish.md).

## Arquitectura

| Componente | Responsabilidad |
|---|---|
| [Page Objects](src/test/java/com/david/qa/pages) | Localizadores, interacciones, esperas explícitas y consultas del estado de las páginas |
| [Pruebas TestNG](src/test/java/com/david/qa/tests) | Preparación de escenarios y aserciones |
| [DriverFactory](src/test/java/com/david/qa/driver/DriverFactory.java) | Creación de Chrome, preferencias del administrador de contraseñas y modo headless opcional |
| [BaseTest](src/test/java/com/david/qa/tests/BaseTest.java) | Navegador nuevo, navegación inicial y cierre por prueba |
| [AccessibilityAudit](src/test/java/com/david/qa/accessibility/AccessibilityAudit.java) | Configuración de reglas, integridad de estados/resultados y resultado agregado |
| [Listeners](src/test/java/com/david/qa/listeners) / Allure | Evidencia de fallos y adjuntos estructurados de accesibilidad |

Las pruebas se ejecutan secuencialmente, con un navegador nuevo por método. La lógica de reportes permanece en los listeners, registrados mediante ServiceLoader.

Las pruebas fallidas reciben una captura PNG y URL cuando están disponibles, antes del cierre; los fallos de configuración no incluyen evidencia del navegador. Los JSON de escaneos y manifiestos por caso se adjuntan en pruebas de accesibilidad aprobadas y fallidas. TestNG/Allure proporciona los detalles de las excepciones. Las pruebas exitosas no tienen capturas.

## Ejecución local

### Prerrequisitos

Instalar JDK 25, Maven y Chrome. Ejecutar los comandos desde la raíz del proyecto. SauceDemo, las descargas de dependencias y la configuración inicial de Selenium Manager/Allure requieren internet. No se necesita Node.js global.

### Ejecutar pruebas

Elegir un modo:

**Funcional — 15 pruebas**

```shell
mvn clean test
```

**Accesibilidad — 6 pruebas, 13 escaneos**

```shell
mvn clean test "-Dtest=AccessibilityTest"
```

**Combinado — 21 pruebas**

```shell
mvn clean test "-Dtest=*Test"
```

Cada `clean test` sustituye los resultados previos de `target/`. Las ejecuciones separadas no consolidan resultados. Conservar la evidencia antes de otra ejecución.

Chrome abre con interfaz gráfica por defecto. Agregar `"-Dheadless=true"` a cualquier comando de pruebas; por ejemplo:

```shell
mvn clean test "-Dheadless=true"
```

### Consultar Allure localmente

Después de las pruebas, generar el HTML:

```shell
mvn allure:report
```

O generar y visualizar el reporte mediante un servidor local:

```shell
mvn allure:serve
```

Detener el servidor con `Ctrl+C`. Visualizar el reporte mediante HTTP en lugar de abrir `index.html` directamente.

**Tras una ejecución fallida, generar el reporte sin ejecutar `clean` antes**, para conservar los resultados y adjuntos.

| Salida | Ubicación |
|---|---|
| Resultados Surefire | `target/surefire-reports/` |
| Resultados originales Allure | `target/allure-results/` |
| HTML generado | `target/allure-report/` |

Git ignora las salidas generadas y la caché del runtime `.allure/`. El historial del reporte está desactivado.

## Integración continua y reportes

### Ejecución de pruebas — SauceDemo CI

[ci.yml](.github/workflows/ci.yml) se ejecuta con pushes a `feature/github-actions-ci` y `master`, PRs dirigidos a `master` y activación manual. Dos jobs independientes utilizan Ubuntu 24.04, Temurin Java 25, caché Maven y Chrome headless. Los jobs pueden ejecutarse simultáneamente; las pruebas de cada job siguen siendo secuenciales.

CI valida 15 resultados funcionales y seis de accesibilidad, incluidos trece escaneos y seis manifiestos. La validación exige pruebas aprobadas y evidencia consistente. La generación de reportes y subida de artifacts se intentan después de fallos salvo cancelación, sin ocultar los pasos fallidos.

| Artifact | Suite |
|---|---|
| `functional-evidence` | Funcional |
| `accessibility-evidence` | Accesibilidad |

Descargar ambos artifacts desde el CI de origen dentro de **14 días**. Incluyen reportes Surefire, resultados originales Allure y HTML cuando su generación termina correctamente.

### Publicación del reporte — Allure Pages

[pages.yml](.github/workflows/pages.yml) se ejecuta después de ejecuciones de CI finalizadas y elegibles de `master`, originadas por push o activación manual. Los resultados de PRs no se publican.

Verifica los artifacts originales, valida y consolida 21 resultados, y genera y comprueba el HTML y los adjuntos antes del despliegue. Conserva los metadatos del CI original; un candidato anterior no puede sustituir una publicación posterior confirmada.

**La evidencia válida y completa puede publicarse aunque existan pruebas fallidas.** La validación de publicación admite resultados `failed`/`broken` documentados, pero rechaza pruebas omitidas, escaneos faltantes y evidencia inconsistente. Un despliegue exitoso confirma la publicación, no el éxito de las pruebas. Los badges muestran el estado de los workflows; los resultados de las pruebas se consultan en el reporte.

## Documentación de QA

| Tema | Documentos |
|---|---|
| Pruebas funcionales | [Plan inicial de pruebas](docs/test-plan/test-plan-spanish.md) · [Libro QA](docs/test-artifacts/qa-test-documentation-spanish.xlsx) |
| Accesibilidad | [Plan de pruebas](docs/accessibility/accessibility-test-plan-spanish.md) · [Casos y matriz WCAG](docs/accessibility/accessibility-test-cases-spanish.xlsx) |
| Línea base local de accesibilidad, 2026-10-09 | [Resultados y limitaciones](docs/accessibility/accessibility-test-results-spanish.md) · [Resumen de ejecución](docs/accessibility/accessibility-execution-summary.json) |
| Evidencia y publicación | [Validador](scripts/validate-ci-evidence.py) · [Consolidación](scripts/consolidate-allure-results.py) · [Comprobaciones de publicación](scripts/pages-publication.py) |

El plan funcional registra el alcance inicial; los documentos fechados describen ejecuciones históricas. Los resultados posteriores se consultan en el reporte público y los workflows.

## Estado y limitaciones

**Los objetivos definidos de automatización funcional, accesibilidad automatizada, reporting y CI/CD están implementados y verificados.**

- La evaluación manual de accesibilidad está **pospuesta sin fecha prevista**, fuera del alcance completado. Sus diez categorías documentadas permanecen Planned / Not Executed.
- Los resultados automatizados no establecen conformidad WCAG 2.2 AA ni constituyen una evaluación integral de accesibilidad. Los hallazgos `incomplete` requieren revisión humana.
- La cobertura se centra en flujos seleccionados en Chrome; la disponibilidad del servicio externo y los cambios de la aplicación pueden afectar la ejecución.
- Quedan fuera del alcance rendimiento, seguridad, dispositivos móviles, cobertura exhaustiva en varios navegadores, backend y pagos reales. Las pruebas API pertenecen a un proyecto separado.

## Licencia

Este proyecto está bajo la licencia MIT.
Consulta el archivo [LICENSE](LICENSE) para más información.

**Responsable:** [David Pérez](https://www.linkedin.com/in/david-perez-s/).
