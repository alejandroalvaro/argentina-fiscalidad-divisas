# Lote K: síntesis

Fecha de acceso de todas las fuentes: 2026-10-15. Todo `sin_revisar`. Rama `grok/lote-k`. Fuentes nuevas: SRC-0945 a SRC-0982 (colocaciones de ONCP 2023, 2025 y 2026, tres comunicados de Finanzas, series CER y A 3500 del BCRA, RC 53 y 60/2026, cinco informes de OPC, la página de datos trimestrales, RC 50 y 54/2023 y 19 índices del Boletín Oficial). La estructura financiera de ONCP es SRC-0106, ya en main.

- **TMF27 y TMG27:** no encontré canje, conversión ni rescate en abril a agosto de 2026. La circulación previa implícita de TMF27 el 2026-09-11 es 3.906.522 millones, 485.000 menos que los 4.391.522 emitidos; en TMG27 el saldo de SIGADE queda 336.831 millones por debajo del VNO emitido (1.950.739). No cargué filas (unresolved.md, punto 1).
- **BONAR Dual 2036 (INS-C-0357):** una fila en `terminos.csv` (rama USD, 3%, fecha de emisión 2023-10-20, cupones 29 de marzo y septiembre), una en `tasas.csv` y una en `duales.csv` (rama CER 3%, `factor_saldo` 2,5704835949 sobre la base de la norma). Los seis tramos de ONCP, convertidos con el A 3500 de tres días hábiles antes de la liquidación, dan USD 640.874.451, igual que SIGADE. No encontré el texto de la RC 53/2023 (unresolved.md, punto 2).
- **TTD26:** cadena publicada 3.500.632 más 5.700.388 menos 4.576.957 da 4.624.064 millones, 0,11% sobre el derivado de 4.618.994 (`tablas/ttd26_vno_publicado.csv`). No hay total publicado.
- **Conversiones con el BCRA:** RC 39 (USD 1.000 y USD 1.000 millones de LELINK a cambio de 2.755 miles de millones de TZXD6), RC 49 (USD 501,792 millones) y RC 51 (1.013.350 millones de T30J7 contra 1.265 miles de millones de S31G6). RC 53 y 60 solo tienen topes. SIGADE al 2026-09-30 no está publicado.
- **Operaciones:** `operaciones.csv` vacío; no hay operaciones nuevas sobre estos instrumentos después del corte en las fuentes revisadas.
- **Límites:** ver `unresolved.md`.
- **Rezago CER (punto 5):** `tablas/cer_rezago_verificacion.csv`. Verificados 11 de 17 (INS-C-0372, 0374, 0375, 0376, 0377, 0378, 0381, 0382, 0383, 0624, 0625): saldo SIGADE por CER del día de emisión coincide con el VNO publicado (diferencia relativa menor a 2 por millón). Sin verificar: INS-C-0373, 0379, 0380, 0386, 0387 y 0388 (ver `unresolved.md`, punto 6).

