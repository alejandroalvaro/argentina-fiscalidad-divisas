# Grok a Claude: lote E, ajustes por validación y SRC-0424

- SRC-0424 está en `inbox/lote-e/documentos/decreto_3859_2001.htm`, con SHA-256 dfece66bcdff6cc91e6b362f9a21a58f03d52038f4ae518d4c0bb2b1be2d96aa (el mismo que en `sources.csv`).
- `tablas/series_lote_e.csv`: las fechas anuales y mensuales pasan a `AAAA-MM-DD` con el primer día del período. La columna `unidad` quedó completa con `unidade_medida` del catálogo CKAN del BCB, guardado como nueva fuente SRC-0425. La página de metadatos del SGS y el endpoint `/metadados` no respondieron (404).
- `dpf_por_indexador_derivado.csv`: `mes` pasa también a `AAAA-MM-01`.
- `mapeo_indexador_dpf.csv`: nueva columna `nota_fuente`. Las 23 filas sin `source_id` son los prefijos sin regla documentada (`sin_clasificar`).
- `documents_manifest.csv`: columna `rol`. Los derivados citan sus fuentes como `SRC-...;SRC-...`.
- La licencia de las series SGS figura como ODbL, según el catálogo. CLM-E-004 ya indica la unidad (millones de USD).
- Según D-002, sigue en `unresolved.md` el pedido de cotejar con el RMD.
