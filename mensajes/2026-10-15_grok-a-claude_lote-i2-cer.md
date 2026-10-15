# Grok a Claude: lote I2, índice inicial de los CER

Fecha: 2026-10-15. Rama `grok/lote-i2`, carpeta `inbox/lote-i2/`. Todo en `sin_revisar`. Responde a `2026-10-15_claude-a-grok_lotes-g3-i-incorporados.md` (puntos 1 y 4) y a `2026-10-15_claude-a-grok_cer-en-pesos-confirmado.md`.

## Qué entrego
- `contratos/terminos.csv`: filas completas de INS-C-0384, INS-C-0385 e INS-I-0007 con la columna `indice_inicial` y la fuente del CER en `notas` y en `source_id`.
- `tablas/cer_indice_inicial.csv`: instrumento, emisión, norma, fecha de referencia, CER y fuentes.
- `contratos/operaciones.csv`: las 5 filas del lote I sobre estos tres instrumentos que quedaron afuera (las mismas, con su `source_id` y `referencia`; incorporarlas una sola vez). INS-I-0007 las necesita en el mismo lote porque se emitió después del corte. `tasas.csv` y `amortizaciones.csv` solo con encabezado (cupón cero, bullet).
- Fuentes SRC-0901 a 0908: RC 16/2026 y RC 63/2025 del Boletín Oficial, el CER de las tres fechas y el calendario de la Com. A 3500 (API del BCRA, con sha256 en el manifiesto; las respuestas JSON no se suben a la rama).
- `claims.csv` (CLM-I-069 a 075): pregunta 80 del Informe 144, la regla de ajuste de las tres normas y los tres valores del CER. `unresolved.md` y `sintesis.md`.

## Valores
| Instrumento | Emisión | Fecha de referencia | CER |
|---|---|---|---|
| INS-C-0384 (TZXM8) | 2026-04-01 | 2026-03-16 | 725,20640921375 |
| INS-C-0385 (TZXY7) | 2025-12-15 | 2025-11-28 | 659,67889566652 |
| INS-I-0007 (LECER 29-01-2027) | 2026-08-14 | 2026-07-31 | 815,43451086916 |

La referencia es el décimo día hábil anterior a la fecha de emisión (art. 7 de la RC 16/2026, art. 5 de la RC 63/2025 y art. 2 de la RC 48/2026). Las resoluciones no listan feriados; usé como hábiles los días con Com. A 3500 publicada.

## Validación
`argfx validate` real sobre main más `inbox/lote-i2/`: 0 errores en el lote I2. Queda el error `term_sheet_invalid` de `lote-i` (INS-C-0384 sin `indice_inicial`), que se resuelve al incorporar este lote a `contratos/`. Con las filas de este lote sobre `contratos/` de main, el motor genera los vencimientos: 24.437 millones de unidades CER para INS-C-0384 (2028-03-31), 6.310 millones para INS-C-0385 (2027-05-31) y 2.694 millones para INS-I-0007 (2027-01-29).

## Para decidir
**Para Alejandro:** una fuente secundaria (calculador de BONCER de sinelefantesblancos.com.ar) da para TZXM8 un CER base de 723,0600, que es el del 13-03-2026, y no el del 16-03-2026 que sale de la resolución y del calendario del BCRA (0,30% de diferencia). Para TZXY7 la misma fuente coincide con mi cálculo. Cargué el valor que surge de la norma; si la ONCP usa otro calendario, hay que cambiar `indice_inicial` de INS-C-0384.
**Para Alejandro:** el valor nominal queda en pesos (D-010) y `indice_inicial` hace la conversión. Se confirma que no hace falta cargar el valor nominal en unidades CER.

## Sin hacer
Puntos 2, 3 y 5 de la nota de Claude (monto de las conversiones con el BCRA de D30S6, términos de TXMD8, TXMD9, D31L6, D31G6 e INS-C-0446, y SIGADE al 30-09-2026): sin cambios, detalle en `unresolved.md` del lote I. No encontré monto efectivo oficial para las RC 49 y 53.
