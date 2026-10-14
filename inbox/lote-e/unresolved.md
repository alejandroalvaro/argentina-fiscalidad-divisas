# Lote E: pendientes y contradicciones (sin_revisar)

## Contradicciones señaladas, no resueltas
- Deuda bruta del gobierno general: el BCB publica dos series vigentes con metodologías distintas (SGS 4537, "metodologia utilizada até 2007", y SGS 13762, "a partir de 2008"). En 2026-08 difieren en unos 11,7 puntos del PIB.
- El WEO del FMI para 2025 (93,3 % del PIB) coincide con SGS 4537 y no con SGS 13762. La diferencia de perímetro (por ejemplo, el tratamiento de los títulos en cartera del BCB) no fue verificada en documentos metodológicos.
- SGS 28192 a 28202 ("Saldo de dívida externa"): el título distingue títulos emitidos en mercado externo y doméstico. No se verificó si el criterio es residencia, moneda o mercado de emisión. Además, 28199 supera a la suma de 28201 y 28202 (la diferencia podría ser préstamos, SGS 28200, que no se descargó).

## Faltantes
- Unidades: la página de metadatos del SGS respondió "System unavailable" durante toda la sesión. Las unidades de las series de balance de pagos, PII, reservas y saldos de deuda quedan vacías en la tabla. Solo se completó "% PIB" cuando figura en el título.
- PII: no se encontró en el catálogo el código del Activo total ni de la posición neta. Solo están el Passivo total (24040) y tres componentes del activo, así que la posición neta no se calculó.
- Deuda por moneda en sentido estricto (DPF por indexador, con la porción cambial): no se derivó. El CSV del Tesouro trae el título por código (LFT, NTN-B, etc.) y se podría clasificar, pero no se hizo para no inferir el indexador sin la tabla oficial. El Relatório Mensal da Dívida (RMD) no se descargó.
- Reservas diarias: solo hay 10 años (desde 2016-10-17), por el límite de la API SGS para series diarias.
- Reservas netas de Brasil (brutas menos pasivos, swaps cambiales del BCB, operaciones de recompra en USD): no hay serie descargada.
- La búsqueda CKAN del BCB devolvió XML/HTML de forma intermitente y hubo que reintentar.
