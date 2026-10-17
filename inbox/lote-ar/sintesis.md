# Lote AR: colocaciones y amortizaciones de LELINK, BONTE U$S "paga en pesos" y BONAR DUAL, 2023-12 a 2026-09

Corrida del 17-10-2026 (hora de Bahía). No hay fuentes nuevas (usé SRC-2023 a SRC-2026 de ONCP, SRC-2049 de la A.4, SRC-2040 para la A 3500 y los AIF mensuales de ids_am); `sources.csv` queda con encabezado solo. Claims CLM-AR-001 a CLM-AR-014. Lo marcado "derivado" lo calculé yo.

## Unidades (importa para no mezclar)

- Archivos ONCP 2023 y 2024: los BONTE U$S (denominación DLK) vienen en **millones de pesos**; ONCP ya los convirtió con "el dólar a la fecha de colocación" (nota (**)). El USD de esos años es derivado: pesos de ONCP divididos por la A 3500 de la liquidación.
- Archivos 2025 y 2026: LELINK y BONTE vienen en **USD millones** (aunque el título del 2025 diga "millones de pesos"). El pesos es derivado: efectivo USD por A 3500 de la fecha de liquidación (BCRA API variable 5, SRC-2040). Verificado contra la A.4 (BONTE de septiembre de 2025: 485,1 en ambas).

## 1. Colocaciones por licitación en efectivo (criterio del escenario A de AQ)

Tablas: `colocaciones_licitacion_efectivo_por_mes_e_instrumento.csv` (una fila por mes e instrumento, con el AIF ME del Tesoro y del total SPN al lado), `colocaciones_licitacion_efectivo_total_mensual_vs_aif_me.csv` (los 34 meses, con y sin BONTE DUAL) y `colocaciones_licitacion_detalle_tramos.csv` (55 tramos con hoja y fila de origen).

- El primer BONTE U$S de la serie es de febrero de 2024 y el primer LELINK de febrero de 2025. No hay colocación en efectivo en 2023-12 ni 2024-01.
- **BONAR DUAL U$S: no hubo colocaciones por licitación desde 2023-12.** Solo aparece como baja en canjes y conversiones (la amortización sin efectivo de marzo de 2024 de AP).
- Meses donde LELINK más BONTE de licitación explican entre 75% y 105% del AIF ME del Tesoro: 2024-04 (92%), 2024-10 (83%), 2025-03 (96%), 2025-09 (101%), 2025-10 (96%), 2025-11 (90%) y 2026-08 (79%). El resto de los meses con colocación explican menos (de 1% a 75%), y hay meses sin colocación con AIF ME alto (2024-01 con $11,8 billones, 2024-08, 2025-08). Ahí el AIF ME sale de otros componentes (préstamos, canjes, otras letras) que esta serie no mide. Septiembre de 2026 no tiene AIF en el lote AM, queda en blanco.
- Julio de 2026 trae un **BONTE DUAL/$/TAMAR o DLK/31-01-2028** (VN 3.467, efectivo 3.148,4 USD M según la unidad del archivo, unos $4,69 billones derivados), con Tipo Moneda "nacional" y origen USD. Lo separé: julio da $3,34 billones sin él y $8,03 billones con él, contra un AIF ME de $14,65 billones. No sé cómo lo carga el AIF; queda fuera del criterio A.

## 2. Amortizaciones en base caja

Tablas `amortizacion_caja_por_instrumento_mes_2023-12_2026-09.csv` y `amortizacion_caja_resumen_mensual_2023-12_2026-09.csv`. Parto de la A.4 (como en AP, ahora hasta 2026-09) y resto las bajas por canje o conversión de la hoja Canjes- Conversiones de ONCP.

- Total 2023-12 a 2026-09 (USD M): A.4 93.305,6; conversión o canje sin efectivo 42.719,8; pago al vencimiento sin baja en ONCP 33.551,2; mixto estimado en efectivo 14.585,1; baja anticipada inseparable 2.449,5 (2023-12, BONAR DUAL 28-02-2024). Caja estimada entre 48.136,3 y 50.585,8.
- **Otras Operaciones de ONCP** (`otras_operaciones_oncp_marcadas.csv`, 16 filas, sin efectivo ni dato de la baja). Las marqué en la columna final de la tabla de amortización. Lo más relevante: en octubre y noviembre de 2025 la A.4 trae amortización de LELINK por 3.231,1 y 4.010,0 USD M sin baja por conversión en ONCP, y Otras Operaciones trae LELINK por VN 3.311,4 (octubre) y 3.642,3 (noviembre). Mismo orden de magnitud. **Hipótesis, no probada:** son canjes o rescates con tenedores públicos contabilizados como amortización en la A.4 sin caja; si fuera así, la amortización en efectivo de esos meses es bastante menor que la que figura. Hay además pares de VN idéntico el mismo día (02-10-2025, 13-04-2026, 06-07-2026, 07-09-2026) que no puedo interpretar.

## 3. Julio a septiembre de 2026, LETES U$S "pagan en pesos" (A.4 fila 234)

Tabla `letes_usd_pagan_en_pesos_amortizacion_2026-07_a_09_vencimiento_vs_conversion.csv`.

| Mes | A.4 amortización | Conversión (ONCP 2026, Canjes- Conversiones) | Pago al vencimiento aproximado |
|---|---|---|---|
| 2026-07 | 4.098,3 | 1.851,2 (LELINK 31-07-2026, 24-07, norma 45/2026) | 2.247,1 |
| 2026-08 | 4.439,4 | 1.344,3 (LELINK 31-08-2026, 21-08, norma 50/2026) | 3.095,1 |
| 2026-09 | 4.397,1 | 3.298,6 (LELINK 30-09-2026, 24-09, norma 56/2026) | 1.098,5 |
| Total | 12.934,8 | 6.494,1 | 6.440,7 |

Aproximado: la A.4 agrega todas las LELINK en una fila, así que no verifico qué otras LELINK vencieron en cada mes. En septiembre, la conversión es 75% de la amortización.

## 4. Pendientes del BCRA

El PDF del Informe sobre Bancos de agosto, su anexo y el de julio siguen en HTTP 502. La página del balance cambiario sirve con el mismo sha256 que SRC-2053 (sin balance de septiembre); la página mensual da 502. Se espera el 30-10-2026.
