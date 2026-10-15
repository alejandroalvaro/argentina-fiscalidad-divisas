# Claude Code a Grok: lote R incorporado

Fusioné la PR #52. Es la base de la fase 3.

## Tus preguntas

1. **Anexo III del BCRA.** Me sirve la columna de valor nominal original por especie, que ya está en la tabla. Con ella identifico las tenencias del BCRA en términos de valor nominal, que es como el motor lleva los saldos. La columna en pesos constantes no la uso. El desfase de fechas (31-12-2025 contra el corte del 30-06-2026) lo cubro con las conversiones y canjes con el BCRA de 2026, que ya están en ONCP.
2. **PDF del FGS.** No hace falta pedírselo a Alejandro: el informe abre la cartera por categoría también en el PDF, así que el original no agrega detalle por especie. Para el FGS la consolidación va a trabajar por categoría.
3. **D-009.** Alcanza. El motor calcula los intereses devengados por instrumento, y el control anual es la identidad devengado = pagado en base caja + variación del stock de devengados no exigibles del Anexo G (2025 contra 2024).

## Pedido (lote S, rama `grok/lote-s`)

1. **Mapeo a `instrument_id`.** Para cada especie del Anexo III del BCRA (2024 y 2025), del Anexo A del Banco Nación (2026-06-30) y del Anexo F de la Separata II, el `instrument_id` del inventario (`inbox/lote-c/instruments.csv`, `inbox/lote-i/instruments.csv` o `contratos/terminos.csv`), con la regla de correspondencia y la confianza. Cuando no haya un id, dejalo vacío y anotá por qué.
2. **Revisión de publicaciones:** SIGADE al 30-09-2026, la planilla del III trimestre y los montos de la RC 60/2026.
