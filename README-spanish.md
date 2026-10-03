# SauceDemo QA Automation Portfolio

Proyecto inicial de portafolio QA para planear y automatizar los flujos principales de la tienda pública de demostración SauceDemo.

Esta versión en español es complementaria; GitHub mostrará `README.md` en inglés como portada principal. [Ver README principal](README.md).

**Responsable:** David Pérez · **Estado:** documentación QA preparada; los 15 casos funcionales iniciales están automatizados y verificados; reporting Allure y evidencia automática de fallos verificados.

## Objetivos del proyecto

- Documentar 15 casos funcionales con escenarios, pasos, resultados esperados y datos de prueba claros.
- Construir un proyecto mantenible de automatización de interfaz con Java, Maven, Selenium WebDriver, TestNG y Page Object Model.
- Automatizar los 15 casos acordados y registrar resultados y defectos cuando se encuentren.
- Generar reportes Allure con evidencia automática del navegador para tests fallidos.
- Incorporar pruebas de accesibilidad y CI/CD con GitHub Actions en fases posteriores.

API Testing se planea como proyecto de portafolio separado. El alcance inicial excluye rendimiento, seguridad, dispositivos móviles, pruebas exhaustivas en varios navegadores, backend y pagos reales.

## Documentación

- [Plan de pruebas — Español](docs/test-plan/test-plan-spanish.md) · [Libro QA — Español](docs/test-artifacts/qa-test-documentation-spanish.xlsx)
- [Test Plan — English](docs/test-plan/test-plan-english.md) · [QA workbook — English](docs/test-artifacts/qa-test-documentation-english.xlsx)
- [Instrucciones para agentes de programación](AGENTS.md)
- [README in English](README.md)

## Tecnologías actuales

Java · Maven · Selenium WebDriver · TestNG · Page Object Model · Google Chrome · Allure Report

El entorno documentado actualmente es una laptop personal con Windows 11 25H2 y Google Chrome 154.0.8037.93. La versión de Chrome es una referencia temporal y puede cambiar.

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
├── driver/
│   └── DriverFactory.java
├── listeners/
│   └── FailureEvidenceListener.java
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
    └── EndToEndTest.java
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

Si una ejecución falla, ejecutar el comando de reporte por separado sin ejecutar `clean` entre ambos, para conservar sus resultados y evidencia. Utilizar `mvn clean test` para una ejecución nueva y evitar mezclar resultados de distintas ejecuciones.

Los métodos `@Test` fallidos reciben únicamente un screenshot PNG del navegador y la URL actual como adjunto de texto, cuando el navegador está disponible. TestNG/Allure proporciona la excepción, el mensaje y el stack trace originales. Los tests exitosos no reciben evidencia del navegador; los fallos de configuración se reportan sin evidencia del navegador. Los tests y Page Objects no contienen lógica de reporting. No se incorporan retries, logging adicional, page source, console/network logs ni video.

La validación del 2 de octubre de 2026 confirmó 15 tests, 0 failures, 0 errors y 0 skipped, con exactamente 15 resultados Allure únicos y sin adjuntos de tests exitosos. Un fallo controlado temporal en TC-LOGIN-001 produjo un resultado fallido con exactamente dos adjuntos (PNG y URL de inventory) y los detalles originales del `AssertionError`. La assertion temporal fue retirada; la suite completa volvió a pasar y el reporte final contiene exactamente 15 tests aprobados.

## Aplicación bajo prueba

[Abrir SauceDemo](https://www.saucedemo.com/)

Las credenciales públicas de demostración de SauceDemo están documentadas en la hoja Datos de prueba del libro QA y se identifican como datos de prueba intencionalmente públicos.

## Responsable

[David Pérez en LinkedIn](https://www.linkedin.com/in/david-perez-s/)
