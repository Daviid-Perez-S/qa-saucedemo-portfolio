# SauceDemo QA Automation Portfolio

Proyecto inicial de portafolio QA para planear y automatizar los flujos principales de la tienda pública de demostración SauceDemo.

Esta versión en español es complementaria; GitHub mostrará `README.md` en inglés como portada principal. [Ver README principal](README.md).

**Responsable:** David Pérez · **Estado:** documentación QA preparada; automatización inicial de login implementada.

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

## Ejecutar la prueba automatizada inicial

Requisitos: JDK 25, Maven, Google Chrome y acceso a internet a SauceDemo. Maven descarga las dependencias; Selenium Manager resuelve ChromeDriver y puede necesitar internet en la primera ejecución.

Desde la raíz del proyecto, ejecutar:

```shell
mvn test
```

La prueba positiva TestNG implementa `TC-LOGIN-001` con los datos públicos `TD-LOGIN-01`: abrir Chrome, iniciar sesión, verificar el título Products, la ruta de inventario y el catálogo visible, y cerrar el navegador incluso si la prueba falla. `TC-LOGIN-002` utiliza `TD-LOGIN-02` (`standard_user` / `invalid_password`) para verificar el error de credenciales y que se rechaza el acceso mientras la página y el formulario de login siguen visibles. Cada prueba abre y cierra su propio navegador. Las assertions están en `LoginTest`; `LoginPage` y `ProductsPage` contienen localizadores, interacciones, esperas y consultas del estado.

El proyecto utiliza Java 25, Selenium 4.49.0, TestNG 7.12.0, Maven Compiler Plugin 3.16.0 y Maven Surefire Plugin 3.6.0. Los otros 13 casos están pendientes. Los resultados estándar de ejecución están disponibles en `target/surefire-reports/`.

## Aplicación bajo prueba

[Abrir SauceDemo](https://www.saucedemo.com/)

Las credenciales públicas de demostración de SauceDemo están documentadas en la hoja Datos de prueba del libro QA y se identifican como datos de prueba intencionalmente públicos.

## Responsable

[David Pérez en LinkedIn](https://www.linkedin.com/in/david-perez-s/)
