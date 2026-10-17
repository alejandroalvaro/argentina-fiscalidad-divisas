# Lote AP: instrumentos en dólares que se pagan en pesos, renovaciones de LIT y 2024-02

Fuente base: hoja A.4 del boletín mensual de Finanzas al 30-09-2026 (SRC-2049, mismo archivo que SRC-9002; A.4 llega hasta 2026-06) y la hoja "Canjes- Conversiones" de ONCP (SRC-2023 a SRC-2026) para separar canje de efectivo. Montos en USD millones. Cada fila de las tablas y cada claim `CLM-AP-xxx` (estado `sin_revisar`) cita la fila y la celda de A.4.

## Cómo identifiqué los instrumentos "dólares pagados en pesos"

- ONCP aclara que la columna Tipo Moneda refiere a la moneda de pago y Moneda de Origen a la moneda de denominación (CLM-AP-063). Los BONTE U$S "Paga en pesos" y las LELINK aparecen como instrumentos en dólares con pago en pesos (CLM-AP-064).
- Incluí en la tabla: BONAR DUAL U$S (filas 298 a 300 y 320 a 326 de A.4), BONTE U$S (filas 402 a 413, excluyendo BONTE 6,5% 30-11-2029, que paga en dólares) y LETES U$S "Pagan en pesos" (fila 234 amortización, fila 27 emisión; ahí están las LELINK). Para BONAR DUAL, el boletín y ONCP no dicen "paga en pesos" en el nombre; lo infiero porque A.5 no lo cuenta como pago en moneda extranjera (2024-08: A.5 USD 154,5 M contra BONAR DUAL de USD 1.546 M, CLM-AP-065). Es inferencia, no dato.
- No incluí: BONAR U$S 2027 a 2029 y BONTE 6,5% 2029 (pagan en dólares), bonos globales, LIT ni letras con organismos públicos (van a otra tabla).

## 1. Amortizaciones de esos instrumentos (tabla `usd_pagan_en_pesos_amortizacion_por_instrumento_mes.csv`, resumen mensual en `resumen_mensual_usd_pagan_en_pesos.csv`)

Total A.4 de 2023-12 a 2026-06: USD 80.371 M, repartidos así:

| Concepto | USD M |
| --- | --- |
| Canje sin efectivo según ONCP | 36.226 |
| Pago al vencimiento sin canje en ese mes | 33.551 |
| LELINK 2026 y BONTE 2026 con parte canje y resto sin separar de forma exacta (resto) | 8.144 |
| Baja anticipada sin conversión en ONCP, no separable (BONAR DUAL 28-02-2024 en 2023-12) | 2.450 |

- **Canje de 2024-03 (RC 16/2024, 15-03-2024): USD 25.172,8 M, separado exactamente.** Las bajas de ONCP coinciden fila por fila con A.4 (BONAR DUAL 29-11-2024 10.914,1; 30-08-2024 5.329,0; 30-04-2024 2.885,6; 30-06-2024 2.703,2; BONTE 30-09-2024 1.760,0; BONTE 30-04-2024 1.580,9; CLM-AP-062). Lo que quedó de cada bono se pagó después al vencimiento (por ejemplo BONAR DUAL 30-08-2024: USD 1.546,3 M en 2024-08).
- **RC 4/2025 (29-01-2025):** ONCP lista BONTE U$S 30-06-2025 como baja en enero de 2025, pero A.4 muestra 0 para esa fila en 2025-01 y los valores de baja de ONCP están en una unidad que la hoja no indica (del orden de 1.029.560, sin duda en pesos). No es separable en USD con estas fuentes. El BONAR DUAL 31-01-2025 (USD 8.596,4 M) no tiene baja por canje en ONCP en enero y lo clasifico como pago al vencimiento.
- **2026 (ONCP, conversiones de LELINK y BONTE U$S 30-06-2026):** A.4 agrega todas las LELINK en la fila 234, por lo que la separación es aproximada. Canje según ONCP: 2026-01 USD 4.793,9 M (de A.4 7.770,9), 2026-02 USD 1.539,4 M (de 2.394,2), 2026-04 USD 1.626,3 M (de 3.888,4), 2026-05 USD 288,6 M del BONTE 30-06-2026 (todo canje), 2026-06 USD 2.804,7 M (de 4.855,2). La hoja ONCP no indica unidad de los valores de baja; los tomé en USD millones porque en la conversión de 2024-03 esa unidad coincide con A.4. Marcado como aproximado en cada fila.
- **Vencimiento en fin de semana:** BONAR DUAL 30-06-2024 aparece 293,6 en 2024-06 y 2.372,3 en 2024-07 (30-06-2024 fue domingo).
- **Caso a revisar:** 2023-12 muestra USD 2.449,5 M de baja del BONAR DUAL 28-02-2024, dos meses antes del vencimiento, sin conversión en ONCP y con efecto en caja en el AIF de 2023-12 (la conciliación del lote AO deja ese mes casi cerrado con esa fila). Lo marco como inseparable.

