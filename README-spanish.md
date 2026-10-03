# SauceDemo QA Automation Portfolio

Proyecto inicial de portafolio QA para planear y automatizar los flujos principales de la tienda pública de demostración SauceDemo.

Esta versión en español es complementaria; GitHub mostrará `README.md` en inglés como portada principal. [Ver README principal](README.md).

**Responsable:** David Pérez · **Estado:** documentación QA preparada; automatización de Login, Products y Cart implementada.

## Objetivos del proyecto

- Documentar 15 casos funcionales con escenarios, pasos, resultados esperados y datos de prueba claros.
- Construir un proyecto mantenible de automatización de interfaz con Java, Maven, Selenium WebDriver, TestNG y Page Object Model.
- Automatizar los 15 casos acordados y registrar resultados y defectos cuando se encuentren.
- Incorporar pruebas de accesibilidad, reportes y CI/CD con GitHub Actions en fases posteriores.

API Testing se planea como proyecto de portafolio separado. El alcance inicial excluye rendimiento, seguridad, dispositivos móviles, pruebas exhaustivas en varios navegadores, backend y pagos reales.

## Documentación

- [Plan de pruebas — Español](docs/test-plan/test-plan-spanish.md) · [Libro QA — Español](docs/test-artifacts/qa-test-documentation-spanish.xlsx)
- [Test Plan — English](docs/test-plan/test-plan-english.md) · [QA workbook — English](docs/test-artifacts/qa-test-documentation-english.xlsx)
- [Instrucciones para agentes de programación](AGENTS.md)
- [README in English](README.md)

## Tecnologías previstas

Java · Maven · Selenium WebDriver · TestNG · Page Object Model · Google Chrome

El entorno documentado actualmente es una laptop personal con Windows 11 25H2 y Google Chrome 154.0.8037.93. La versión de Chrome es una referencia temporal y puede cambiar.

## Cobertura de Automatización

**Progreso de automatización: 10 / 15 casos de prueba**

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
| TC-CHECK-001 | Completar checkout con información válida | Planeado |
| TC-CHECK-002 | Validar nombre vacío | Planeado |
| TC-CHECK-003 | Validar apellido vacío | Planeado |
| TC-CHECK-004 | Validar código postal vacío | Planeado |
| TC-E2E-001 | Completar una compra y cerrar sesión | Planeado |

El estado refleja la implementación en el código, no un resultado de ejecución. Consulta el [libro QA en español](docs/test-artifacts/qa-test-documentation-spanish.xlsx) para los pasos completos, datos de prueba, resultados esperados y registros de ejecución, y el [Plan de Pruebas](docs/test-plan/test-plan-spanish.md) para el alcance y enfoque.

## Arquitectura de Automatización

El proyecto utiliza Page Object Model con una separación sencilla de responsabilidades:

- `LoginPage`, `ProductsPage`, `CartPage` y `CheckoutInformationPage` contienen localizadores, interacciones, esperas explícitas y consultas del estado de las páginas.
- `LoginTest`, `ProductsTest` y `CartTest` contienen los escenarios y las assertions, con cada prueba vinculada a su ID de caso aprobado.
- `@BeforeMethod` abre un navegador Chrome nuevo y navega a SauceDemo para cada prueba. `@AfterMethod(alwaysRun = true)` llama a `quit()` cuando existe un driver, incluso después de fallos en las pruebas.
- `ProductsTest` inicia sesión y espera a Products durante la preparación; sus tres casos se ejecutan de forma independiente, cada uno con un navegador nuevo.
- `CartTest` prepara un carrito con un producto para cada caso independiente y desactiva los avisos del gestor de contraseñas en su sesión de Chrome.
- `CheckoutInformationPage` solo verifica el destino de la navegación desde Cart hacia checkout; los casos de Checkout siguen planeados.
- Selenium Manager resuelve ChromeDriver automáticamente.

Estructura actual de automatización:

```text
src/test/java/com/david/qa/
├── pages/
│   ├── LoginPage.java
│   ├── ProductsPage.java
│   ├── CartPage.java
│   └── CheckoutInformationPage.java
└── tests/
    ├── LoginTest.java
    ├── ProductsTest.java
    └── CartTest.java
```

El proyecto utiliza Java 25, Selenium 4.49.0, TestNG 7.12.0, Maven Compiler Plugin 3.16.0 y Maven Surefire Plugin 3.6.0.

## Ejecutar las pruebas automatizadas

Requisitos: JDK 25, Maven, Google Chrome y acceso a internet a SauceDemo. Maven descarga las dependencias; Selenium Manager puede necesitar internet en la primera ejecución.

Desde la raíz del proyecto, ejecutar:

```shell
mvn test
```

Los resultados estándar de ejecución están disponibles en `target/surefire-reports/`.

## Aplicación bajo prueba

[Abrir SauceDemo](https://www.saucedemo.com/)

Las credenciales públicas de demostración de SauceDemo están documentadas en la hoja Datos de prueba del libro QA y se identifican como datos de prueba intencionalmente públicos.

## Responsable

[David Pérez en LinkedIn](https://www.linkedin.com/in/david-perez-s/)
