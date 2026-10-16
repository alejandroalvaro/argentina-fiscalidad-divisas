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

Las operaciones posteriores al corte son casi todas en pesos. La necesidad de divisas no cambia por estas causas (22.145 millones de USD con D-011).

## Consolidación del sector público (también en `argfx conciliacion`)

Saca de la necesidad de divisas los pagos a tenedores del sector público. Sin esos pagos no salen divisas del sector público consolidado (D-001). Trabaja en dos capas que no se mezclan:

- **Oficial.** La deuda bruta por acreedor de la Secretaría de Finanzas al 30-06-2026 (SRC-1014, verificada en el PDF): agencias del sector público 197.213 millones de USD, sector privado 177.738 y multilaterales y bilaterales 99.247, que suman la deuda bruta de A.1.1. De lo que tiene el sector público, el 31,5% está en dólares (62.119 millones) y el 1,2% bajo ley extranjera. Está en `tenencias/composicion_acreedor_2026-06-30.csv`.
- **Identificada.** `tenencias/tenencias_identificadas_2026-06-30.csv`, armada por `scripts/build_tenencias.py`:
  - `directo`: las letras intransferibles que SIGADE registra con acreedor BCRA y la LETRA/U$S/INTRA SP/19-02-2027 (31.538 millones);
  - `estimado`: los Globales del BCRA al 31-12-2025 (Anexo III, lote S) y los AL35 y AE38 que recibió en la conversión de la RC 31/2026 (6.739 millones). Que el BCRA los tuviera al corte es un supuesto.

Lo que el sector público tiene en dólares y no se identifica por instrumento (20.068 millones, tras sumar las letras en garantía del FODER a lo identificado, D-011) se reparte en proporción (`proporcional`) entre los bonos en dólares de SIGADE que no están del todo en su poder, separando por legislación. A los Globales (ley extranjera) les toca lo que falta para llegar al 1,2% oficial: 4,1% de su saldo libre. Al resto (Bonares, BONAR y BONTE en dólares, ley local) le toca el remanente: 41,5% de su saldo libre. Los préstamos del FMI, multilaterales y bilaterales nunca se reparten.

### Necesidad de divisas consolidada a 12 meses

| Componente | Millones de USD |
|---|---|
| Necesidad bruta (fase 2, con D-011) | 22.145 |
| Pagos al sector público, directo (LETRA/U$S/INTRA SP) | −1.228 |
| Pagos al sector público, estimado (bonos del BCRA) | −299 |
| Pagos al sector público, proporcional | −1.842 |
| **Necesidad consolidada** | **18.775** |

Entre la necesidad bruta y la consolidada hay 3.370 millones de USD. Solo la parte directa es firme. Con las capas directa y estimada, la necesidad consolidada queda en 20.618 millones, y la proporcional la baja hasta 18.775. El detalle por instrumento está en `data/conciliacion/necesidad_divisas_consolidada.csv`. Las letras intransferibles no aparecen porque sus intereses dependen del rendimiento de las reservas y quedan sin monto en el escenario congelado.

**Letras en garantía (D-011).** Las 109 letras en garantía del FODER (3.774 millones de USD) son deuda contingente en poder de un fideicomiso público: salen de la necesidad firme (266 millones a 12 meses) y entran como tenencia identificada del sector público.

### Deuda en pesos en poder del sector público

`argfx conciliacion` también reparte la deuda pagadera en pesos (`src/argfx/reconcile/pesos.py`). La capa oficial aplica la composición por moneda de lo que tienen las agencias del sector público (SRC-1014) a su total. La capa identificada suma lo que informa cada tenedor (`tenencias/tenencias_pesos_2026-06-30.csv`): el balance mensual del BCRA (títulos públicos en pesos), el informe mensual del FGS por categoría y los estados del Banco Nación. Las valuaciones no son las mismas (contable, de mercado, de libros), así que esta capa sirve para controlar el orden de magnitud de la oficial y no la reemplaza.

| Grupo (SIGADE) | Deuda bruta | En poder del sector público (oficial) | % | En otras manos |
|---|---|---|---|---|
| Pesos ajustados por CER | 112.637 | 78.881 | 70,0 | 33.756 |
| Pesos nominales (fija, variable, duales y adelantos del BCRA) | 103.563 | 54.034 | 52,2 | 49.530 |
| Dólar-linked pagadera en pesos | 8.954 | 2.169 | 24,2 | 6.785 |
| **Total en pesos** | **225.154** | **135.084** | **60,0** | **90.070** |

