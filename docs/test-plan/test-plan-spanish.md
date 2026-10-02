# SauceDemo QA Automation Portfolio — Plan de Pruebas

| Campo del documento | Valor |
|---|---|
| Versión | 1.0 |
| Fecha | Octubre de 2026 |
| Autor | David Pérez |
| Aplicación bajo prueba | SauceDemo — https://www.saucedemo.com/ |
| Repositorio | https://github.com/Daviid-Perez-S/qa-saucedemo-portfolio |
| Idioma | Español |

## 1. Objetivo

Definir un enfoque enfocado y trazable para evaluar los principales flujos de compra de SauceDemo mediante pruebas funcionales manuales y automatización de interfaz. Este proyecto de portafolio demuestra análisis de QA, diseño de pruebas, automatización y comunicación clara de resultados, sin añadir procesos ni complejidad innecesarios.

## 2. Aplicación bajo prueba

SauceDemo es una aplicación web pública que simula una tienda en línea. Este plan cubre autenticación, consulta y ordenamiento de productos, operaciones del carrito, checkout, confirmación del pedido y cierre de sesión al terminar el flujo end-to-end.

## 3. Alcance

La suite inicial contiene 15 casos de prueba funcionales. Se planea automatizar los 15 en el proyecto.

| Módulo | Cobertura | IDs de casos de prueba | Cantidad |
|---|---|---|---:|
| Inicio de sesión | Inicio válido, contraseña incorrecta, usuario inexistente y usuario bloqueado | TC-LOGIN-001–004 | 4 |
| Productos | Ver catálogo, ordenar por precio y agregar producto | TC-PROD-001–003 | 3 |
| Carrito | Verificar producto, eliminar producto y continuar a checkout | TC-CART-001–003 | 3 |
| Checkout | Completar checkout; validar nombre, apellido y código postal vacíos | TC-CHECK-001–004 | 4 |
| End-to-End | Completar compra y cerrar sesión | TC-E2E-001 | 1 |
| **Total** |  |  | **15** |

Los escenarios detallados, pasos, resultados esperados, campos de ejecución y datos de prueba están en [el libro de QA en español](qa-test-documentation-spanish.xlsx). También está disponible [la versión en inglés](qa-test-documentation-english.xlsx).

## 4. Fuera del alcance

- Pruebas de rendimiento, carga y estrés.
- Pruebas de seguridad y penetración.
- Pruebas en dispositivos móviles y cobertura exhaustiva en varios navegadores.
- Pruebas de backend, API, infraestructura y proveedores de pago reales. API Testing se planea como proyecto de portafolio separado.
- Pruebas de accesibilidad en el ciclo inicial; se planean para una fase posterior del proyecto.

## 5. Enfoque de pruebas

- Aplicar pruebas funcionales, positivas, negativas, de regresión y end-to-end a los casos incluidos en el alcance.
- Realizar comprobaciones manuales exploratorias para conocer la aplicación e investigar comportamientos inesperados; registrar defectos cuando se identifiquen.
- Automatizar los 15 casos definidos con Java, Maven, Selenium WebDriver, TestNG y Page Object Model. Mantener el diseño sencillo para que sea fácil de explicar y mantener.
- Registrar estado de ejecución, resultado real y referencia del defecto en el libro QA cuando corresponda. No asumir ni inventar defectos antes de la ejecución.
- Incorporar reportes de pruebas y CI/CD con GitHub Actions en fases posteriores.

## 6. Entorno de pruebas

- Dispositivo: laptop personal de David Pérez.
- Sistema operativo: Windows 11 25H2.
- Navegador: Google Chrome 154.0.8037.93, versión disponible al preparar este plan (octubre de 2026). La versión instalada puede cambiar.
- Aplicación: sitio público de demostración SauceDemo.
- Stack de automatización previsto: Java, Maven, Selenium WebDriver y TestNG.

## 7. Datos de prueba

Se usarán las cuentas públicas de demostración de SauceDemo y datos de checkout de muestra no sensibles. El usuario y la contraseña públicos de demostración están en la hoja Datos de prueba de cada libro QA, junto con la referencia y una nota que explica que son credenciales públicas intencionales, no un defecto de seguridad. Los casos negativos usan valores sintéticos identificados como inválidos.

## 8. Escenarios y trazabilidad

El libro QA relaciona cada escenario de alto nivel con sus casos y datos de prueba. La suite está agrupada en Inicio de sesión, Productos, Carrito, Checkout y End-to-End. Los IDs de caso son referencias estables para futuros métodos de automatización y resultados de ejecución.

## 9. Criterios de entrada

- SauceDemo está disponible desde la laptop de pruebas.
- Las cuentas públicas de prueba y los datos de muestra necesarios están disponibles.
- El alcance, los escenarios y los resultados esperados están documentados.
- Antes de la ejecución automatizada, el proyecto local de Java/Maven y la configuración del navegador están listos.

## 10. Criterios de salida

- Los 15 casos tienen un resultado de ejecución para el ciclo planificado.
- Los resultados y los defectos observados están registrados en el libro.
- Los casos automatizados se ejecutaron y sus resultados fueron revisados cuando la fase de automatización esté lista.
- Todo caso bloqueado o sin ejecutar queda identificado con su motivo; no se establece un porcentaje mínimo de aprobación.

## 11. Riesgos y supuestos

- SauceDemo es un servicio externo de demostración; su disponibilidad y comportamiento no dependen de este proyecto.
- Las actualizaciones de la aplicación pueden cambiar el comportamiento o los localizadores y requerir mantenimiento de pruebas.
- Las cuentas públicas y el flujo de compra simulado no representan credenciales de producción ni pagos reales.
- La suite definida cubre flujos seleccionados y no afirma cubrir exhaustivamente todo el producto.
- La versión instalada de Chrome puede cambiar; el entorno registra la versión al preparar el plan.

## 12. Entregables y trabajo futuro

**Entregables iniciales:** este Test Plan en inglés y español, los libros de pruebas QA bilingües, las instrucciones del proyecto en `AGENTS.md` y un README inicial bilingüe.

**Fases posteriores:** framework de automatización Java/Maven y los 15 casos automatizados; reportes de ejecución y defectos; pruebas de accesibilidad; y CI/CD con GitHub Actions. API Testing se desarrollará por separado.

## 13. Mantenimiento del documento

Actualizar este plan cuando cambien el alcance acordado, el entorno de pruebas o el enfoque del proyecto. Mantener alineadas las versiones en inglés y español, y actualizar versión/fecha cuando haya una revisión material.
