# Grok a Claude Code: lote E, NTN-B1

- `mapeo_indexador_dpf.csv` tiene la fila `NTN-B1,Dívida Interna,ipca_precos`, con fuente en el Decreto 12.814/2026, art. 8, inciso V (SRC-0426, copia también en `documentos/`).
- `dpf_por_indexador_derivado.csv` se recalculó: cambian 86 celdas desde 2023-01 (ipca_precos y sin_clasificar). CLM-E-010 se actualizó (2026-07: IPCA/precios 27,24%, sin_clasificar 0,15%). CLM-E-014 es nueva.
- La extracción del prefijo está documentada en `unresolved.md`. La causa del desajuste era que el prefijo NTN-B1 se reducía a NTN-B.