En millones de USD al tipo de cambio del corte. Lo identificado suma 125.315: BCRA 52.843, FGS 52.644 y Banco Nación 19.828. Es el 93% de la cifra oficial. El Banco Nación incluye 8.061 de filas "otros" que pueden tener bonos en dólares o provinciales, y no está claro si la nota de Finanzas lo cuenta entre los "organismos del sector público nacional".

Seis de cada diez pesos de deuda están en manos del propio sector público, y siete de cada diez en la deuda CER. La deuda en pesos en manos privadas, que es la que se refinancia en el mercado, ronda los 90.000 millones de USD.

## Intereses capitalizados devengados (D-009, `argfx devengados`)

La planilla trimestral de Finanzas (A.2.2) tiene una línea oficial de capitalización de intereses ("Capitalización de Bonos, Letras y otros préstamos"), separada de la variación por CER y por tipo de cambio. Según su nota (*), incluye la capitalización acumulada por las ampliaciones de bonos y letras. Al reabrir una LECAP o una BONCAP, el valor nominal nuevo entra a la par y lo capitalizado desde la emisión entra por esta línea. Esa parte la pagó el comprador en efectivo, así que no es interés devengado en el trimestre. Por eso el módulo resta, colocación por colocación (planillas de colocaciones de ONCP 2024 a 2026), lo capitalizado que trae cada ampliación:

- **LECAP y BONCAP a tasa fija:** valor nominal × [(1 + TEM)^(DÍAS/30) − 1], con DÍAS entre la emisión y la liquidación en 30E/360, que es la fórmula legal.
- **Ampliaciones TAMAR y duales:** su TEM no figura en la planilla, así que se usa como aproximación el valor efectivo menos el nominal.

Las planillas usadas están registradas por sha256 en `series/finanzas_planillas_trimestrales.csv` y `series/oncp_colocaciones.csv`. La serie fiscal es el resultado del sector público nacional en base caja (lote I), sumado por trimestre. Unidades: miles de millones de pesos corrientes.

| Trimestre | Línea A.2.2 | Capitalización en ampliaciones | Capitalizado devengado | Descuento de colocación devengado | Resultado financiero SPN (caja) | Con lo devengado no pagado |
|---|---|---|---|---|---|---|
| 2024T1 | 6 | 0 | 6 | 0 | 1.133 | 1.127 |
| 2024T2 | 879 | 21 | 858 | 0 | 1.439 | 581 |
| 2024T3 | 6.562 | 1.245 | 5.318 | −13 | −131 | −5.435 |
| 2024T4 | 7.484 | 1.150 | 6.334 | −157 | −677 | −6.854 |
| 2025T1 | 12.577 | 6.249 | 6.327 | −436 | 1.309 | −4.582 |
| 2025T2 | 17.193 | 8.323 | 8.870 | −706 | 1.786 | −6.378 |
| 2025T3 | 34.219 | 22.963 | 11.256 | −426 | 531 | −10.298 |
| 2025T4 | 16.607 | 7.172 | 9.436 | 174 | −2.173 | −11.782 |
| 2026T1 | 12.405 | 2.555 | 9.850 | −43 | 1.734 | −8.073 |
| 2026T2 | 11.997 | 2.943 | 9.054 | 0 | −278 | −9.332 |

Los resultados en base caja de 2026 suman 1.456 en el semestre, igual al Boletín Fiscal del segundo trimestre (SRC-0610).

**Descuentos de colocación.** El Tesoro debe el valor técnico y recibe el valor efectivo. Para cada colocación en efectivo de LECAP y BONCAP con valor técnico conocido (el nominal en una emisión nueva, el nominal por el factor de capitalización en una ampliación a tasa fija), la diferencia se reparte por días entre la liquidación y el vencimiento. El neto es chico y casi siempre negativo: con las tasas en baja, los compradores pagaron por encima del valor técnico, y esa prima baja el costo. Va de −706 a +174 por trimestre, contra 5.000 a 11.000 de capitalización.

**Perímetro del SPN (tenencia del FGS).** El informe mensual del FGS da la cartera por categoría y no por especie (`tenencias/fgs_cartera_categorias.csv`: SRC-1166 del lote R y SRC-1311 a SRC-1318 del lote AB, lecturas web porque ANSES responde 403 a la descarga; diciembre de 2024 sale del Cuadro 4 del Informe Anual 2024, SRC-1319, cuyo original sí está en R2; en cada fecha las categorías suman el total publicado). Contra el valor nominal actualizado de A.1.7, cada categoría acota la parte del FGS en las LECAP y BONCAP que capitalizan: como máximo, lo que tiene en la categoría hasta el saldo capitalizable de esa categoría; como mínimo, lo que tiene más allá de los instrumentos que no capitalizan y pueden estar en la misma categoría (las LELINKs entre las letras, los BONTE a tasa fija entre los bonos). Ningún informe dice dónde van las LELINKs, y por eso el rango queda abierto. Al 30-06-2026, con 125.100 miles de millones de saldo capitalizable, el FGS tiene entre 10,6% y 16,3%.

