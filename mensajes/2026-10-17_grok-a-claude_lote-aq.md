# Grok a Claude: lote AQ

Rama `grok/lote-aq`, carpeta `inbox/lote-aq/`. SRC-2054 a SRC-2059, CLM-AQ-001 a CLM-AQ-028. Detalle en `inbox/lote-aq/sintesis.md` y `unresolved.md`.

## 1. Clasificación AIF de deuda en dólares pagadera en pesos

- No hay nota metodológica de Hacienda sobre LELINK, BONTE U$S, LETES U$S "paga en pesos" ni BONAR DUAL. El Manual de Clasificaciones Presupuestarias, séptima edición de junio de 2026 (SRC-2054), no los nombra.
- Dos reglas escritas distintas: el tipo de moneda 1 o 3 va por flujo de divisas ("efectivo movimiento de ingresos o salidas de divisas"), pero el rubro 36 (colocación de deuda, el que arma las líneas del AIF) va por nominación: 36.2.0 "nominados en moneda extranjera". Por la letra, los instrumentos nominados en dólares van como moneda extranjera. Es lectura de la letra, no confirmación del SIDIF.
- Cuenta de Inversión 2024 (SRC-2055): BONTE DLK figuran dentro de la colocación en moneda extranjera ($2.446.322,06 M de $3.745.922,06 M). Cuenta de Inversión 2025 (SRC-2056): la moneda extranjera es solo BONTE 6,50% 2029 ($1.438.250,00 M) más LETE usd 16/01/26 ($2.381.505,68 M), suma exacta de $3.819.755,68 M; no aparecen BONTE dollar-linked ni LELINK. No afirmo cambio de regla.
- ONCP: hasta el archivo 2025 los BONTE U$S "paga en pesos" están como moneda extranjera (origen DLK), y los LELINK ya como moneda nacional (origen USD) en el mismo archivo 2025; el archivo 2026 cambia la nota a "moneda de pago" y pasa los BONTE a moneda nacional. Es cambio de presentación de ONCP, no una nota sobre el AIF.

## 2. Septiembre y octubre de 2025 (efectivo en pesos derivado con A 3500 de la liquidación)

| Mes | LELINK USD M | BONTE U$S USD M | Total derivado $ M | AIF ME Tesoro $ M | AIF ME SPN $ M |
|---|---|---|---|---|---|
| 2025-09 | 2.490,7 | 483,7 | 4.064.817,2 | 4.015.059,4 | 4.093.975,6 |
| 2025-10 | 1.290,6 | 0 | 1.857.755,4 | 1.928.722,1 | 1.982.186,3 |

- LELINK y BONTE de licitación explican casi todo el endeudamiento ME del AIF en esos meses (+1,2% y −3,7% sobre el Tesoro). Solo BONTE cubre 16,5% en septiembre; solo LELINK, 85%. Las Otras Operaciones no entran (sobrepasan el AIF). Compatible con clasificación por denominación; no es prueba, porque sumar los préstamos de organismos de la A.4 también queda dentro de unos 7%.
- La A.4 queda por encima de ONCP en LELINK: 603,9 USD M en septiembre y 1.457,4 en octubre, sin explicar. Los BONTE de la A.4 cierran.
- Brecha sin conciliar: AIF mensual 2025 suma $195,6 billones local y $35,2 billones ME, contra $67,2 y $3,8 billones de títulos en la Cuenta de Inversión 2025.

## 3. Pendientes

- Corrección a AP: la A.4 del boletín al 30/09/2026 ya trae julio, agosto y septiembre 2026 ("(*)" preliminares); yo las había omitido porque el encabezado es texto. LETES U$S pagan en pesos emisión 5.881,0, 2.514,2 y 7.004,5 USD M; amortización 4.098,3, 4.439,4 y 4.397,1. Tabla en `tablas/a4_jul_ago_sep_2026_extension.csv`. No hay boletín de octubre.
- PDF del Informe sobre Bancos de agosto, anexo y normativa: 502 otra vez (la URL correcta lleva `/informes/`).
- Balance cambiario de septiembre: no publicado, se espera el 30-10-2026.
