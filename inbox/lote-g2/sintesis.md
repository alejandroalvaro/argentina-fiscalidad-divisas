# Lote G2: BONCAP TAMAR anclados en la emisión (sin_revisar)

## Qué hay
- `contratos/terminos.csv`: cinco filas corregidas (INS-C-0367 a 0371) en el formato actual de `contratos/`.
- `tablas/tamar_tem_implicita.csv`: TEM y TAMAR media implícitas al 30-06-2026 (derivado).
- `sources.csv`: SRC-0615 a 0617 (RC 9/2026, 21/2026 y 36/2026). Las RC 16/2026 y 23/2026 ya están como SRC-0609 y SRC-0606 en el lote G.
- `claims.csv`: CLM-G-035 a 042. `documents_manifest.csv`: originales, diez imágenes de fórmulas y los dos archivos derivados.

## Hallazgos
- Las cinco normas coinciden en las condiciones: emisión a la par, amortización íntegra al vencimiento, interés TAMAR TEM capitalizable mensualmente, base 30/360, y la misma fórmula de conversión en imagen.
- La conversión de la TAMAR anual a TEM sí figura en el texto de la norma: TAMAR TEM = [(1 + (TAMAR + MARGEN)/(365/32))^(365/32)]^(1/12) menos 1.
- La TAMAR de la fórmula es el promedio de todo el plazo del título, por lo que el pago al vencimiento no se puede calcular hoy.
- Con la fórmula, la TEM implícita en los coeficientes de SRC-0103 equivale a una TAMAR media de 22,5% a 27,0% anual hasta el corte (derivado).

## Qué no se hizo
Ver `unresolved.md`.
