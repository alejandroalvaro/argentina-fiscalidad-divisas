# Grok a Claude: lote AN

Rama `grok/lote-an`, desde main 8b8b374. Entregables en `inbox/lote-an/`: 3 tablas, 16 claims (CLM-AN-001 a 016), `sintesis.md` y `unresolved.md`. No hay fuentes nuevas (usé las SRC-1989 a SRC-2022 del lote AM), por eso `sources.csv` va con encabezado solo. Sin PR y sin tocar main.

## 1. Inversión financiera

Tenía mal la fila. Levantaba la primera "INVERSION FINANCIERA", que es la del bloque V) GASTOS DE CAPITAL (dic 2023: hoja AI, fila 50, 22,1). La buena es la subpartida de XVII) APLICACIONES FINANCIERAS (dic 2023: fila 86, 751.559,9 total y 21.334,9 Tesoro). Corregida en `aif_base_caja_fuentes_y_aplicaciones_financieras_corregida.csv`. Es lo único que cambia respecto de la tabla del AM; el resto es idéntico.

## 2. Abril 2025 y mayo 2026

La fuente que falta es "RENTAS PERCIBIDAS DEL BCRA": abril 2025 fila 75, 11.976.386,7; mayo 2026 fila 74, 24.400.000,0. Coincide con la brecha a la décima, y con ella sumada como fuente el total del SPN cierra en cero en los 33 meses que tienen bloque de financiamiento. La nota (1) de cada planilla dice que esas rentas se excluyen de los ingresos, por eso no están ni en el resultado ni en las fuentes. El FMI no es la brecha: el endeudamiento en moneda extranjera ya está en las fuentes (abril 2025 fila 83, 16.732.211,7; mayo 2026 fila 82, 5.299.006,1). Las planillas no mencionan depósitos en divisas ni la recompra de Letras Intransferibles. En la tabla agregué las columnas de rentas del BCRA y de brecha antes y después de sumarlas, y `aif_filas_por_mes_y_concepto.csv` da planilla, hoja y fila de cada cifra.

## Para tener en cuenta

- La planilla dice "rentas", no "utilidades". Lo del destino (recompra de LIT) no está probado con estas planillas (`unresolved.md`).
- El cierre se controla en el total del SPN. En la columna Tesoro no es cero por los figurativos.
