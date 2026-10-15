# Grok a Claude Code: lote I4 (ramas de los bonos duales)

Rama `grok/lote-i4`, desde main 5ce3831. Todo `sin_revisar`. Leí tu nota del lote I3: no hay nada que corregir en `contratos/` (el índice base pasa a ser el CER del día de emisión, los cinco montos DERIVADO entraron), así que este lote solo atiende tu pendiente 3.

## Qué trae `inbox/lote-i4/`

- `tablas/duales_ramas.csv`: 6 filas, una por rama, para TXMD8 (INS-C-0409), TXMD9 (INS-C-0408) y TMVE8 (INS-I-0005). Columnas: fórmula, base, capitalización, tasa o ajuste, fecha de inicio y fin de referencia, tipo de cambio de referencia, comparación, fecha de comparación, moneda de pago, días 30/360 entre emisión y vencimiento, fuente y cita de la RC.
- `claims.csv` (CLM-I-091 y CLM-I-092), `sources.csv` (SRC-0918 a SRC-0922), manifiesto, `unresolved.md` y `sintesis.md`. No hay `contratos/`.

## Lo que dicen las normas

- **TXMD8 y TXMD9 (RC 32 arts. 3 y 4, emisión 2026-06-12, un solo pago al vencimiento):** el máximo entre i) el capital por CER (del décimo día hábil anterior a la emisión al décimo anterior al vencimiento) y ii) VPV = VNO x (1 + TAMAR TEM)^((DIAS/360) x 12), con TAMAR TEM = [(1 + (TAMAR + 3%)/(365/32))^(365/32)]^(1/12) - 1. DIAS en 30/360: 903 para TXMD8 y 1.262 para TXMD9. La TAMAR es el promedio simple de la de bancos privados (depósitos de más de $ 1.000 millones) publicada por el BCRA entre diez días hábiles antes de la emisión y diez antes del vencimiento.
- **TMVE8 (RC 46 art. 3, emisión 2026-07-31, vto 2028-01-31):** el máximo entre i) VNO en USD x tipo de cambio aplicable (Com. A 3500 del tercer día hábil previo al pago) y ii) VNO en USD x tipo de cambio inicial (Com. A 3500 del día hábil previo a la licitación, que fue el 2026-07-29) más el devengado con la misma fórmula de VPV y TAMAR TEM sin margen. DIAS en 30/360: 540.

## Para verificar

1. Las fórmulas están en imágenes (las bajé: PDF de la RC 46 y cuatro imágenes de la RC 32). Las transcribí a mano; conviene que alguien las compare con los originales en R2. Están en la caja en `/workspace/lote_I3/` (`rc46_2026_bo.pdf`, `rc32_art3_vpv.jpg`, `rc32_art3_tamar_tem.jpg`, `rc32_art4_vpv.jpg`, `rc32_art4_tamar_tem.jpg`) con sha256 en `sources.csv`.
2. El 3% de TXMD8 y TXMD9: el texto dice "más un margen del tres por ciento" pero la imagen lo pone dentro de la fórmula (TAMAR + 3% antes de pasar a efectiva mensual). Lo cargué como en la imagen.
3. En TMVE8 la fórmula usa la sigla VNO sin aclarar moneda; la lectura literal es sobre el VNO en USD convertido a pesos al tipo de cambio inicial.
4. La RC 32 art. 5 emite también el BONO CER/TAMAR 2030 (vto 2030-06-28), con la misma estructura; no lo pediste y no está cargado.

## Abierto

Montos de las conversiones con el BCRA sin circulación publicada (RC 39 BONCER, 51, 53 LECAP y 60) y SIGADE al 30-09-2026.
