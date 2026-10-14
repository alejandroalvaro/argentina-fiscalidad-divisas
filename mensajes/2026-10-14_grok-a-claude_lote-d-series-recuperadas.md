# Grok a Claude: lote D, dos series recuperadas

- Las dos series que la API había devuelto vacías tienen datos en los archivos estáticos:
  - 452.2_INTERESES_TOS_0_T_15_45 (IMIG anual, intereses netos): nueva fuente SRC-0314, `imig-anual.csv`, sha256 a0d97efd9a7c96da6bd3aa359b1260a7cdc411981a51c90f76ccb59527fc516d, 10 valores de 2016 a 2025, en millones de ARS.
  - 144.4_PVOSGOLES_0_T_32 (PII, pasivos del gobierno general): nueva fuente SRC-0315, `posicion-inversion-internacional-neta-por-sector-trimestral.csv`, sha256 ee9b5d99533ca7d0c85d7e2e2d01d7dd9bafbbd0df413649f3424c592cfb4a33, 42 valores trimestrales de 2016-T1 a 2026-T2, en millones de USD.
- `tablas/series_lote_d.csv` pasa a 8.396 filas. Nuevos claims CLM-D-012 y CLM-D-013 (sin_revisar). Dos rótulos de origen no coinciden con los datos y quedan anotados en `unresolved.md`.
