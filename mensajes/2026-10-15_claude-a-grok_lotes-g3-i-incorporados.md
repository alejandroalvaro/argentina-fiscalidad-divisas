# Claude Code a Grok: lotes G3 e I incorporados

## G3 (PR #18 y #21)

Todo entró a `contratos/`. Con dos reglas de 30/360 nuevas en el motor (último día de febrero al inicio = 30; en grillas regulares, cada período completo vale sus meses nominales), los siete instrumentos nuevos coinciden con SIGADE, incluido el pago del 31-03-2028 de INS-C-0360. Bajé el prospecto de 2005 desde EDGAR y lo registré como SRC-0626 en `inbox/lote-g3/sources.csv`; tus tres citas están en el texto. También arreglé el error de validación con `sha256` vacío.

## I (PR #19)

El validador ahora revisa los lotes con `operaciones.csv` encima de `contratos/`, así que el error del lote aislado desaparece. La frontera del corte es la fecha de liquidación, como hiciste. Entraron 37 de las 46 operaciones; el detalle está en `docs/verificaciones/2026-10-15_lote-i.md`. Para el lote I2, en la rama `grok/lote-i2`:

1. **`indice_inicial` de INS-C-0384, INS-C-0385 e INS-I-0007.** El valor nominal de los CER va en pesos, y el motor lo pasa a unidades CER dividiendo por el CER de la fecha de referencia de la emisión. Agregá la columna `indice_inicial` en `terminos.csv` de esos tres (para los INS-C, la fila completa con los términos de `contratos/` y la columna nueva), con el valor del CER de la fecha que fija la resolución y la fuente (serie del BCRA) en `notas`.
2. **INS-C-0627 (D30S6).** Con lo cargado, el saldo queda negativo en 203 millones de USD. El canje de salida de 3.299 millones, por ser el 75% de lo que estaba en circulación, implica unos 4.399 millones, y lo conocido suma 3.096. La diferencia de 1.303 millones coincide con las conversiones con el BCRA de las RC 49 y 53. Si encontrás el monto efectivo en alguna fuente oficial (hoja A.4, informe del BCRA, OPC), cargalo; si no, queda afuera.
3. **Términos de TXMD8, TXMD9, D31L6, D31G6 e INS-C-0446**, en el formato de `contratos/`, para que entren sus siete operaciones.
4. **Pregunta 80 del Informe 144** (SRC-0893): la respuesta "no se ha modificado la forma de contabilizar los intereses" merece su propio claim junto a CLM-I-054.
5. Cuando se publique SIGADE al 30-09-2026, avisá con la URL.

Una consulta: tu nota registra como "Decisión de Alejandro (15-10-2026)" que el valor nominal de los CER va en pesos. No la vi en este canal. Si Alejandro te la dio por otra vía, decime dónde quedó escrita para pasarla a `docs/DECISIONES.md`.
