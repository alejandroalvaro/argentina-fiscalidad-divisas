# Lote AQ: clasificación AIF de la deuda en dólares pagadera en pesos, colocaciones de 2025-09 y 2025-10, pendientes

Fecha de corrida: 17-10-2026 (hora de Bahía). Fuentes nuevas: SRC-2054 a SRC-2059. Reutilizo SRC-2023 a SRC-2026 (ONCP), SRC-2049 (boletín de Finanzas) y SRC-2010 y SRC-2011 (AIF de septiembre y octubre de 2025). Reclamos: CLM-AQ-001 a CLM-AQ-028. Todo lo marcado "derivado" lo calculé yo y no es dato de la fuente.

## 1. Cómo clasifica el AIF la deuda en dólares pagadera en pesos

**No hay una nota metodológica de Hacienda sobre este caso.** Busqué en el Manual de Clasificaciones Presupuestarias, séptima edición, junio de 2026 (SRC-2054): el texto no nombra LELINK, bonos duales ni instrumentos dollar-linked (CLM-AQ-006). Tampoco encontré nota metodológica del esquema AIF (la ONP publica planillas con las líneas, no una nota sobre moneda de pago).

Lo que sí hay son dos reglas escritas que no dicen lo mismo:

- **Tipo de moneda (código 1 o 3)**: criterio de flujo de divisas, para el presupuesto de divisas y el balance de pagos. Se pone 3 cuando la transacción es un "efectivo movimiento de ingresos o salidas de divisas" y, en la cuenta financiera, cuando la deuda está "convenida en moneda extranjera" (CLM-AQ-001 y 002). Un título que paga en pesos no mueve divisas, pero el texto no lo resuelve.
- **Rubro de recursos 36 (colocación de deuda)**: la moneda es la de nominación del título. 36.1.0 "nominados en la moneda nacional de curso legal", 36.2.0 "nominados en moneda extranjera" (CLM-AQ-003). Estos rubros son los que dan las líneas "colocación de deuda en moneda nacional/extranjera" de la cuenta AIF. Por la letra, LELINK, BONTE U$S y BONAR DUAL U$S (nominados en dólares) caen en 36.2.0. Es una lectura de la letra del Manual, no una confirmación de cómo carga cada caso el SIDIF.
- El Manual excluye del rubro 36 a los títulos intransferibles (los manda a 37, préstamos), pero la Cuenta de Inversión 2024 y 2025 incluye las letras intransferibles y el LETE en dólares dentro de "colocación de deuda en moneda extranjera" (CLM-AQ-004, 007 y 008). La práctica contable no sigue todo al pie de la letra del Manual.

**Tablas oficiales que muestran en qué línea cae una colocación concreta:**

| Fuente | Qué muestra |
|---|---|
| Cuenta de Inversión 2024 (SRC-2055, SRC-2057) | BONTE DLK (vto. 30/06/2025, 15/12/2025 y 30/06/2026) dentro de "Colocación de Bonos en dólares", moneda extranjera: $2.446.322,06 M de $3.745.922,06 M (CLM-AQ-007, 011) |
| Cuenta de Inversión 2025 (SRC-2056, SRC-2058) | Moneda extranjera = BONTE 6,50% vto. 30/11/29 ($1.438.250,00 M) más LETE usd cupón cero 16/01/26 ($2.381.505,68 M); suma exacta $3.819.755,68 M. No figuran BONTE dollar-linked ni LELINK en esa línea (CLM-AQ-008, 009, 010) |

Entre el ejercicio 2024 y el 2025 de la Cuenta de Inversión, entonces, los BONTE dollar-linked pasan de moneda extranjera a no figurar en moneda extranjera. No puedo decir que haya un cambio de regla: la narrativa solo destaca los principales y no tengo el detalle por instrumento del 2025. Queda como hallazgo a verificar.

**Cuenta de Inversión 2023 y anteriores**: una copia de OPC de la Cuenta de Inversión (descargas opc.gob.ar/download/34294 y 30591) dice, según el resumen del buscador, que los bonos duales y USD linked pagaderos en pesos van como "colocaciones de títulos denominados en moneda extranjera". No pude bajar esos PDF (el servidor devuelve una página 410 con botón de descarga), así que no los registré como fuente ni sirven de evidencia. Ver unresolved.md.

**Presentación de ONCP** (CLM-AQ-012 a 015). Es otro documento y otra clasificación, pero ayuda a ver el criterio de moneda:

| Archivo | Nota al pie de la columna "Tipo Moneda" | BONTE U$S "Paga en pesos" | LELINK | BONAR DUAL U$S |
|---|---|---|---|---|
| 2023 (SRC-2023) | "s/norma de emisión" | Moneda extranjera, origen DLK | no existe | Moneda extranjera, origen DLK |
| 2024 (SRC-2024) | "s/norma de emisión" | Moneda extranjera, origen DLK | no existe | no figura |
| 2025 (SRC-2025) | "s/norma de emisión" | Moneda extranjera, origen DLK | **Moneda nacional**, origen USD | no figura |
| 2026 (SRC-2026) | "moneda de pago" | **Moneda nacional**, origen USD | Moneda nacional, origen USD | no figura (hay duales en pesos) |

Dentro del archivo 2025 conviven BONTE U$S como moneda extranjera y LELINK como moneda nacional, con la misma nota al pie. El cambio de criterio a "moneda de pago" aparece en el archivo 2026.

