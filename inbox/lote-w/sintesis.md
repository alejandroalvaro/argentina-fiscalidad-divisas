# Lote W: RC 30/2026, revisión y enlaces del lote V

Todo `sin_revisar`. Hecho el 2026-10-15 (hora de Brasilia). Ids de fuente nuevos: SRC-1263 a SRC-1265.

## 1. RC 30/2026: los USD 1.040 millones siguen sin aparecer

- Las dos operaciones de mayo de 2026 son distintas. La RC 27/2026 es la compra al BCRA en pesos ($ 18,4 billones, de los dividendos del BCRA), liquidada el 2026-05-26. La RC 30/2026 es la compra en dólares (USD 1.040.378.745,11 de valor efectivo) de la letra a 2032, liquidada el 2026-05-29.
- El informe monetario de mayo dice que el desembolso del FMI de USD 1.043 millones se destinó a cancelar Letras Intransferibles. El comunicado del FMI del 21 de mayo habla de unos USD 1.000 millones.
- Las series: el desembolso entra a los depósitos del Tesoro el 2026-05-26 (variable 79 de más USD 1.040,6 millones; saldo de USD 2.388 a 3.425 millones). Entre el 28 de mayo y el 1 de junio la variable 80 suma menos USD 415 millones (más 150, menos 507, menos 58). Ningún día de la ventana 2026-05-26 a 2026-06-05 muestra una salida de USD 1.040 millones. La variable 48 es cero en toda la ventana. El saldo termina en USD 2.931 millones el 2026-06-05.
- Ni la RC, ni el informe monetario, ni el comunicado del Ministerio, ni el informe del FMI dicen de qué cuenta salieron los dólares. Queda abierto.
- Dato nuevo que no prueba nada: el informe del personal técnico del FMI lista entre los datos de seguimiento diario los depósitos del Tesoro en DEG en el BCRA, una categoría aparte de los depósitos en dólares. No dice cómo se acreditó el desembolso de mayo de 2026.

## 2. Hallazgo de fuente: el informe del FMI está en el sitio del BCRA

El informe del personal técnico del FMI de la segunda revisión (8 de mayo de 2026, 136 páginas, con el comunicado del 21 de mayo) está en https://www.bcra.gob.ar/archivos/Pdfs/Institucional/informe-fmi-eff-revision-02-2026-05.pdf y se baja sin bloqueo (SRC-1263). Contiene definiciones y tablas de reservas y de depósitos del Tesoro que no se leyeron a fondo en este lote. Puede servir para D-001.

## 3. Revisión (nada nuevo)

Al 2026-10-15, 22:33 hora de Brasilia: no hay planilla del III trimestre, ni SIGADE al 2026-09-30, ni RC 60/2026 en la OPC, ni comunicado con montos (ADEBA, último CE 14715).

## 4. Enlaces del lote V

`tablas/enlaces_reales_fuentes_bcra_lote_v.csv` da, para cada fuente de bcra.gob.ar, el enlace con el que se verificó la descarga hoy. En las 31 fuentes que daban 404 el error era de la ruta que armé yo: el BCRA no usa un patrón único para los PDF (varía la carpeta, mayúscula o minúscula, y el nombre del mes). Las 38 filas bajan hoy con HTTP 200 y el mismo sha256 que `sources.csv`. Las URL erróneas se corrigieron en `inbox/lote-v/sources.csv`.