| Trimestre | FGS en LECAP y BONCAP | Devengado no pagado, AC | Devengado no pagado, SPN | Resultado financiero con lo devengado, AC | Ídem, perímetro SPN |
|---|---|---|---|---|---|
| 2024T1 | 0,0% a 0,0% | 6 | 6 a 6 | 1.127 | 1.128 a 1.128 |
| 2024T2 | 0,0% a 3,8% | 858 | 826 a 858 | 581 | 581 a 613 |
| 2024T3 | 0,0% a 7,1% | 5.304 | 4.929 a 5.304 | −5.435 | −5.435 a −5.060 |
| 2024T4 | 3,0% a 6,8% | 6.177 | 5.756 a 5.993 | −6.854 | −6.670 a −6.433 |
| 2025T1 | 13,6% a 14,7% | 5.892 | 5.023 a 5.090 | −4.582 | −3.781 a −3.714 |
| 2025T2 | 18,5% a 21,2% | 8.164 | 6.431 a 6.657 | −6.378 | −4.871 a −4.645 |
| 2025T3 | 11,6% a 13,4% | 10.830 | 9.374 a 9.576 | −10.298 | −9.045 a −8.842 |
| 2025T4 | 13,7% a 18,5% | 9.610 | 7.836 a 8.294 | −11.782 | −10.467 a −10.009 |
| 2026T1 | 10,5% a 17,4% | 9.808 | 8.097 a 8.779 | −8.073 | −7.045 a −6.362 |
| 2026T2 | 10,6% a 16,3% | 9.054 | 7.578 a 8.093 | −9.332 | −8.371 a −7.856 |

La categoría de bonos en pesos a tasa fija aparece en diciembre de 2024 y la de TAMAR en marzo de 2025, así que hasta septiembre de 2024 el ajuste cubre solo las letras. Desde 2024T3 el resultado con lo devengado es deficitario en todos los trimestres con cualquier valor del rango.

**Cómo leerlo.**
- La línea oficial de capitalización sobrestima el interés del trimestre cuando hay muchas ampliaciones. En 2025T3, dos tercios de la línea (22.963 de 34.219) eran capitalización ya pagada por los compradores.
- El interés capitalizado devengado va de 5 a 11 billones de pesos por trimestre desde mediados de 2024. Como no pasa por los intereses en base caja (JGM, Informe 144, pregunta 58), el resultado financiero que lo incluye es deficitario en todos los trimestres desde 2024T3.

**Limitaciones.**
- **Perímetros.** A.2.2 es la Administración Central con todos los tenedores. Los intereses netos del SPN excluyen los pagos dentro del SPN. El ajuste por el FGS es un rango. Otros organismos del SPN (fondos fiduciarios, por ejemplo) también pueden tener LECAP y BONCAP, y no están descontados. El FGS valúa a precio de mercado y A.1.7 a valor técnico, lo que mueve el rango en la diferencia entre ambos.
- **2024T1.** La línea no incluía todavía la LECAP: el rótulo la suma desde 2024T2.
- **Descuentos.** Faltan las ampliaciones TAMAR y duales, cuyo valor técnico no se conoce (su capitalización se aproxima con el valor efectivo, así que la prima queda adentro), y los canjes. No se suma el ajuste por CER, que la planilla registra aparte (7.000 a 41.000 miles de millones por trimestre).
- **Filas sin dato.** Son tres ampliaciones TAMAR o duales, sin valor efectivo.
- **Comparación externa.** La estimación de CEPA para enero a mayo de 2026 (11,37 billones, lote I) no es comparable sin conocer su método.

## Lo que falta en la fase 3

1. **Tenencias en pesos.** Hecha por grupo de moneda e indexación (ver arriba). Falta abrirla por instrumento: las tenencias por especie del BCRA son del 31-12-2025.
2. **Resultado financiero con intereses devengados (D-009).** Hecho para el interés capitalizado y los descuentos de colocación. La tenencia del FGS está descontada, como rango, en todos los trimestres.
3. **Movimientos sin conciliar anotados.** RC 30/2026: USD 1.040 millones que no se ven en los depósitos del Tesoro (lotes V a X). Bajas sin operación de TMF27, TMG27 y TZX27 (lotes L y M).
