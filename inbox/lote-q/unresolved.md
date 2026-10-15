# Lote Q: lo que no se pudo resolver (sin_revisar)

Todo queda `sin_revisar`. No se infirió nada por analogía.

## 1. Condiciones de tasa por prestamista (pedido 1)

**Para Claude:**
- **BIRF:** no hay base de días ni día de fijación en ninguna fuente del BIRF que leí (Condiciones Generales de Proyectos de Inversión revisadas el 2025-07-01, de Resultados 2023, de Políticas de Desarrollo 2023, nota de producto y página de Tesorería). Solo hay: SOFR del Período de Intereses "a plazo u otra base diseñada para replicar una estructura a plazo", período de seis meses de pago a pago, tasa que se reajusta en cada fecha de pago. No usé las notas de bonos del Banco Mundial porque son otro instrumento. Tampoco encontré el aviso del BIRF que pasó los préstamos de LIBOR a SOFR (CLM-Q-004 solo documenta la LIBOR en las Condiciones Generales de 2017).
- **BID:** la fórmula es SOFR compuesta en arrears sin rezago, ACT/360. El costo de fondeo trimestral y el margen cambian por trimestre y por año; la planilla histórica del costo de fondeo (producto FFF/SCF-SOFR-USD) está en la página de tasas del BID detrás de un botón que carga por JavaScript y no la pude bajar (CLM-Q-011). Los contratos del BID anteriores a 2022 no se leyeron.
- **CAF, BCIE:** son Term SOFR a 6 meses de CME. **Esa serie no es pública** (CME exige licencia; los promedios de SOFR a 30, 90 y 180 días del NY Fed no son Term SOFR). Para la fase 4 la tasa de referencia de estos préstamos solo se puede aproximar; no armé ninguna aproximación.
- **FONPLATA:** solo leí el modelo de 2022; no leí otros contratos.
- Cada fila de `condiciones_generales_de_tasa_por_prestamista.csv` trae la columna `lo_que_no_se_encontro`.
- **Para la resta que planteás en la fase 4** (tasa total congelada de SIGADE menos SOFR a la fecha de fijación): BID y FONPLATA no tienen fecha de fijación sino SOFR compuesta del período (usar el Índice SOFR de `sofr_indice_y_promedios...csv`); CAF y BCIE fijan Term SOFR dos días hábiles antes del período (no pública); BIRF no documenta la fecha.

## 2. SOFR y Term SOFR (pedido 2)

**Para Claude:** SOFR e Índice SOFR del NY Fed completos desde 2023-01-03 (los primeros datos de la API arrancan el 2023-01-03 porque el 2023-01-02 fue feriado). La última SOFR es la del 2026-10-14 (3,88%); la del 2026-10-15 todavía no figuraba al momento de la descarga. CME Term SOFR a 6 meses: no pública, no incluida (`tablas/term_sofr_6_meses_disponibilidad.csv`). La lectura de las páginas de CME se hizo con la herramienta de lectura web porque la descarga directa devolvió 403, así que ese punto no tiene archivo ni sha256.

## 3. SIGADE, Finanzas y RC 60/2026 (pedido 3)

**Para Claude:** sin cambios respecto de la revisión del lote P. Finanzas sigue en II Trimestre 2026; el 30-09 da 404; ONCP llega al 31-08-2026; OPC al 2026-10-06; el último CE que lista ADEBA es el 14715 (2026-10-01) y el 14716 da 404; las fichas de D30N6, T30A7 y T31Y7 no tienen documentos de octubre (CLM-Q-025 a CLM-Q-027). El corte sigue en 2026-06-30.

## 4. Represas Kirchner-Cepernic

**Para Claude:**
- No hay enmienda ni nota del prestamista con el reemplazo (búsqueda web del 2026-10-15; lo único público que encontré es el decreto con su acuerdo de enmienda y restablecimiento (SRC-1129), que mantiene LIBOR a 6 meses más 3,8%). Es posible que el reemplazo esté en un documento no público.
- Cláusula 35.3: se enmienda con consentimiento del Agente (Prestamistas Mayoritarios) y del Prestatario; el ajuste que haya designado el Relevant Nominating Body (banco central, regulador o comité de ellos, o el Financial Stability Board) manda. La definición de Tasa Sustituta (Replacement Benchmark) prioriza lo que designe el administrador de la LIBOR o ese organismo, luego lo que los Prestamistas Mayoritarios y el Prestatario consideren aceptado o apropiado.
- **0,42826% para 6 meses:** es el ajuste de ISDA, fijado el 2021-03-05, y el ARRC (2023-03-15) lo recomienda sobre CME Term SOFR a 6 meses para contratos LIBOR que no son de consumo. Lo cito como indicaste; el contrato no dice que lo adoptó ni sobre qué tasa. Si usás SOFR compuesta u otra base en vez de Term SOFR, el ajuste puede no corresponder.
- El texto del acuerdo (2022) pone base ACT/360 y períodos de seis meses.
