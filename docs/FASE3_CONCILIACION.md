# Fase 3: conciliación

La fase 3 contrasta el inventario y el calendario de obligaciones con las series oficiales, saca las tenencias dentro del sector público y reconstruye el resultado financiero con intereses devengados (D-009). Este documento cubre la primera parte, ya construida. Las otras dos se describen al final, con los insumos que ya están en el repositorio.

## Conciliación con la planilla de Finanzas (`argfx conciliacion`)

Usa la planilla trimestral de deuda de la Secretaría de Finanzas al corte (`deuda_publica_30-06-2026_0.xlsx`, SRC-0103 y SRC-1005). El comando la baja de R2 por su sha256. Lee tres hojas (`src/argfx/reconcile/finanzas.py`) y escribe en `data/conciliacion/`:

| Tabla | Control |
|---|---|
| `stock.csv` | Saldos de SIGADE al corte contra A.1.1: deuda en situación de pago normal, organismos internacionales y adelantos transitorios del BCRA |
| `flujos_trimestre.csv` | Identidades de A.2.2: saldo inicial más variaciones igual a saldo final; la variación total como suma de sus partes; operaciones de crédito público como financiamiento menos amortizaciones |
| `perfil.csv` | Perfil mensual de vencimientos de A.3.1 (doce meses, capital e interés) contra la proyección de SIGADE y contra el calendario |
| `atribucion.csv` | Calendario menos SIGADE, por mes, concepto y causa |

Montos en millones de USD a los tipos de cambio del corte, que son los de A.3.1 y los del escenario congelado. La materialidad se configura con `--umbral-abs` (millones de USD, 10 por defecto) y `--umbral-rel` (0,001): una diferencia es material cuando supera los dos umbrales.

### Resultados al 2026-06-30

- **Stock.** SIGADE suma 471.689,8 millones de USD, igual a la deuda en situación de pago normal de A.1.1. Organismos internacionales (96.425,0) y adelantos transitorios (2.758,6) también coinciden.
- **Flujos del segundo trimestre.** Las cuatro identidades de A.2.2 cierran. La amortización de letras intransferibles (22.284,1 millones) es la compra al BCRA de las RC 27 y 30/2026 (lote T).
- **Perfil.** La proyección de SIGADE reproduce A.3.1 en los 24 casos (12 meses, capital e interés). El perfil oficial sale de SIGADE.
- **Calendario contra perfil oficial.** A doce meses, el calendario tiene 32.913 millones de USD más de capital y 309 millones menos de interés que A.3.1. La atribución lo explica todo, sin residuo:

| Causa | Capital | Interés |
|---|---|---|
| Operaciones posteriores al corte (emisiones, reaperturas, canjes) | +36.328 | +71 |
| Capitalización de LECAP y BONCAP hasta el vencimiento | +3.638 | |
| Base y rezago de índices (CER, A 3500, TAMAR, BADLAR) | +943 | +2 |
| Duales | | +10 |
| Flujos sin monto en el escenario congelado (TAMAR, BADLAR, duales) | −7.997 | −391 |

Las operaciones posteriores al corte son casi todas en pesos. La necesidad de divisas sigue en 22.410 millones de USD (fase 2).

## Lo que falta en la fase 3

1. **Consolidación del sector público.** Hay que sacar las tenencias de deuda del Tesoro dentro del sector público:
   - BCRA: Anexo III de los estados contables, por especie al 31-12-2025 (lote R), llevado al corte con las compras y conversiones de 2026 (lotes I, K y T).
   - Banco Nación: por especie al 30-06-2026 (lote R).
   - Letras intransferibles: directo en SIGADE.
   - FGS: solo por categoría.

   El mapeo a `instrument_id` está en el lote S. La salida separa Tesoro, BCRA y sector público consolidado, sin doble conteo.
2. **Resultado financiero con intereses devengados (D-009).** Intereses devengados por instrumento con el motor (capitalización de LECAP y BONCAP, descuentos de emisión) contra el gasto en intereses de base caja. El control anual es la identidad devengado = pagado + variación del stock de devengados no exigibles (Anexo G de la Cuenta de Inversión, lote R).
3. **Movimientos sin conciliar anotados.** RC 30/2026: USD 1.040 millones que no se ven en los depósitos del Tesoro (lotes V a X). Bajas sin operación de TMF27, TMG27 y TZX27 (lotes L y M).