## 2. Emisiones de esos instrumentos (tabla `usd_pagan_en_pesos_emision_por_instrumento_mes.csv`)

Total A.4 sección 1 de 2023-12 a 2026-06: USD 39.996 M, de los cuales USD 11.230 M son entrega por conversión según ONCP (todo en 2026: LELINK y BONTE U$S entregados en las conversiones de 2026) y USD 28.767 M se estiman como colocación en efectivo (residuo). En 2024 y 2025 no hay entregas por canje de estos instrumentos en ONCP: la RC 16/2024 emitió BONCER en pesos y la RC 4/2025 bonos duales en pesos, es decir, no generó emisión de dólares pagados en pesos. En 2026 el residuo es aproximado por la misma razón de unidad. Los BONAR DUAL U$S no tienen emisiones en la ventana.

## 3. LIT y letras en dólares con organismos públicos (tabla `lit_y_letras_usd_organismos_publicos_emision_amortizacion_mensual.csv`)

- La tabla trae por mes la emisión y la amortización de LETRA BCRA - U$S (filas 209 y 420) y de las letras en dólares con FGS, FODER, FONDCE, Playas Ferroviarias, CMEA, Intercargo, Provincia de Mendoza y Letras en Garantía, junto con la amortización y el endeudamiento ME del AIF, el capital ME de A.5 y un proxy de renovación bruta (mínimo entre emisión y amortización de LIT más públicas).
- **Renovación bruta visible:** LIT en 2024-01 (emisión USD 9.644 M, amortización USD 7.896,8 M, AIF amortización USD 10.274 M y endeudamiento USD 14.372 M), 2024-07 (2.781/2.652) y 2024-08 (3.052/3.043). Letras en dólares con organismos públicos, de a USD 1.200 M aprox., renovadas trimestralmente en 2024-02, 2024-08, 2025-02 y 2026-02 (emisión y amortización de unos USD 1.190 a 1.230 M). El proxy cubre 77% de la amortización ME del AIF en 2024-01, 68% en 2024-08, 89% en 2025-02, 56% en 2026-02 y 34% en 2024-07.
- **No es renovación sino recompra:** las amortizaciones de LIT de 2025-05 (USD 13.617 M), 2025-08 (3.269) y 2026-05 (22.284), que corresponden a las RC 21/2025, 37/2025 y 27/2026; no hay emisión de LIT en esos meses y el proxy da 0. La amortización de A.4 de esas filas es valor nominal, no efectivo.
- **BNA:** A.4 no tiene una fila de letras con el Banco Nación. No pude identificar esa tenencia.
- **Letras en Garantía U$S** (fila 275: USD 1.345 M amortizados en la ventana): las dejé separadas porque no sé de qué tenedor se trata.

## 4. 2024-02 (tabla `explicacion_2024-02_amortizacion_me_aif.csv`)

El detalle de A.4 no explica los USD 2.426 M. Componentes: A.5 (solo préstamos: CAF 1.047,7, BID 54,8, BIRF 3,2, otros 5,5) USD 1.111,2 M; letras con organismos públicos (FGS 1.071,6, FODER 74,9, FONDCE 4,8, Playas 22,4) USD 1.173,7 M; BONAR DUAL 28-02-2024 USD 4.938,7 M. Suma USD 7.223,6 M contra AIF USD 9.649,1 M: residuo USD 2.425,5 M (CLM-AP-073 a 076).
- Descarté dos causas: (a) usar el A 3500 del 28-02-2024 (841,75) en lugar del promedio (834,91) baja el AIF a USD 9.570 M y no cierra; (b) la fila `BONO R.A./U$S/STEP UP/09-07-2035` muestra USD 7.595,9 M en 2024-02 sin contrapartida en A.5 ni emisión, y si fuera caja el AIF sería mayor, así que no es caja.
- Otras filas de febrero son en pesos (LETES $ 2.507,8; BONCER 4,25% 1.188,8) y no entran en la amortización ME.
- Queda sin explicar. Hipótesis sin respaldo: que el AIF valúe el BONAR DUAL con otra fórmula de pago (dual) o que registre otra operación; no encontré fuente.

## 5. Pendientes de publicación

- **Informe sobre Bancos con datos de agosto de 2026:** publicado el 16-10-2026 (SRC-2050, página con resumen ejecutivo y sha256; el PDF devolvió 502, SRC-2051). El resumen ejecutivo trae crédito, depósitos y morosidad; no abre tenencia de títulos del Tesoro.
- **Balance cambiario de septiembre de 2026:** no publicado; el portal del BCRA lo anuncia para el 30-10-2026 (SRC-2052, CLM-AP-078).
- **Boletín de Finanzas de octubre:** no lo encontré. La URL equivalente `boletin_mensual_31_10_2026.xlsx` da 404 y el archivo de 30-09-2026 sigue idéntico (mismo sha256, CLM-AP-079). A.4 sigue llegando hasta 2026-06.
