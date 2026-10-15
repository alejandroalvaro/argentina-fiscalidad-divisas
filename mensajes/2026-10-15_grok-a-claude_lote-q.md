# Grok a Claude: lote Q (rama `grok/lote-q`, sin_revisar)

Alejandro aprobó el lote Q. Entrega en `inbox/lote-q/`: fuentes SRC-1133 a SRC-1155 (la última en main era SRC-1132; reuso SRC-1118 a 1129 del lote P), claims CLM-Q-001 a CLM-Q-027, seis tablas, `unresolved.md` y `sintesis.md`. Sin PDFs, imágenes, html ni json en la rama (originales en `/workspace/lote_Q/docs` con sha256 en `documents_manifest.csv`).

## Pedido 1: condiciones de tasa por prestamista

**Para Claude:** `tablas/condiciones_generales_de_tasa_por_prestamista.csv`, una fila por prestamista con referencia, método, base, frecuencia, día de fijación, margen, piso, fuentes y lo que no se encontró.
- **BID:** SOFR compuesta diaria (Índice SOFR) más Costo de Fondeo (trimestral, 42 pb en el segundo trimestre de 2026) más margen del Capital Ordinario (80 pb en 2026), más 1,15% en Financiamiento Especial para el Desarrollo; ACT/360; semestral; sin fecha de fijación.
- **BIRF:** SOFR más margen variable, semestre, tasa no menor a 0%. **No hay base de días ni día de fijación en ninguna fuente del BIRF** y las Condiciones Generales no dicen si la SOFR es a plazo o compuesta. Los contratos de 2017 o antes dicen LIBOR; no encontré el aviso que los pasó a SOFR.
- **CAF:** CME Term SOFR a 6 meses, fijada 2 días hábiles antes del período; ACT/360; pago el último día hábil de cada semestre. **BCIE:** Term SOFR a 6 meses, 2 días hábiles antes; ACT/360; semestral; margen trimestral. **FONPLATA:** SOFR compuesta con Índice SOFR, bloqueo de 30 días, base 360, semestral.

## Pedido 2: SOFR

**Para Claude:** `tablas/sofr_diaria_ny_fed_2023-01-03_a_2026-10-14.csv` (944 observaciones) y `tablas/sofr_indice_y_promedios_ny_fed_2023-01-03_a_2026-10-15.csv` (945, con el Índice SOFR para componer). **CME Term SOFR a 6 meses no es pública** (licencia de CME); no la incluí ni la aproximé. Para CAF y BCIE esa es la tasa de referencia, así que la resta de la fase 4 queda sin SOFR exacta.

## Pedido 3: revisión

**Para Claude:** sin cambios: Finanzas sigue en II Trimestre 2026, SIGADE al 30-09 no salió, ONCP llega al 31-08, no hay comunicado de A3 Mercados con los montos de la RC 60 (último CE listado: 14715, 2026-10-01).

## Represas Kirchner-Cepernic

**Para Claude:** no hay enmienda ni nota pública con el reemplazo de la LIBOR. Cláusula 35.3: enmienda con el Agente y el Prestatario, con el ajuste que designe el Relevant Nominating Body si existe; no nombra SOFR ni cifra. El 0,42826% para 6 meses es el ajuste de ISDA/ARRC sobre CME Term SOFR a 6 meses (documentos del 2021-03-05 y 2023-03-15); no hay documento que diga que el crédito lo adoptó. ACT/360, períodos de 6 meses.

## Preguntas

1. Para CAF y BCIE (Term SOFR a 6 meses, no pública), ¿querés que use un proxy declarado (por ejemplo, el promedio de SOFR a 180 días del NY Fed, que no es Term SOFR) o que la fase 4 deje esos préstamos con la tasa total de SIGADE sin separar la SOFR?
2. ¿Sigo con la búsqueda de los avisos del BIRF y del BID (costo de fondeo trimestral) en un lote R?
