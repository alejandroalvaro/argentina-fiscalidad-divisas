# Grok a Claude: lote S (rama `grok/lote-s`, sin_revisar)

Alejandro aprobó el lote S. Entrega en `inbox/lote-s/`: fuentes SRC-1191 a SRC-1198 (solo la revisión), claims CLM-S-001 a CLM-S-007, tres tablas de mapeo a `instrument_id`, la tabla de revisión, `sintesis.md` y `unresolved.md`. Sin PDFs, imágenes, html ni json en la rama; los originales de la revisión están en la caja con sha256 en `documents_manifest.csv`. Todo `sin_revisar`.

**Para Claude:**
- `tablas/mapeo_anexo_iii_bcra_a_instrument_id.csv`: 47 especies distintas de los EECC 2024 y 2025, con el valor nominal original de cada columna; 23 con id (12 alta, 11 media), 24 sin id con motivo. `tablas/mapeo_anexo_a_banco_nacion_a_instrument_id.csv`: 10 de 10 con id (6 alta, 2 media, 2 baja). `tablas/mapeo_anexo_f_separata_ii_a_instrument_id.csv`: 7 de 14 letras (2025) y 7 de 15 (2024) con id.
- Cada fila trae la regla de match, la confianza, el vencimiento del inventario (de terminos.csv o del nombre), el archivo del inventario y, en las letras del BCRA, un control del valor nominal contra el saldo del inventario.
- El inventario es el saldo en circulación al 2026-06-30; los anexos son tenencias al cierre contable. No son comparables salvo en las letras intransferibles.
- Seis letras del BCRA presentes al 2025-12-31 no están en el inventario al 2026-06-30 (Ley 27.541/19, Res. 28/20, Res. 3/21 y 11/21, Decreto 622/21, Decreto 280/24, Decreto 1104/24). La LETRA/U$S/BCRA/20-04-2032 (INS-C-0444) bajó de 7.809.225 miles de USD a 4.413.717.781,5 USD. No sé la causa.
- Confianza baja (revisar): BNA Letra TAMAR 31.08.2028 contra INS-C-0371, y Bonos Rep. Arg. Step Up 35 contra INS-C-0405 (alternativa INS-C-0399).
- **Revisión:** sin cambios; Finanzas llega al II trimestre, SIGADE al 30-09 no salió y no hay montos de la RC 60/2026 (último CE en ADEBA: 14715).

## Preguntas

- Para las especies vencidas, ¿querés que reconstruya el inventario SIGADE de 2024-12-31 y 2025-12-31 desde las planillas trimestrales de Finanzas para darles id?
- ¿Buscamos el motivo de la baja de las seis letras del BCRA en 2026 (conversiones y canjes de ONCP)?
