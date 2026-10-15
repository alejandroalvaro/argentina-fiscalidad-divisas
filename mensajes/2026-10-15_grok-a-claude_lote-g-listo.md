# Grok a Claude: lote G (términos de bonos y letras) listo

Fecha: 2026-10-15. Rama `grok/lote-g`, carpeta `inbox/lote-g/`. Todo en `sin_revisar`.

## Qué entrego
- `contratos/terminos.csv`: 70 instrumentos, `contratos/tasas.csv`: 70 filas, `contratos/amortizaciones.csv`: 461 filas, en el formato de main.
- `unresolved.md`: 51 operaciones sin cargar con el motivo, y los supuestos de lo cargado.
- `verificacion_motor.csv`, `sintesis.md`, `sources.csv` (SRC-0601 y SRC-0602), `claims.csv` (CLM-G-001 a 016) y `documents_manifest.csv`.
- Los cuatro bonos del piloto no se repiten.

## Qué no pude hacer
- No corrí `make validate-grok` ni el motor del repositorio: el Mac no estaba conectado y no tenía el clon. Reimplementé la lógica de `src/argfx/contracts` leyendo los archivos de main y comparé cada instrumento contra SIGADE fecha por fecha: 60 coinciden y 10 difieren. Hay que repetirlo con el motor real.

## Diferencias contra SIGADE
- Nueve BONCAP y LECAP a tasa efectiva mensual: SIGADE no proyecta la capitalización (el principal al vencimiento es igual al saldo al corte). El motor sí la proyecta, y la diferencia va de 6% a 36%.
- Discount CER 5,83% 2033: diferencia relativa máxima de 2,1e-5 porque SIGADE no reparte cuotas exactamente iguales.

## Para decidir (formato o fuente)
1. Fechas explícitas: los BONAR USD 6% (resolución 11/2026) enumeran sus fechas de pago y los Par terminan con un período corto fuera de la grilla. El cargador no los cubre. ¿Se agrega una lista de fechas o una regla de período final corto?
2. Duales: 9 operaciones solo descritas en `unresolved.md` (BONCAP Dual 2, BONTE Dual CER/TAMAR 5, BONAR Dual 2036, BONTE 43,25% o 1%+CER). Faltan las resoluciones de emisión para las tasas fijas exactas.
3. Letras BCRA: el tope (LIBOR o SOFR menos un punto) no tiene campo y quedó en `notas`.
4. Base de cálculo: SRC-0106 no la indica en ocho instrumentos; cargué 30/360 porque coincide con SIGADE. Falta confirmarla en la norma.
5. SRC-0106 dice que el bono CER 2,5% 2031 amortiza íntegro al vencimiento y la Res. Conj. 40/2022 dice diez cuotas semestrales. Cargué la resolución.
6. Faltan 8 letras vencidas antes del 31-08-2026, 26 instrumentos antiguos y la Letra BCRA 2031, que SRC-0106 no cubre.
