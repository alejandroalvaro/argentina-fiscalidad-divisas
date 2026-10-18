# Anexo C. Datos

## C.1 Fuentes principales

| Fuente | Qué aporta | Identificador | Capítulos |
|---|---|---|---|
| SIGADE al 30-06-2026, Oficina Nacional de Crédito Público | Cada operación de deuda de la Administración Central | SRC-0102 | 2 |
| Planilla trimestral de deuda, Secretaría de Finanzas | Saldos, flujos y perfil de vencimientos oficiales | SRC-0103, SRC-1005 | 2, 8 |
| Boletín mensual de la Secretaría de Finanzas, serie 2019-2026 | Deuda por moneda (A.1, A.3), operaciones (A.4) y pagos por moneda de pago (A.5) | SRC-9002 | 2, 3, 5 |
| Deuda de la Administración Central por tenedor | Sector público, privados y organismos | SRC-1014, SRC-1706 a SRC-1715 | 2, 6 |
| Esquema ahorro-inversión-financiamiento, base caja, Secretaría de Hacienda | Ingresos, gastos, resultado y financiamiento del sector público nacional | lotes AM y AN | 3, 5 |
| Balance cambiario, BCRA | Compras y ventas de divisas por concepto | SRC-1604 | 4 |
| Series.xlsm, BCRA | Factores de la base monetaria e instrumentos del BCRA | SRC-1625 | 3 |
| Estados contables del BCRA 2023 a 2025 | Intereses pagados y cobrados, utilidades | SRC-1673 y siguientes | 3, 6 |
| Informe sobre Bancos, BCRA | Resultados del sistema financiero | lote AJ | 6 |
| Informes del personal técnico del FMI, acuerdo de 2025 y revisiones | Metas y resultados de reservas netas, desembolsos | SRC-1263, SRC-1270, SRC-1271, SRC-1611 | 4 |
| Resoluciones conjuntas de Finanzas y Hacienda | Recompras, canjes y conversiones | SRC-1257, SRC-2031, SRC-2042, SRC-2047, SRC-2063, SRC-2064 | 5, 6 |
| Compras de divisas del Tesoro (informes del BCRA y comunicados) | Compras al BCRA y en el mercado | lote AI | 5 |
| Licitaciones y deuda escrita en dólares pagada en pesos | Colocaciones y pagos en pesos de deuda en dólares | lotes AQ y AR | 5, 7 |
| Zips mensuales de exportaciones, ARCA | Valor FOB por posición | SRC-1375 a SRC-1491 | anexo A |
| Recaudación de derechos de exportación, datos.gob.ar | Derechos cobrados | lote D | anexo A |
| IPC nacional, INDEC | Deflactor de los pesos | SRC-2028 | 3, 5 |
| Comunicación A 3500, BCRA | Tipo de cambio de referencia | `series/bcra_a3500.csv` | todos |

Un lote es una entrega del agente de búsqueda, guardada en la carpeta `inbox/lote-…` del repositorio con su lista de fuentes, sus tablas y sus notas. La lista completa de fuentes, con URL, fecha de descarga y huella sha256, está en `manifests/downloads.csv` y en el `sources.csv` de cada lote.

## C.2 Salidas que sostienen el informe

| Salida | Comando | Archivo |
|---|---|---|
| Calendario de pagos y necesidad de divisas | `argfx calendario` | `data/calendario/` |
| Conciliación, consolidación y tenencias | `argfx conciliacion` | `data/conciliacion/` |
| Interés capitalizado por trimestre | `argfx devengados` | `data/conciliacion/devengados_trimestral.csv` |
| Diagramas del mandato | `argfx flujos` | `data/informe/flujos_*.csv` y `.html` |
| Derechos estimados y cobrados | `argfx derechos` | `data/simulacion/derechos_*.csv` |
| Modelo de la fase 4: el mandato con cobro en dólares y la proyección a 2036 | `argfx simular` | `data/simulacion/mandato_*` y `proyeccion_*` |
| Gráficos de barras | `argfx graficos` | `data/informe/grafico_*.csv` y `.html` |
| Proyección del FMI del saldo comercial | | `series/fmi_balanza_proyectada.csv` (SRC-1263) |

Todas las salidas de este borrador se regeneraron el 17 de octubre de 2026 desde la versión `57a7c62` del repositorio.

## C.3 Decisiones de método

Las decisiones del investigador están en `docs/DECISIONES.md`, con fecha y fundamento. Las que más pesan en este informe son:

- **D-001.** Reservas netas con la definición del acuerdo con el FMI, sin restar los depósitos del Tesoro.
- **D-008.** El análisis incorpora las operaciones posteriores al corte de SIGADE.
- **D-009.** Los intereses se miden también en base devengada.
- **D-011.** Las letras en garantía del FODER son deuda contingente.
- **D-016.** El informe trata la naturaleza bimonetaria de la deuda; el cobro en dólares pasa a anexo.
- **D-017.** Cada moneda en su unidad, gráficos por moneda y glosario.
- **D-018.** Los supuestos de la corrida del modelo de la fase 4.

## C.4 Cómo verificar una cifra

Todo lo que sostiene este informe es público:

- **El repositorio**, con el código, las pruebas, los manifiestos, las tablas de cada lote, las decisiones de método y los mensajes entre los agentes, con su historial completo: https://github.com/alejandroalvaro/argentina-fiscalidad-divisas
- **Los documentos originales oficiales**, tal como se bajaron, en https://datos.8kgm.com.br. Cada original está en `objects/sha256/` seguido de su huella. La tabla `manifests/publicacion.csv` da, para cada código SRC, el emisor, la URL de origen, la huella y la dirección pública.
- **Los documentos de terceros** (notas de prensa, trabajos académicos, informes de cámaras privadas y copias de textos oficiales alojadas en sitios de terceros), 140 de 1.214, no se reproducen porque sus derechos son de sus autores. La misma tabla da su URL de origen y su huella, para que quien los baje pueda comprobar que es el mismo archivo.

Para comprobar un original alcanza con bajarlo y calcular su huella (`shasum -a 256 archivo` en macOS o Linux, `certutil -hashfile archivo SHA256` en Windows): tiene que coincidir con el nombre del objeto. Para rehacer un cálculo, el repositorio explica cómo instalar el código y qué comando produce cada salida (sección C.2).

El código se distribuye con la licencia MIT, y los textos y las tablas propias, con la licencia Creative Commons Atribución 4.0 (CC BY 4.0). Los documentos originales siguen siendo de sus emisores.

