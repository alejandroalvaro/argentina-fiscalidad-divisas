# Lote AN: dos correcciones a la tabla de fuentes y aplicaciones del lote AM

No hay fuentes nuevas: todo sale de las planillas AIF base caja de la ONP ya registradas en el lote AM (SRC-1989 a SRC-2022; `sources.csv` va solo con encabezado). Cada cifra trae hoja y fila en `aif_filas_por_mes_y_concepto.csv`. Montos en millones de pesos corrientes.

## 1. Inversión financiera: estaba mal la fila

El lote AM buscaba la primera fila que empezara con "INVERSION FINANCIERA" y levantaba la del bloque V) GASTOS DE CAPITAL (diciembre 2023: hoja AI, fila 50, $22,1 millones en el total). La fila correcta es la subpartida de XVII) APLICACIONES FINANCIERAS (diciembre 2023: fila 86, $751.559,9 millones total y $21.334,9 Tesoro). Corregí la búsqueda para que tome solo filas posteriores a APLICACIONES FINANCIERAS. En los 34 meses cambian únicamente las dos columnas `inversion_financiera_*`; el resto de la tabla coincide con la anterior. Septiembre 2026 queda en blanco porque su planilla no trae el bloque de financiamiento.

## 2. La fuente que falta son las rentas percibidas del BCRA

En el total del Sector Público Nacional, resultado financiero (XV) más fuentes (XVI) menos aplicaciones (XVII) cierra en cero en 31 de los 33 meses con bloque de financiamiento. En abril 2025 da -11.976.386,7 y en mayo 2026 da -24.400.000,0. En ambos casos la diferencia es igual, a la décima de millón, a la partida informativa "- RENTAS PERCIBIDAS DEL BCRA" (abril 2025: fila 75, $11.976.386,7; mayo 2026: fila 74, $24.400.000,0), que la nota (1) de cada planilla dice que se excluye de los ingresos. Sumada como fuente, la brecha queda en cero en los 33 meses con bloque de financiamiento (hasta 0,002 millones de diferencia de redondeo). En los demás meses esa fila vale 0.

- Desembolso del FMI: no es la fuente faltante. El endeudamiento en moneda extranjera del Tesoro ya está en las fuentes financieras (abril 2025: fila 83, $16.732.211,7; mayo 2026: fila 82, $5.299.006,1). La planilla no identifica el FMI por nombre.
- Uso de depósitos en divisas: la planilla no tiene una fila con ese nombre; no hay evidencia de que sea la brecha.
- Recompra de Letras Intransferibles: la planilla no la identifica. Lo que se ve es que las aplicaciones de esos meses son enormes (inversión financiera total abril 2025 $29.742.607,8, fila 88; amortización en moneda extranjera del Tesoro mayo 2026 $20.134.436,2, fila 90). Que esa sea la contrapartida no está probado con estas planillas.

Para el Sankey: agregar "Rentas percibidas del BCRA" como fuente del Tesoro en pesos, con su monto en abril 2025 y mayo 2026.
