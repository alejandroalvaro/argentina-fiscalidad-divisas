# Lote G: términos contractuales de bonos y letras (sin_revisar)

## Qué hay
- `contratos/terminos.csv`: 70 instrumentos (una fila por operación SIGADE, con su `instrument_id`).
- `contratos/tasas.csv`: 70 filas de tasas fijas por tramo (31 instrumentos de tasa fija o por período).
- `contratos/amortizaciones.csv`: 461 filas de fracciones del nominal original (los instrumentos sin filas amortizan íntegro al vencimiento).
- `verificacion_motor.csv`: comparación fecha por fecha contra el perfil SIGADE (60 coinciden, 10 con diferencias explicadas).
- `unresolved.md`: 51 operaciones sin cargar (9 duales, 4 Par, 2 BONAR USD, 1 BONAR consenso fiscal, 1 Letra BCRA 2031, 8 vencidas antes del 31-08-2026, 26 antiguas) y los supuestos incluidos.
- Las cuatro operaciones del piloto (INS-C-0398, 0404, 0399, 0405) ya están en main y no se repiten.

## Composición de lo cargado
| Grupo | Cantidad |
|---|---|
| Globales y Bonares step up (A.1), sin los cuatro del piloto | 13 |
| Cero cupón CER (BONCER 0%, LECER) | 16 |
| Cero cupón dólar linked (LELINK, BONTE DLK) | 5 |
| Letra USD sin interés (OL) | 1 |
| BONCER, Discount y Cuasipar con cupón fijo (CER) | 5 |
| Discount yen y BONTE fijos en pesos, BONTE USD 6,5% | 4 |
| BONCAP y LECAP a tasa efectiva mensual capitalizable | 9 |
| Flotantes: BONCAP TAMAR (5), BONTE BADLAR (4), Letras BCRA (7), Bocon PR17 (1) | 17 |

## Hallazgos sobre las fuentes (ver `claims.csv` y `unresolved.md`)
- SRC-0106 tiene un error en el Global USD 2035 (amortización del 2030 y tramo de tasa omitido) y un error de fecha en el EUR 2041 ("09-97-2021").
- SRC-0106 dice que el bono CER 2,5% 2031 amortiza íntegro al vencimiento; la Res. Conj. 40/2022 y SIGADE dicen diez cuotas semestrales. Se cargó la resolución.
- SIGADE no proyecta la capitalización de BONCAP y LECAP: el principal al vencimiento es igual al saldo al corte.
- Los BONAR USD 6% enumeran sus fechas de pago en la resolución, y los Par tienen un período final fuera de la grilla semestral. El cargador actual no cubre ninguno de los dos casos.

## Qué no se hizo
- No se corrió `make validate-grok` ni el motor del repositorio (Mac sin conexión, sin clon). La verificación usó una reimplementación local de la lógica de `src/argfx/contracts`.
- No se descargaron las resoluciones de emisión de los instrumentos duales ni de los vencidos.

## Adenda 2026-10-15: capitalización de BONCAP y LECAP
- `tablas/capitalizacion_*.csv`, `tablas/escenario_interes_en_caja.csv`, `tablas/ilustracion_posponer_interes.csv`, `tablas/resultado_fiscal_publicado.csv`: método y cifras en `mensajes/2026-10-15_grok-a-claude_capitalizacion-boncap-lecap.md`.
- Fuentes nuevas SRC-0603 a SRC-0614 (resoluciones y publicaciones fiscales); claims CLM-G-017 a CLM-G-034.
- `contratos/fechas_explicitas.csv` y `contratos/topes_propuesta.csv` son propuestas de formato.
