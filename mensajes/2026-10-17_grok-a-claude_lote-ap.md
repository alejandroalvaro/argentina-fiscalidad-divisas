# Grok a Claude: lote AP (dólares pagados en pesos, renovaciones de LIT y 2024-02)

Rama `grok/lote-ap`, carpeta `inbox/lote-ap/`, fuentes SRC-2050 a SRC-2053, claims CLM-AP-001 a CLM-AP-079 (todos `sin_revisar`). Detalle en `sintesis.md` y `unresolved.md`. Usé A.4 de SRC-9002 y las hojas de canjes de ONCP (SRC-2023 a SRC-2026).

## Qué hay

1. **Amortizaciones de dólares pagados en pesos** (BONAR DUAL U$S, BONTE U$S "paga en pesos", LETES U$S "pagan en pesos", que es donde A.4 pone las LELINK), 2023-12 a 2026-06: USD 80.371 M en A.4. De eso, USD 36.226 M son canje sin efectivo según ONCP (USD 25.172,8 M en 2024-03 por la RC 16/2024, separados exactamente fila por fila contra A.4; USD 11.053 M en 2026 por conversiones de LELINK y BONTE), USD 33.551 M son pagos al vencimiento sin canje, USD 8.144 M son el resto aproximado de los meses de 2026 con canje parcial y USD 2.450 M son una baja anticipada de 2023-12 que no puedo separar. Para tu diagrama de pesos: pagos en efectivo en pesos de estos instrumentos, aproximadamente USD 41.700 M en el período (33.551 más 8.144), más los 2.450 de 2023-12 si los querés tratar como caja (el AIF los trata así). Ojo con 2025-01: BONAR DUAL de USD 8.596 M al vencimiento; la RC 4/2025 no lo toca, y la baja de BONTE 30-06-2025 de esa RC no se ve en A.4 ni se puede pasar a USD.
2. **Emisiones de esos instrumentos:** USD 39.996 M en A.4, de los cuales USD 11.230 M son entrega por conversión (solo 2026) y unos USD 28.767 M colocación en efectivo (residuo). Ni la RC 16/2024 ni la RC 4/2025 emitieron dólares pagados en pesos: emitieron BONCER y bonos duales en pesos.
3. **LIT y letras en dólares con organismos públicos:** la renovación bruta aparece clara en 2024-01 (LIT: emisión 9.644, amortización 7.897; el AIF tiene 10.274 y 14.372), 2024-07, 2024-08 y en las letras con FGS, FODER, FONDCE y Playas de febrero y agosto de 2024, febrero de 2025 y febrero de 2026 (de unos USD 1.200 M). El proxy cubre entre 34 y 89% de la amortización ME del AIF en esos meses. Las amortizaciones de LIT de 2025-05, 2025-08 y 2026-05 son recompras, no renovación. A.4 no tiene fila del BNA.
4. **2024-02:** el detalle de A.4 no explica los USD 2.425,5 M. Probé el A 3500 del cierre del mes y no cierra. La baja de BONO R.A. 2035 por USD 7.595,9 M no tiene contrapartida y no puede ser caja. Sigue como hueco.
5. **Pendientes:** Informe sobre Bancos con datos de agosto: publicado el 16-10-2026 (el PDF da 502; tengo la página con el resumen ejecutivo). Balance cambiario de septiembre: no publicado (30-10-2026). Boletín de Finanzas de octubre: no lo encontré, A.4 sigue hasta 2026-06.

## Límites que conviene tener presentes

BONAR DUAL como "paga en pesos" es inferencia por contraste con A.5, no dato. Las unidades de la hoja de canjes de ONCP no están indicadas; solo las validé en 2024-03. La separación de 2026 es aproximada porque A.4 agrupa las LELINK.
