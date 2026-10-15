# Lote O: síntesis (sin_revisar)

Rama `grok/lote-o`. Fuentes SRC-1048 a SRC-1107 (60); claims CLM-O-001 a CLM-O-057; tablas en `tablas/`; huecos en `unresolved.md`. Los tres `contratos/*.csv` van solo con encabezado.

## Resultado

1. **BADLAR en los BONTE:** las tres normas fijan promedio simple de la BADLAR de bancos privados con diez días hábiles de rezago en los dos extremos (2030: fin "exclusive"; 2027 y 2031: sin esa palabra). Con 21 avisos oficiales de pago (TB27P, TB31P) la tasa del aviso coincide con el promedio simple de la serie BCRA variable 7 desde el décimo día hábil previo al inicio del período hasta el décimo día hábil previo al fin, ambos inclusive, con diferencia de punto flotante. La base de días del cupón es 365 o 366 según el año en que empieza el período del aviso (`terminos.csv` tiene ACT/365 para los tres). Sin aviso para el BONTE 2030, y su norma no fija los días de pago de los intereses.
2. **A 3500 en pagos ligados al dólar:** tercer día hábil previo a la fecha de pago en todas las familias (LELINK, BONTE DLK, TMVE8 y pata dólar del BONAR Dual 2036), por norma; los avisos de D30S6 y D31G6 lo confirman y la cifra del cupón es exactamente la A 3500 de ese día.
3. **RC 53 y 60/2026 y SIGADE al 2026-09-30:** sin planilla oficial nueva; el monitor de la OPC llega a la RC 59 (la RC 60 no figura). Los comunicados de MAE 14.664, 14.699 y 14.715 dan altas y bajas de septiembre (topes de la RC 53 coinciden con el 14.664).
4. **Copia pública de los avisos de Discount, Par y Cuasipar:** no hay copia de las notas en BYMA, Caja de Valores ni Boletín de la Bolsa; los comunicados de Caja de Valores 12856 (2026-07-01) y 12500 (2025-08-26) traen los pagos ejecutados y coinciden con los avisos (por 100 de VN).

## Cómo leer las cifras

Tasas en porcentaje nominal anual. "Día hábil" es el día con publicación de la serie BCRA correspondiente (proxy; sin calendario de feriados). Los originales (PDF, HTML y JSON) están en `/workspace/lote_O` con sha256 en `documents_manifest.csv`; no van en la rama.
