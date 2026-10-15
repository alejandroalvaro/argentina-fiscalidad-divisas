# Lote J: los cuatro pendientes de duales

Rama `grok/lote-j`, carpeta `inbox/lote-j/`. Fuentes SRC-0924 a SRC-0943, claims CLM-J-001 a CLM-J-024, todo `sin_revisar`. Leí `formato-duales` y `lote-i4-incorporado`; no hay mensajes claude-a-grok posteriores. Los originales (PDF, imágenes, html, json) no están en la rama: quedan en la caja con sha256 en `documents_manifest.csv`.

## Validación
`argfx validate` real sobre origin/main más `inbox/lote-j`: 1 error, el mismo de main (INS-I-0007, `indice_inicial` faltante en lote-i), 2.268 advertencias, sin ninguna nueva. Con las filas nuevas superpuestas sobre `contratos/`, `argfx calendario` al corte 2026-06-30 carga 100 instrumentos con términos (96 en main) y los cuatro duales entran como "dual: falta trayectoria para comparar".

## Qué se cargó
- `contratos/terminos.csv` (4 filas): INS-C-0410, 0411 y 0412 (CER, tasa cero, `indice_inicial` = CER del día de emisión; el CER del décimo día hábil previo está en notas) e INS-C-0362 (rama fija 2,14% mensual capitalizable, 30E/360, `fija_por_periodo`). `saldo_corte` igual a SIGADE.
- `contratos/tasas.csv`: INS-C-0362, 2,14% desde 2025-01-29.
- `contratos/duales.csv` (4 filas): 0410 a 0412 con TAMAR + 3%, `tem_dias` 32, `promedio_plazo`, `factor_saldo` = CER de emisión, `saldo_es_valor_nominal` true; 0362 con TAMAR sin margen, provisional.
- `contratos/amortizaciones.csv`, `fechas.csv`, `operaciones.csv`: solo encabezado, el validador los exige.
- `tablas/vno_boncap_tamar_2026-06-30.csv`, `tablas/duales_bonte_unidades_cer.csv`, `tablas/ttd26_ramas.csv`.

## Los cuatro pendientes
1. **TTD26 (INS-C-0362)**: ramas completas en la RC 4/2025. Falta el VNO original y el saldo de SIGADE (7.498.004.805.716,07) parece ya capitalizado. `factor_saldo` 1,0 y `saldo_es_valor_nominal` false son provisionales. **Para Alejandro:** confirmar qué representa ese saldo.
2. **BONAR Dual 2036 (INS-C-0357)**: no hay norma con fechas. El anexo III del DNU 164/2023 fija los términos (dólares, pago en pesos, CER o A3500, 3%, hasta 13 años) pero no emisión ni vencimiento. No cargué filas. La "Res. Conj. 53-E/2023" no apareció. **Para Alejandro:** indicar la norma de emisión si la tiene.
3. **INS-C-0410 a 0412**: 0410 es el BONO CER/TAMAR 2030 de la RC 32 art. 5; 0411 es el de la RC 23 art. 3 (ampliado por la RC 25 art. 5); 0412 es el de la RC 25 art. 1. Unidades de SIGADE por el CER de emisión reproducen el VNO adjudicado con diferencia menor a 0,7 millones.
4. **VNO de los cinco BONCAP TAMAR** al 2026-06-30 con cadena de eventos. TML27, TMG28, TMF27 y TMG27 salen de totales publicados por Finanzas; TMF28 es derivado por suma. Razón saldo SIGADE / VNO: TML27 1,0000; TMG28 1,0496; TMF28 1,0497; TMF27 0,9930; TMG27 0,8273.

## Huecos y preguntas
- **Para Alejandro:** SIGADE de TMG27 está 17,3% por debajo del VNO y TMF27 0,7% por debajo; TMG28 y TMF28 están casi 5% por encima. No lo expliqué ni lo ajusté.
- Base: la RC 4/2025 dice 30/360 y usé 30E/360, la convención del repositorio para los BONCAP (CLM-G-023). Confirmar.
- `primer_periodo` de INS-C-0362 es 2025-02-28 (febrero no tiene día 29); el motor genera fechas de capitalización los días 28. No afecta el pago, que es al vencimiento.
- La imagen de la TAMAR TEM del Boletín Oficial (RC 4/2025) es de baja resolución; la leí con la estructura de las RC 23, 25 y 32.
- TTS26 (INS-C-0361, vencido 2026-09-15): sin operaciones posteriores al corte encontradas, sin filas.
- Siguen pendientes los montos de las conversiones con el BCRA de las RC 39, 51, 53 y 60, y SIGADE al 2026-09-30.
