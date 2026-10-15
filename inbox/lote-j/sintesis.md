# Lote J: pendientes de duales

Fecha de acceso de todas las fuentes: 2026-10-15. Todo `sin_revisar`. Rama `grok/lote-j`.

- **BONTE duales CER/TAMAR (INS-C-0410, 0411, 0412):** identificados con la RC 32 art. 5 (BONO CER/TAMAR 2030), la RC 23 art. 3 (TXMJ9, ampliado por la RC 25 art. 5) y la RC 25 art. 1 (vencimiento 2028-06-30). Tres filas en `contratos/terminos.csv` (CER cupón cero, `indice_inicial` = CER del día de emisión: 788,9793474221, 758,11795391868 y 770,89823475195) y tres en `contratos/duales.csv` (TAMAR + 3%, mismo formato que TXMD8). Las unidades de SIGADE por el CER del día de emisión reproducen los VNO adjudicados (3.857.824, 4.095.802 y 2.434.341 millones).
- **TTD26 (INS-C-0362):** términos de la RC 4/2025 art. 1 punto IV. Una fila en `terminos.csv` (rama fija 2,14% efectiva mensual, `tasas.csv`) y una en `duales.csv` (rama TAMAR sin margen). Falta el VNO original; `factor_saldo` y `saldo_es_valor_nominal` quedan provisorios (unresolved.md, punto 1).
- **BONAR Dual 2036 (INS-C-0357):** solo hallé el anexo III del DNU 164/2023, sin fechas; no cargué filas (unresolved.md, punto 2).
- **VNO de los cinco BONCAP TAMAR al 2026-06-30** (`tablas/vno_boncap_tamar_2026-06-30.csv`, en millones): TML27 2.425.482, TMG27 1.950.739, TMF28 9.984.903 (derivado), TMF27 4.391.522, TMG28 4.789.359. Los saldos de SIGADE de TMG27 (razón 0,827) y TMF27 (0,993) quedan por debajo del VNO, lo que la capitalización no explica.
- **Operaciones:** ninguna nueva; las colocaciones anteriores al corte están en el saldo de SIGADE y no hay posteriores en las páginas revisadas.
- **Fuentes nuevas:** SRC-0924 a SRC-0943 (RC 4/2025 en el Boletín Oficial, DNU 164/2023, RC 23 y 25/2026 con sus imágenes, imágenes de la RC 32, series CER y A3500 del BCRA y siete comunicados de Finanzas).
- **Límites:** ver `unresolved.md`.
