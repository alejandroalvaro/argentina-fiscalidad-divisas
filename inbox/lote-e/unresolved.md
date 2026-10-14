# Lote E: pendientes y contradicciones (sin_revisar)

## Contradicciones señaladas, no resueltas
- Deuda bruta del gobierno general: el BCB publica dos series vigentes con metodologías distintas (SGS 4537, "metodologia utilizada até 2007", y SGS 13762, "a partir de 2008"). En 2026-08 difieren en unos 11,7 puntos del PIB.
- El WEO del FMI para 2025 (93,3 % del PIB) coincide con SGS 4537 y no con SGS 13762. La diferencia de perímetro (por ejemplo, el tratamiento de los títulos en cartera del BCB) no fue verificada en documentos metodológicos.
- SGS 28192 a 28202 ("Saldo de dívida externa"): el título distingue títulos emitidos en mercado externo y doméstico. No se verificó si el criterio es residencia, moneda o mercado de emisión. Además, 28199 supera a la suma de 28201 y 28202 (la diferencia podría ser préstamos, SGS 28200, que no se descargó).

## Faltantes
- Unidades: **resuelto.** La página de metadatos del SGS siguió sin responder, pero el catálogo de datos abiertos del BCB (CKAN, campo `unidade_medida`, SRC-0425) informa la unidad de las 19 series: millones de USD (balanza de pagos, PII, reservas), millones de reales (saldos de deuda externa 28192 a 28202) y porcentaje (series en % del PIB). La columna `unidad` ya no tiene vacíos.
- PII: no se encontró en el catálogo el código del Activo total ni de la posición neta. Solo están el Passivo total (24040) y tres componentes del activo, así que la posición neta no se calculó.
- Clasificación de la DPF por indexador (`tablas/mapeo_indexador_dpf.csv` y `tablas/dpf_por_indexador_derivado.csv`): DERIVADA POR GROK, NO OFICIAL. Debe cotejarse con el Relatório Mensal da Dívida (RMD) del Tesouro, que no fue descargado. Puntos a revisar:
  - Deuda externa asignada en bloque a cambio según los metadatos (conversión desde moneda extranjera). Algunos préstamos podrían tener otra moneda o indexador.
  - Global BRL (denominado en reales), TDA, CVS, títulos de securitización (HCF*, HSTN), ECTN, AINSS y otros quedan sin_clasificar (0,30% del stock en 2026-07).
  - LFT-TD asignada a Selic solo por prefijo.
  - NTN-C (IGP-M) agrupada en ipca_precos.
  - Las valoraciones del CSV usan la TIR media de emisión (metadatos), por lo que las participaciones pueden diferir de las del RMD.
- Reservas diarias: solo hay 10 años (desde 2016-10-17), por el límite de la API SGS para series diarias.
- Reservas netas de Brasil (brutas menos pasivos, swaps cambiales del BCB, operaciones de recompra en USD): no hay serie descargada.
- La búsqueda CKAN del BCB devolvió XML/HTML de forma intermitente y hubo que reintentar.

## Formato y entrega (ajustes posteriores a la validación de Claude Code)

- Las fechas anuales (WEO) y mensuales (DPF) pasaron a formato completo con el primer día del período (`2000-01-01`, `2017-09-01`).
- `mapeo_indexador_dpf.csv`: las 23 filas sin `source_id` son los prefijos sin regla documentada (`sin_clasificar`). Se agregó la columna `nota_fuente`, que lo explica.
- SRC-0424 (Decreto 3.859/2001) se sube a `inbox/lote-e/documentos/decreto_3859_2001.htm`, porque planalto.gov.br cierra la conexión desde el entorno de Claude Code. Desde aquí sí se descargó.