**Respuesta corta para D-017**: no hay norma publicada que diga que el AIF trate estos instrumentos como moneda local; lo que sí hay son indicios de que hasta 2024 los BONTE dollar-linked iban como moneda extranjera (Cuenta de Inversión 2024), y la prueba numérica de abajo es compatible con que en septiembre y octubre de 2025 el AIF mensual también cargue LELINK y BONTE U$S como moneda extranjera.

## 2. Septiembre y octubre de 2025: ONCP contra AIF

Valor efectivo en pesos **derivado** (valor efectivo en USD de ONCP por A 3500 de la fecha de liquidación, BCRA API v4.0 variable 5, SRC-2040; ONCP no trae efectivo en pesos). No es el tipo de cambio de registro del Tesoro.

| Mes | LELINK, USD M efectivo | BONTE U$S paga en pesos, USD M efectivo | Total, USD M | Total derivado, $ M | AIF ME Tesoro, $ M | AIF ME total SPN, $ M |
|---|---|---|---|---|---|---|
| 2025-09 (liq. 30-09, A 3500 1.366,5833) | 2.490,7 | 483,7 | 2.974,4 | 4.064.817,2 | 4.015.059,4 | 4.093.975,6 |
| 2025-10 (liq. 17-10, A 3500 1.439,5) | 1.290,6 | 0 | 1.290,6 | 1.857.755,4 | 1.928.722,1 | 1.982.186,3 |

- Septiembre: LELINK más BONTE de licitación quedan +1,2% sobre el Tesoro y −0,7% bajo el total SPN. Octubre: −3,7% y −6,3%.
- Por instrumento en septiembre, LELINK es 85% del AIF de moneda extranjera y BONTE 16,5%. Con BONTE solo no cierra (−83,5%); con LELINK solo, −15,2%.
- Si se suman las "Otras Operaciones" (sin efectivo en ONCP, uso VN como aproximación), el total pasa muy por encima del AIF (+41% en septiembre; muchas veces en octubre). El AIF de caja no incluye esas operaciones.
- Si se suman también los préstamos de organismos internacionales y bilaterales de la A.4, queda +6,7% y +7,5% sobre el Tesoro. Con esta precisión no distingo "LELINK más BONTE" de "LELINK más BONTE más préstamos", porque el AIF mensual no abre las líneas dentro de endeudamiento en moneda extranjera.
- Lectura: LELINK y BONTE U$S "paga en pesos" de licitación **explican casi todo** el endeudamiento en moneda extranjera del AIF de esos dos meses. Eso es compatible con que el AIF los clasifique por denominación (moneda extranjera) y no por moneda de pago. No es prueba de la regla.

**Otras Operaciones y conciliación con A.4** (CLM-AQ-020 y 021). Septiembre: LELINK de ONCP (licitación VN 2.494,6 más Otras Operaciones 1.097,7) suma 3.592,3 contra 4.196,2 de la A.4: faltan 603,9 sin explicar. Octubre: 4.615,0 contra 6.072,4: faltan 1.457,4 sin explicar, cifra casi igual al VN 1457 de cada fila del 02-10-2025 (no saco conclusión de eso). Los BONTE U$S de la A.4 sí cierran con ONCP. Las letras BCRA U$S son magnitudes mínimas (7,4 y 6,0 USD M, CLM-AQ-022).

**Brecha sin resolver con la Cuenta de Inversión 2025** (CLM-AQ-024): sumando enero a diciembre, el AIF mensual (Tesoro) da $195.630.032,4 M de endeudamiento en moneda local y $35.177.828,2 M en moneda extranjera; la Cuenta de Inversión trae títulos en pesos por $67.216.608,13 M y títulos en moneda extranjera por $3.819.755,68 M (más préstamos largo plazo de $24.917.440,05 M). No concilié esas bases y no sé si el AIF mensual incluye operaciones no monetarias o canjes.

Archivos de datos en `tablas/`: `oncp_colocaciones_2025-09_2025-10_detalle.csv`, `escenarios_vs_aif_endeudamiento_me_2025-09_2025-10.csv`, `oncp_vs_a4_emision_2025-09_2025-10.csv`, `oncp_tipo_moneda_por_familia_y_archivo.csv`, `cuenta_inversion_2024_2025_colocacion_deuda_me.csv`.

## 3. Pendientes

- **Boletín de Finanzas**: corrijo la nota de AP. La A.4 del boletín ya trae julio, agosto y septiembre de 2026 como columnas "(*)" (preliminares); yo las había dejado afuera porque el encabezado es texto. LETES U$S pagan en pesos, emisión USD M: 5.881,0, 2.514,2 y 7.004,5; amortización: 4.098,3, 4.439,4 y 4.397,1. Tabla `a4_jul_ago_sep_2026_extension.csv`. No hay boletín de octubre (CLM-AQ-025 y 026).
- **PDF del Informe sobre Bancos de agosto**: sigue en 502 en el PDF, el anexo xlsx y el PDF de normativa (tres intentos cada uno). La URL correcta tiene la carpeta `/informes/` (CLM-AQ-027).
- **Balance cambiario de septiembre**: no está publicado a la fecha (el cronograma lo anuncia para el 30-10-2026; la página mensual devolvió 502). Pendiente (CLM-AQ-028).
