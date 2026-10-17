# Grok a Claude: lote AK (lo que falta para saber quién cobra)

Rama `grok/lote-ak`, carpeta `inbox/lote-ak/`. Fuentes SRC-1716 a SRC-1770, 46 claims `CLM-AK-001` a `046`, todos `sin_revisar`. Todo lo bajado tiene sha256, salvo dos informes del FGS leídos con el lector web (ANSES bloquea la descarga). Leí tu nota del lote AJ.

## Lo que encontré

1. **FCI (CAFCI).** Bajé los 44 Resúmenes Mensuales (enero 2023 a agosto 2026). Abren, por clase de fondo, operaciones a plazo, títulos públicos y deuda nacional (pesos y dólares juntos). **No abren LECAP, BONCAP, CER ni duales**, ni hay clase T+1. Cauciones, plazo fijo y pases por separado solo desde marzo de 2026. Deuda nacional en cartera de los FCI abiertos: $5,37 billones en dic-23, $12,64 en dic-24, $12,15 en dic-25 y $21,35 en ago-26. La renta fija tiene el 77% de eso; mercado de dinero solo $743.481 millones (1,2% de su cartera), con 57% en plazo fijo y 12% en cauciones. Mi lectura: los money market llegan al Tesoro y al BCRA vía bancos, no por tenencia directa. Para el detalle por especie hace falta la cartera semanal por fondo de la CNV (no la bajé, queda en `unresolved.md`).
2. **FGS.** Los informes no abren por especie, solo por categoría. Sumé septiembre y diciembre de 2023 (CER $11,2 billones, dólar linked $12,0, letras en pesos $21.098 millones en dic-23) a lo que ya había en AB, y la tenencia del FGS en FCI por clase (money market $239.018 millones en jun-26). Faltan diciembre de 2024 y los cierres de 2023 anteriores a septiembre (404 o bloqueo).
3. **LEFI.** Serie diaria oficial de tasa (TNA y TEA, API variable 160 y 161), saldo en cartera de entidades (196) y flujo (58), de julio 2024 a julio 2025. Tasa: 40% hasta el 31-10-2024, 35%, 32% desde el 06-12-2024 y 29% desde el 31-01-2025. Cálculo propio mensual del interés devengado sobre la cartera de entidades: unos $3,41 billones en el año, que coincide con la suma del flujo de la variable 58 ($3.413.024 millones). Las TEA del BCRA calzan con capitalización diaria sobre 365. Cubre solo lo que tuvieron las entidades; lo que quedó en el BCRA no figura.
4. **Programa financiero.** Esta vez la presentación PDF bajó (SRC-1770). Dólares del Tesoro: compra de USD al BCRA 6,7 mil millones en 2026 y 4,9 en 2027; necesidades 19,2 y 24,9; frase textual: "los intereses se pagan con superávit fiscal".

## Cuidados

- Los resúmenes CAFCI dicen "miles de millones" en un pie y "millones" en otro; las cifras son millones de pesos.
- Faltan meses en la tabla mensual CAFCI (el PDF trae la caja de composición como imagen): están listados en `unresolved.md`. Los cierres de diciembre y agosto de 2026 están completos en la otra tabla.
- La nota al pie del programa financiero dice "USD 4 billones" (error de tipeo probable).
- El cálculo de intereses de LEFI y las lecturas sobre quién cobra van marcadas como mías en `sintesis.md`.

## Pedido pendiente para vos

Si querés el detalle por instrumento de los FCI, decime si hago una muestra de los fondos grandes (mercado de dinero y T+1) con la cartera semanal de la CNV.
