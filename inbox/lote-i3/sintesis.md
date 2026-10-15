# Lote I3: términos de cinco instrumentos del lote C y conversiones con el BCRA

Fecha de acceso de todas las fuentes: 2026-10-15. Todo `sin_revisar`.

- **Términos nuevos en `contratos/terminos.csv`** (6 filas): TXMD9 (INS-C-0408) y TXMD8 (INS-C-0409) como CER cupón cero con `indice_inicial` 779,88639312623 (CER del 2026-05-29, décimo día hábil anterior a la emisión del 2026-06-12) y solo la pata CER; D31L6 (INS-C-0629) y D31G6 (INS-C-0630) como letras dólar linked cupón cero pagaderas en pesos; INS-C-0446 como letra intransferible flotante a la tasa de reservas del BCRA con tope SOFR TERM a un año más 0,71513% menos un punto; INS-I-0010 (letra intransferible de 15-09-2031, nueva).
- **Operaciones** (16 filas en `contratos/operaciones.csv`): las 7 excluidas del lote I por falta de términos, las ampliaciones de INS-C-0446 (RC 38 y 43), las dos de INS-I-0010 (RC 54 y 57) y cinco montos de conversiones con el BCRA derivados de circulaciones oficiales (`tablas/derivaciones_conversiones_bcra.csv`, con rangos).
- **Conciliación de INS-C-0446:** 3.878.320 + 35.256.166 + 37.113.987 = 76.248.473 = VNO comprado en la RC 47; el saldo queda en cero el 2026-08-10.
- **Hallazgo:** las unidades de SIGADE de los bonos CER usan el CER del día de emisión (TXMD8 788,979, TZXM8 736,0, TZXY7 668), no el del décimo día hábil anterior de las normas; explica la diferencia de 736 y 668 que había señalado Claude. Decisión pendiente en `unresolved.md`.
- **Límites:** los duales TXMD8 y TXMD9 no tienen modelada la pata TAMAR + 3%; las conversiones de las RC 39 (BONCER), 51, 53 (LECAP) y 60 siguen sin monto en sus patas en pesos y en las entradas de la RC 60.
