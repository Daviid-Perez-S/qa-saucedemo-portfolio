# SauceDemo QA Automation Portfolio

Proyecto inicial de portafolio QA para planear y automatizar los flujos principales de la tienda pública de demostración SauceDemo.

Esta versión en español es complementaria; GitHub mostrará `README.md` en inglés como portada principal. [Ver README principal](README.md).

**Responsable:** David Pérez · **Estado:** los 15 tests funcionales iniciales y seis tests de accesibilidad (trece scans) están automatizados y verificados; CI con GitHub Actions, reportes Allure y artifacts de evidencia separados verificados en `feature/github-actions-ci`; integración a `master` pendiente.

## Objetivos del proyecto

- Documentar 15 casos funcionales con escenarios, pasos, resultados esperados y datos de prueba claros.
- Construir un proyecto mantenible de automatización de interfaz con Java, Maven, Selenium WebDriver, TestNG y Page Object Model.
- Automatizar los 15 casos acordados y registrar resultados y defectos cuando se encuentren.
- Generar reportes Allure con evidencia automática del navegador para tests fallidos.
- Mantener las pruebas de accesibilidad automatizadas y la integración continua con GitHub Actions y evidencia verificable.

API Testing se planea como proyecto de portafolio separado. El alcance inicial excluye rendimiento, seguridad, dispositivos móviles, pruebas exhaustivas en varios navegadores, backend y pagos reales.

## Documentación

- [Plan de pruebas — Español](docs/test-plan/test-plan-spanish.md) · [Libro QA — Español](docs/test-artifacts/qa-test-documentation-spanish.xlsx)
- [Test Plan — English](docs/test-plan/test-plan-english.md) · [QA workbook — English](docs/test-artifacts/qa-test-documentation-english.xlsx)
- [Instrucciones para agentes de programación](AGENTS.md)
- [README in English](README.md)

## Tecnologías actuales

Java · Maven · Selenium WebDriver · TestNG · Page Object Model · Google Chrome · Allure Report · GitHub Actions

El entorno local documentado es una laptop personal con Windows 11 25H2 y Google Chrome 154.0.8037.99. CI utiliza runners Ubuntu 24.04 proporcionados por GitHub, Temurin Java 25, Maven y Chrome headless. Las versiones de Maven y Chrome provienen de la imagen del runner y se registran en cada ejecución; la versión local de Chrome es una referencia temporal y puede cambiar.

## Cobertura de Automatización

**Progreso de automatización: 15 / 15 casos de prueba**

| ID de caso de prueba | Escenario | Estado |
|---|---|---|
| TC-LOGIN-001 | Iniciar sesión con credenciales válidas | Automatizado |
| TC-LOGIN-002 | Iniciar sesión con contraseña incorrecta | Automatizado |
| TC-LOGIN-003 | Iniciar sesión con un usuario inexistente | Automatizado |
| TC-LOGIN-004 | Iniciar sesión con un usuario bloqueado | Automatizado |
| TC-PROD-001 | Visualizar el catálogo de productos | Automatizado |
| TC-PROD-002 | Ordenar productos por precio de menor a mayor | Automatizado |
| TC-PROD-003 | Agregar un producto al carrito | Automatizado |
| TC-CART-001 | Verificar un producto agregado en el carrito | Automatizado |
| TC-CART-002 | Eliminar un producto del carrito | Automatizado |
| TC-CART-003 | Continuar del carrito al checkout | Automatizado |
| TC-CHECK-001 | Completar checkout con información válida | Automatizado |
| TC-CHECK-002 | Validar nombre vacío | Automatizado |
| TC-CHECK-003 | Validar apellido vacío | Automatizado |
| TC-CHECK-004 | Validar código postal vacío | Automatizado |
| TC-E2E-001 | Completar una compra y cerrar sesión | Automatizado |

El estado refleja la implementación en el código, no un resultado de ejecución. Consulta el [libro QA en español](docs/test-artifacts/qa-test-documentation-spanish.xlsx) para los pasos completos, datos de prueba, resultados esperados y registros de ejecución, y el [Plan de Pruebas](docs/test-plan/test-plan-spanish.md) para el alcance y enfoque.

## Arquitectura de Automatización

El proyecto utiliza Page Object Model con una separación sencilla de responsabilidades:

