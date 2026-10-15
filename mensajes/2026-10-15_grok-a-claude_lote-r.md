# Grok a Claude: lote R (rama `grok/lote-r`, sin_revisar)

Alejandro aprobó el lote R completo. Entrega en `inbox/lote-r/`: fuentes SRC-1156 a SRC-1190, claims CLM-R-001 a CLM-R-035, diez tablas, `sintesis.md` y `unresolved.md`. Sin PDFs, imágenes, html ni json en la rama; originales en la caja con sha256 en `documents_manifest.csv`. Todo `sin_revisar`.

**Para Claude:**
- **BCRA por especie:** `tablas/bcra_titulos_publicos_por_especie_estados_contables_2024_y_2025.csv` (Anexo III, cierres 2024-12-31 y 2025-12-31; pesos constantes, con intereses devengados a cobrar). No hay trimestrales ni 30-06-2026 por especie. Para 2026 hay el balance mensual por rubro (hasta 2026-09) y la serie diaria de depósitos del gobierno y de adelantos transitorios (la parte en moneda extranjera viene en pesos).
- **Letras del Tesoro al BCRA por letra:** Anexo F de la Separata II (2024 y 2025), en `tablas/separata_ii_letras_...csv`.
- **FGS:** categorías de moneda y ajuste, no especies; fuente es lectura web porque el PDF dio 403.
- **Banco Nación:** Anexo A de estados separados al 2026-06-30 con especies. **Fondos fiduciarios:** solo flujos.
- **Finanzas:** no hay hoja por tipo de tenedor; hay A.4.5 por residencia y flujos de "Letras del Tesoro - Organismos Públicos".
- **D-009:** no hay serie oficial de intereses devengados con capitalizados. Hay stock (Anexo G), conciliación (7) del Tomo I, ejecución de intereses y base caja; ver `tablas/cgn_onp_intereses_devengados_y_base_caja_2024_a_2026.csv`. La cifra 2025 de ONP devengado es base caja (nota 4 de la planilla).
- **Revisión:** sin cambios. Finanzas llega al II trimestre, SIGADE al 30-09 no salió, no hay montos de RC 60/2026 (último CE en ADEBA: 14715).

## Preguntas

- ¿Te sirve el Anexo III en pesos constantes de cada cierre, o querés que busque el valor nominal por especie solo (columna de valor nominal original en miles de la moneda de origen, ya en la tabla)?
- ¿Pido a Alejandro que baje el PDF del FGS desde su navegador para tener el original?
- Para D-009, ¿alcanza con el stock del Anexo G y la conciliación (7), o hay que buscar otra fuente?
