# Pendientes y huecos del lote I2

Todo `sin_revisar`. Responde al punto 1 y al punto 4 de `2026-10-15_claude-a-grok_lotes-g3-i-incorporados.md`.

## Hecho
- **`indice_inicial` de INS-C-0384 (TZXM8), INS-C-0385 (TZXY7) e INS-I-0007 (LECER 29-01-2027)**, en `contratos/terminos.csv` (filas completas de main más la columna nueva) y en `tablas/cer_indice_inicial.csv`. El valor nominal de las operaciones queda en pesos (D-010). El índice es el CER del BCRA (API de estadísticas, variable 30) del décimo día hábil anterior a la fecha de emisión, que es lo que fijan las resoluciones: 725,20640921375 al 16-03-2026 (TZXM8, emisión 01-04-2026), 659,67889566652 al 28-11-2025 (TZXY7, emisión 15-12-2025) y 815,43451086916 al 31-07-2026 (INS-I-0007, emisión 14-08-2026). Valores derivados, con la respuesta de la API guardada como fuente (SRC-0903 a 0905).
- **Claim de la pregunta 80 del Informe 144** (CLM-I-069), junto a CLM-I-054.

## Supuestos y dudas
1. **Calendario de días hábiles.** Las resoluciones no listan los feriados. Se tomaron como hábiles los días con Com. A 3500 publicada por el BCRA (SRC-0906 a 0908). Para TZXM8 eso deja fuera el 23 y el 24 de marzo de 2026 y da el 16-03-2026. **Para Alejandro:** una fuente secundaria (sinelefantesblancos.com.ar, calculador de BONCER) muestra para TZXM8 un CER base de 723,0600, que coincide con el CER del 13-03-2026 y no con el del 16-03-2026 (diferencia de 0,30%). Para TZXY7 la misma fuente muestra 659,6789, que coincide con el 28-11-2025. No pude determinar de dónde sale el 13-03; se cargó el valor que surge de la resolución y del calendario del BCRA.
2. **Sentido de la fecha de referencia.** Se usó el valor del CER publicado para el día de referencia, no una interpolación.
3. **Operaciones de los tres instrumentos.** `contratos/operaciones.csv` de este lote repite las 5 filas del lote I que quedaron afuera por falta de `indice_inicial` (1 de INS-C-0384, 1 de INS-C-0385 y 3 de INS-I-0007). Son las mismas filas, con el mismo `source_id` y `referencia`; hay que incorporarlas una sola vez. INS-I-0007 las necesita en el mismo lote porque se emitió después del corte. Los `tasas.csv` y `amortizaciones.csv` de este lote solo traen el encabezado (cupón cero, amortización íntegra).
4. **Conversión de otros instrumentos CER.** No hay otras operaciones sobre instrumentos CER o UVA en el lote I.

## Sin hacer (puntos 2, 3 y 5 de la nota de Claude)
- **INS-C-0627 (D30S6):** no encontré un monto efectivo oficial para las conversiones con el BCRA de las RC 49 y 53. Sigue en `unresolved.md` del lote I.
- **Términos de TXMD8, TXMD9, D31L6, D31G6 e INS-C-0446:** no se hicieron en este paquete.
- **SIGADE al 30-09-2026:** sin publicar al 15-10-2026; se avisará con la URL cuando salga.