- `LoginPage`, `ProductsPage`, `CartPage`, `CheckoutInformationPage`, `CheckoutOverviewPage` y `CheckoutCompletePage` contienen localizadores, interacciones, esperas explícitas y consultas del estado de las páginas.
- `LoginTest`, `ProductsTest`, `CartTest`, `CheckoutTest` y `EndToEndTest` contienen los escenarios y las assertions, con cada prueba vinculada a su ID de caso aprobado.
- Las cinco clases de tests extienden `BaseTest`, que centraliza únicamente el lifecycle común de WebDriver. Su `@BeforeMethod` abre un navegador Chrome nuevo y navega a SauceDemo antes de la preparación específica de cada prueba. Su `@AfterMethod(alwaysRun = true)` llama a `quit()` cuando existe un driver, incluso después de fallos en las pruebas, y limpia la referencia al driver en `finally`.
- `ProductsTest` inicia sesión y espera a Products durante la preparación; sus tres casos se ejecutan de forma independiente, cada uno con un navegador nuevo.
- `CartTest` prepara un carrito con un producto para cada caso independiente.
- `DriverFactory.createChromeDriver()` centraliza la creación de Chrome y desactiva el guardado de contraseñas y los avisos de contraseñas comprometidas en cada navegador de prueba. Cada llamada crea un WebDriver nuevo; `BaseTest` administra el lifecycle común, mientras que la preparación específica y las assertions permanecen en las clases concretas de tests.
- El test de ordenamiento espera explícitamente a que los precios mostrados alcancen el orden ascendente antes de comprobar el resultado. `CartPage.removeBackpack()` espera únicamente la eliminación de la mochila; el test de carrito espera explícitamente el estado vacío y la desaparición del badge antes de sus assertions. Estas expectativas del escenario permanecen en la capa de tests.
- `CheckoutTest` prepara la información de checkout con un producto para cada caso independiente, cubriendo checkout válido y validación de campos obligatorios. Su método privado de assertions comprueba el error específico del campo y que checkout sigue bloqueado; las assertions permanecen en la capa de tests.
- `CheckoutInformationPage` permite ingresar campos, ejecutar `clickContinue()` y consultar errores, además de verificar el destino utilizado por Cart. `clickContinue()` describe la acción tanto para envíos válidos como para envíos bloqueados por validación. `CheckoutOverviewPage` permite revisar el resumen y finalizar el pedido; `CheckoutCompletePage` expone el estado de confirmación. `CheckoutCompletePage` también abre el menú y cierra sesión; `LoginPage` espera al formulario de login después del logout.
- `EndToEndTest` ejecuta el flujo completo de compra y logout en una sesión de navegador independiente, reutilizando los Page Objects existentes.
- Selenium Manager resuelve ChromeDriver automáticamente.
- `FailureEvidenceListener` utiliza `IInvokedMethodListener.afterInvocation()` y se registra centralmente mediante ServiceLoader. Para métodos `@Test` fallidos, obtiene el navegador de la instancia actual mediante `BaseTest.getDriver()` e intenta independientemente un screenshot PNG y la URL actual antes del cierre. Los errores de evidencia conservan el fallo original. La ejecución sigue siendo secuencial, con un navegador nuevo por test.

Estructura actual de automatización:

```text
src/test/java/com/david/qa/
├── accessibility/
│   └── AccessibilityAudit.java
├── driver/
│   └── DriverFactory.java
├── listeners/
│   ├── FailureEvidenceListener.java
│   └── AccessibilityEvidenceListener.java
├── pages/
│   ├── LoginPage.java
│   ├── ProductsPage.java
│   ├── CartPage.java
│   ├── CheckoutInformationPage.java
│   ├── CheckoutOverviewPage.java
│   └── CheckoutCompletePage.java
└── tests/
    ├── BaseTest.java
    ├── LoginTest.java
    ├── ProductsTest.java
    ├── CartTest.java
    ├── CheckoutTest.java
    ├── EndToEndTest.java
    └── accessibility/
        └── AccessibilityTest.java
```

Los recursos de test contienen `allure.properties` y `META-INF/services/org.testng.ITestNGListener`.

El proyecto utiliza Java 25, Selenium 4.49.0, TestNG 7.12.0, Maven Compiler Plugin 3.16.0, Maven Surefire Plugin 3.5.6, Allure TestNG 3.0.0, Allure Maven Plugin 3.1.0 y Allure Report 3.20.0.

Surefire 3.5.6 es una decisión de compatibilidad para la integración actual de TestNG + Allure. Surefire 3.6.0 utiliza el motor TestNG de JUnit Platform, cuyo descubrimiento en modo dry-run generó 45 resultados Allure para 15 tests reales. El proveedor nativo de TestNG en 3.5.6 fue verificado con exactamente 15 resultados únicos, sin adaptadores ni filtros de resultados.

## Ejecutar las pruebas automatizadas

Requisitos: JDK 25, Maven, Google Chrome y acceso a internet a SauceDemo. Maven descarga las dependencias; Selenium Manager puede necesitar internet en la primera ejecución.

Desde la raíz del proyecto, ejecutar:

```shell
mvn clean test
```

