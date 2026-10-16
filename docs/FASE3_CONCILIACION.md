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

## Consolidación del sector público (también en `argfx conciliacion`)

Saca de la necesidad de divisas los pagos a tenedores del sector público. Sin esos pagos no salen divisas del sector público consolidado (D-001). Trabaja en dos capas que no se mezclan:

- **Oficial.** La deuda bruta por acreedor de la Secretaría de Finanzas al 30-06-2026 (SRC-1014, verificada en el PDF): agencias del sector público 197.213 millones de USD, sector privado 177.738 y multilaterales y bilaterales 99.247, que suman la deuda bruta de A.1.1. De lo que tiene el sector público, el 31,5% está en dólares (62.119 millones) y el 1,2% bajo ley extranjera. Está en `tenencias/composicion_acreedor_2026-06-30.csv`.
- **Identificada.** `tenencias/tenencias_identificadas_2026-06-30.csv`, armada por `scripts/build_tenencias.py`:
  - `directo`: las letras intransferibles que SIGADE registra con acreedor BCRA y la LETRA/U$S/INTRA SP/19-02-2027 (31.538 millones);
  - `estimado`: los Globales del BCRA al 31-12-2025 (Anexo III, lote S) y los AL35 y AE38 que recibió en la conversión de la RC 31/2026 (6.739 millones). Que el BCRA los tuviera al corte es un supuesto.

Lo que el sector público tiene en dólares y no se identifica por instrumento (23.842 millones) se reparte en proporción (`proporcional`) entre los bonos en dólares de SIGADE que no están del todo en su poder, separando por legislación. A los Globales (ley extranjera) les toca lo que falta para llegar al 1,2% oficial: 4,1% de su saldo libre. Al resto (Bonares, BONAR y BONTE en dólares, ley local) le toca el remanente: 50,3% de su saldo libre. Los préstamos del FMI, multilaterales y bilaterales nunca se reparten.

### Necesidad de divisas consolidada a 12 meses

| Componente | Millones de USD |
|---|---|
| Necesidad bruta (fase 2) | 22.411 |
| Pagos al sector público, directo (LETRA/U$S/INTRA SP) | −1.228 |
| Pagos al sector público, estimado (bonos del BCRA) | −299 |
| Pagos al sector público, proporcional | −2.192 |
| **Necesidad consolidada** | **18.691** |

Entre la necesidad bruta y la consolidada hay 3.720 millones de USD. Solo la parte directa es firme. Con las capas directa y estimada, la necesidad consolidada queda en 20.883 millones, y la proporcional la baja hasta 18.691. El detalle por instrumento está en `data/conciliacion/necesidad_divisas_consolidada.csv`. Las letras intransferibles no aparecen porque sus intereses dependen del rendimiento de las reservas y quedan sin monto en el escenario congelado.

**Sensibilidad abierta: letras en garantía.** Las 109 letras en garantía de SIGADE (3.774 millones de USD, 266 millones en la necesidad a 12 meses) respaldan contratos de energías renovables. Hoy cuentan como deuda firme. Si las tiene el FODER, que es un fondo fiduciario público, son tenencia del sector público y probablemente deuda contingente. En ese caso salen de la necesidad firme, y la parte proporcional de los Bonares baja de 50% a 41%. Pedido a Grok.

## Intereses capitalizados devengados (D-009, `argfx devengados`)

La planilla trimestral de Finanzas (A.2.2) tiene una línea oficial de capitalización de intereses ("Capitalización de Bonos, Letras y otros préstamos"), separada de la variación por CER y por tipo de cambio. Según su nota (*), incluye la capitalización acumulada por las ampliaciones de bonos y letras. Al reabrir una LECAP o una BONCAP, el valor nominal nuevo entra a la par y lo capitalizado desde la emisión entra por esta línea. Esa parte la pagó el comprador en efectivo, así que no es interés devengado en el trimestre. Por eso el módulo resta, colocación por colocación (planillas de colocaciones de ONCP 2024 a 2026), lo capitalizado que trae cada ampliación:

- **LECAP y BONCAP a tasa fija:** valor nominal × [(1 + TEM)^(DÍAS/30) − 1], con DÍAS entre la emisión y la liquidación en 30E/360, que es la fórmula legal.
- **Ampliaciones TAMAR y duales:** su TEM no figura en la planilla, así que se usa como aproximación el valor efectivo menos el nominal.

Las planillas usadas están registradas por sha256 en `series/finanzas_planillas_trimestrales.csv` y `series/oncp_colocaciones.csv`. La serie fiscal es el resultado del sector público nacional en base caja (lote I), sumado por trimestre. Unidades: miles de millones de pesos corrientes.

| Trimestre | Línea A.2.2 | Capitalización en ampliaciones | Capitalizado devengado | Resultado financiero SPN (caja) | Con capitalizado devengado |
|---|---|---|---|---|---|
| 2024T1 | 6 | 0 | 6 | 1.133 | 1.127 |
| 2024T2 | 879 | 21 | 858 | 1.439 | 581 |
| 2024T3 | 6.562 | 1.245 | 5.318 | −131 | −5.448 |
| 2024T4 | 7.484 | 1.150 | 6.334 | −677 | −7.011 |
| 2025T1 | 12.577 | 6.249 | 6.327 | 1.309 | −5.018 |
| 2025T2 | 17.193 | 8.323 | 8.870 | 1.786 | −7.084 |
| 2025T3 | 34.219 | 22.963 | 11.256 | 531 | −10.725 |
| 2025T4 | 16.607 | 7.172 | 9.436 | −2.173 | −11.608 |
| 2026T1 | 12.405 | 2.555 | 9.850 | 1.734 | −8.116 |
| 2026T2 | 11.997 | 2.943 | 9.054 | −278 | −9.332 |

Los resultados en base caja de 2026 suman 1.456 en el semestre, igual al Boletín Fiscal del segundo trimestre (SRC-0610).

**Cómo leerlo.**
- La línea oficial de capitalización sobrestima el interés del trimestre cuando hay muchas ampliaciones. En 2025T3, dos tercios de la línea (22.963 de 34.219) eran capitalización ya pagada por los compradores.
- El interés capitalizado devengado va de 5 a 11 billones de pesos por trimestre desde mediados de 2024. Como no pasa por los intereses en base caja (JGM, Informe 144, pregunta 58), el resultado financiero que lo incluye es deficitario en todos los trimestres desde 2024T3.

**Limitaciones.**
- **Perímetros.** A.2.2 es la Administración Central con todos los tenedores. Los intereses netos del SPN excluyen los pagos dentro del SPN, por ejemplo al FGS. Lo que el FGS tenga en LECAP y BONCAP está en la columna de devengado y no debería estarlo para el SPN, así que la columna sobrestima en esa medida.
- **2024T1.** La línea no incluía todavía la LECAP: el rótulo la suma desde 2024T2.
- **Descuentos.** No se suman los descuentos de colocación (valor efectivo por debajo del valor técnico), que también son costo devengado. Tampoco el ajuste por CER, que la planilla registra aparte (7.000 a 41.000 miles de millones por trimestre).
- **Filas sin dato.** Son tres ampliaciones TAMAR o duales, sin valor efectivo.
- **Comparación externa.** La estimación de CEPA para enero a mayo de 2026 (11,37 billones, lote I) no es comparable sin conocer su método.

## Lo que falta en la fase 3

1. **Tenencias en pesos.** La consolidación de la deuda en pesos (BCRA, Banco Nación, FGS) queda para después: no cambia la necesidad de divisas, y las tenencias por especie del BCRA son del 31-12-2025, con muchas LECAP vencidas y reemplazadas en 2026.
2. **Resultado financiero con intereses devengados (D-009).** Hecho para el interés capitalizado (ver arriba). Falta separar la tenencia del FGS para el perímetro del SPN y sumar los descuentos de colocación.
3. **Movimientos sin conciliar anotados.** RC 30/2026: USD 1.040 millones que no se ven en los depósitos del Tesoro (lotes V a X). Bajas sin operación de TMF27, TMG27 y TZX27 (lotes L y M).
