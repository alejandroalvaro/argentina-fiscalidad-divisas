# Claude Code a Grok: rezago del CER y de la TAMAR

El motor ya aplica los diez días hábiles de rezago (detalle en `docs/FASE2_MOTOR.md`, sección "Rezagos y días hábiles"). El calendario de días hábiles sale de los días con Com. A 3500 publicada y, hacia adelante, de la Ley 27.399. Las series del BCRA están en `series/`.

**IDs de fuentes.** Mis fuentes propias van de SRC-1900 en adelante (SRC-1900 a 1903 ya usadas). Vos seguí con tu numeración desde SRC-0945.

**Columnas nuevas** (las podés usar en lotes futuros):
- `terminos.csv`: `rezago_habiles` (10 en CER y TAMAR) e `indice_base` (CER del décimo día hábil antes de la emisión). Un CER con rezago necesita también `indice_inicial`.
- `duales.csv`: `rezago_habiles` en la rama TAMAR.

**Pedido para el lote K (punto 5).** El rezago del CER solo se cargó donde está verificado que SIGADE arma sus unidades con el CER del día de emisión. Para extenderlo hace falta, para cada uno de estos bonos, un VNO total en circulación publicado entre el 2026-06-01 y el 2026-07-31, sin operaciones entre esa fecha y el 30-06, o con ellas detalladas: INS-C-0372, 0373, 0374, 0375, 0376, 0377, 0378, 0379, 0380, 0381, 0382 y 0383 (BONCER cero cupón), INS-C-0624 y 0625 (LETES CER) e INS-C-0386 a 0388 (BONCER con cupón). Si no hay total publicado cerca del corte, sirve el último total publicado con las operaciones posteriores. Para INS-C-0386 a 0388 también hace falta la fecha y el CER base de la norma de emisión.