Los resultados estándar de ejecución están disponibles en `target/surefire-reports/`.

Chrome abre con interfaz gráfica por defecto. Agregar `"-Dheadless=true"` a cualquier comando de tests permite ejecutar sin una ventana visible del navegador, como en CI:

```shell
mvn clean test "-Dheadless=true"
```

## Reporting Allure y evidencia de fallos

Los resultados originales de Allure se escriben en `target/allure-results/`. Generar el reporte HTML después de ejecutar los tests:

```shell
mvn allure:report
```

El reporte se genera en `target/allure-report/`. Para generarlo y visualizarlo mediante un servidor local:

```shell
mvn allure:serve
```

Detener el servidor con `Ctrl+C`. El plugin descarga su runtime privado de Node.js y el paquete de Allure Report en `.allure/` durante el primer uso; esa descarga requiere internet, pero no necesita una instalación global de Node.js. Git ignora la caché del runtime y los resultados/reportes generados. El historial del reporte está inicialmente desactivado con `historyEnabled=false`.

Visualizar los reportes mediante un servidor HTTP local en lugar de abrir `index.html` directamente. Para un reporte descargado de CI, extraer el artifact y servir su carpeta `allure-report/`. En Windows, el runtime privado existente permite servirlo sin Python ni una instalación global de Node.js (las rutas siguientes corresponden a la caché local actual; ajustarlas si cambia):

```powershell
& ".allure/node-v24.14.1-win-x64/node.exe" ".allure/allure-3.20.0/node_modules/allure/cli.js" open "C:/ruta/al/artifact-extraido/allure-report"
```

Ejecutar desde la raíz del proyecto después de que el plugin Maven haya inicializado `.allure/`; detener el servidor con `Ctrl+C`.

Si una ejecución falla, ejecutar el comando de reporte por separado sin ejecutar `clean` entre ambos, para conservar sus resultados y evidencia. Utilizar `mvn clean test` para una ejecución nueva y evitar mezclar resultados de distintas ejecuciones.

Los métodos `@Test` funcionales fallidos reciben un screenshot PNG del navegador y la URL actual como adjunto de texto, cuando el navegador está disponible. TestNG/Allure proporciona la excepción, el mensaje y el stack trace originales. Los tests exitosos no reciben evidencia del navegador; los fallos de configuración se reportan sin evidencia del navegador. Los tests y Page Objects no contienen lógica de reporting. No se incorporan retries, logging adicional, page source, console/network logs ni video.

La validación del 2 de octubre de 2026 confirmó 15 tests, 0 failures, 0 errors y 0 skipped, con exactamente 15 resultados Allure únicos y sin adjuntos de tests exitosos. Un fallo controlado temporal en TC-LOGIN-001 produjo un resultado fallido con exactamente dos adjuntos (PNG y URL de inventory) y los detalles originales del `AssertionError`. La assertion temporal fue retirada; la suite completa volvió a pasar y el reporte final contiene exactamente 15 tests aprobados.


## Accesibilidad automatizada

Se implementaron y verificaron los seis casos aprobados y trece scans con axe-core 4.13.0. Los tests funcionales existentes mantienen sus quince métodos.

```shell
mvn clean test
mvn clean test "-Dtest=AccessibilityTest"
mvn clean test "-Dtest=*Test"
```

Los modos Functional / Accessibility / All produjeron respectivamente 15 / 6 / 21 resultados TestNG y Allure el 2026-10-09. Las ejecuciones finales completaron los trece estados con cero violaciones y errores técnicos. Hay cuatro estados con color-contrast incomplete pendientes de revisión humana; no se declara conformidad WCAG.

AccessibilityAudit mantiene configuración, validación de estados/resultados y aserción final. AccessibilityEvidenceListener adjunta JSON por scan y manifiesto por caso, también en PASS; el listener de fallo mantiene captura/URL sin duplicación. No se cambió BaseTest ni los quince tests funcionales. Las variantes consecutivas de checkout usan borrado por teclado para actualizar el estado del formulario. Surefire permanece en 3.5.6, sin perfiles ni ejecución paralela de tests. La evaluación manual de accesibilidad queda pospuesta indefinidamente; las diez categorías manuales siguen Planned / Not Executed. El éxito automatizado no certifica conformidad WCAG y los resultados `incomplete` siguen pendientes de revisión humana.

[Resultados y limitaciones](docs/accessibility/accessibility-test-results-spanish.md) · [Resumen verificable](docs/accessibility/accessibility-execution-summary.json).

## Integración continua

[`SauceDemo CI`](.github/workflows/ci.yml) prepara el entorno, ejecuta tests headless, valida la evidencia, genera reportes HTML Allure y sube artifacts. Las ejecuciones en `feature/github-actions-ci` se verificaron con 15 tests funcionales y seis de accesibilidad aprobados, cero fallos, errores u omitidos y trece scans completados. No hay despliegue ni publicación en GitHub Pages.

Los triggers son push a `feature/github-actions-ci` o `master`, Pull Requests dirigidos a `master` y activación manual (`workflow_dispatch`). La activación manual mediante **Actions → SauceDemo CI → Run workflow** requiere que el workflow exista en la rama predeterminada del repositorio (`master`); queda pendiente de comprobar tras la integración. Consultar las [instrucciones de ejecución manual de GitHub](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).

Cada job tiene su propio runner Ubuntu 24.04, Temurin Java 25, caché de dependencias Maven cuya clave utiliza `pom.xml` y Chrome. El workflow concede únicamente `contents: read`.

| ID del job / nombre mostrado | Comando de tests | Tests esperados | Artifact |
|---|---|---|---|
| `environment-check` / Check Java, Maven and Chrome | `mvn --batch-mode --no-transfer-progress clean test -Dheadless=true` | 15 funcionales | `functional-evidence` |
| `accessibility` / Accessibility tests | `mvn --batch-mode --no-transfer-progress clean test "-Dtest=AccessibilityTest" -Dheadless=true` | 6 de accesibilidad, 13 scans | `accessibility-evidence` |

Los jobs no tienen dependencia `needs` y pueden ejecutarse simultáneamente. Los tests siguen siendo secuenciales dentro de cada job, con un navegador nuevo por test. Son dos ejecuciones separadas de suites, con 21 tests en total; CI no ejecuta el modo Maven combinado.

El [validador de evidencia compartido](scripts/validate-ci-evidence.py) utiliza únicamente la biblioteca estándar de Python, disponible en el runner. Los jobs lo invocan con `functional` o `accessibility`. Comprueba cantidades y resultados exitosos en los XML de Surefire; compara las identidades de tests con resultados Allure únicos y aprobados; verifica referencias de containers y adjuntos existentes y no vacíos, incluidos los anidados; y rechaza referencias duplicadas de adjuntos. En accesibilidad exige además trece scans únicos de los estados aprobados y seis manifiestos de una misma ejecución, metadatos de estados consistentes, preparación/scans completados, ausencia de errores técnicos o violaciones confirmadas y las cuatro categorías axe (`passes`, `violations`, `incomplete`, `inapplicable`). Informa las ocurrencias `incomplete` sin considerarlas conformidad demostrada. La evidencia faltante o inconsistente devuelve código de salida 1 y hace fallar el job.

La validación, generación del reporte y subida de artifacts utilizan `if: ${{ !cancelled() }}` para intentarse después de fallos de tests o integridad, sin ocultarlos. Una ejecución cancelada no garantiza la conservación de evidencia. La generación Allure no ejecuta `clean`, conservando los resultados de tests.

Para revisar una ejecución:

1. Abrir [Actions → SauceDemo CI](https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio/actions/workflows/ci.yml) y seleccionar el commit y evento correspondientes.
2. Abrir el step de tests de cada job. Esperar `Tests run: 15` o `Tests run: 6`, con `Failures: 0, Errors: 0, Skipped: 0`, y comprobar el mensaje `Evidence integrity PASS` del validador. Abrir los steps fallidos para consultar los errores; Success por sí solo no sustituye la comprobación de cantidades.
3. En **Artifacts**, dentro del resumen de la ejecución, descargar `functional-evidence` y `accessibility-evidence`. La retención es de 14 días. Ambos contienen `surefire-reports/`, `allure-results/` y `allure-report/`; los archivos del reporte dependen de que su generación termine correctamente.
4. Revisar los `TEST-*.xml` de Surefire y visualizar el reporte HTML siguiendo las instrucciones de servidor local anteriores. Los resultados Allure funcionales contienen 15 archivos `*-result.json`; accesibilidad contiene seis resultados y 19 adjuntos JSON (13 scans y seis manifiestos). Los containers representan agrupaciones del ciclo de vida de TestNG, no tests adicionales; su cantidad no es un criterio de aceptación.

Los checks del PR sobre el último commit y la ejecución en `master` quedan pendientes de verificar durante la integración. La revisión manual de accesibilidad y la certificación de conformidad WCAG quedan fuera de los criterios actuales de aceptación automatizada.

## Aplicación bajo prueba

[Abrir SauceDemo](https://www.saucedemo.com/)

Las credenciales públicas de demostración de SauceDemo están documentadas en la hoja Datos de prueba del libro QA y se identifican como datos de prueba intencionalmente públicos.

## Responsable

[David Pérez en LinkedIn](https://www.linkedin.com/in/david-perez-s/)
