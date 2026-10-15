# Fase 2: motor contractual

El motor arma el calendario de obligaciones de la Administración Central a partir del saldo al corte (30/06/2026) y lo resume en los tramos del protocolo: mensual del mes 1 al 36 y anual del año 4 al 20. El código está en `src/argfx/contracts/` y se ejecuta con:

```bash
uv run argfx calendario            # deja las tablas en data/calendario/
```

## Cómo está armado

El cálculo va en tres pasos, y cada uno guarda su resultado por separado:

1. **Flujos contractuales** (`CashFlow`). Salen de los términos de cada instrumento y se expresan en la unidad del contrato: la moneda de cuenta, o unidades CER o UVA cuando el capital está indexado.
2. **Valuación bajo un escenario** (`Valuation`). Convierte cada flujo a moneda de cuenta, a moneda de liquidación y a USD. Las trayectorias de tasas, índices y tipos de cambio viven en el escenario y no en los términos.
3. **Tramos** (`aggregate`). Suma por tramo y por cada dimensión.

Cada flujo lleva por separado la moneda de cuenta, la indexación, la moneda de liquidación, el deudor, el tipo de acreedor y la residencia del tenedor. Lleva además si es firme o contingente (los avales son contingentes), si es un pago o interés que se capitaliza, y si su monto depende del escenario.

Un monto que no se puede calcular queda vacío y nunca se completa con cero. Pasa, por ejemplo, con una tasa flotante sin trayectoria en el escenario. Las sumas por tramo informan aparte cuántos flujos quedaron sin monto.

## Dos fuentes de flujos

| Fuente | Qué es | Cuándo entra al calendario |
|---|---|---|
| `motor` | Flujos calculados desde los términos de `contratos/` | Siempre que el instrumento tenga términos |
| `sigade` | Perfil de vencimientos de SIGADE al corte (SRC-0102), con tasas y tipos de cambio congelados | Para los instrumentos sin términos |

La columna `base` de `flujos.csv` marca qué flujo entra al calendario. Los flujos de SIGADE se conservan también para los instrumentos con términos, porque sirven de control: `comparacion_sigade.csv` contrasta los dos, fecha por fecha.

SIGADE identifica cada operación por el nombre, la moneda del préstamo y el tipo de tasa a la vez. Un mismo préstamo puede tener tramos en varias monedas, o un tramo fijo y otro SOFR en la misma moneda. Con esa clave, las 753 operaciones de `inbox/lote-c/instruments.csv` se vinculan una a una con el perfil de vencimientos.

## Módulos

| Archivo | Contenido |
|---|---|
| `model.py` | Tipos: obligación, flujo, dimensiones |
| `daycount.py` | Bases 30/360, ACT/365, ACT/360 y ACT/ACT (ISDA) |
| `schedule.py` | Fechas de pago sin ajuste por día hábil, como las informa SIGADE |
| `engine.py` | Cupones fijos con escalones (anuales o por período, como la TEM), cupones flotantes, capitalización y amortización |
| `options.py` | Duales: se queda con la rama que paga más bajo el escenario |
| `scenario.py` | Trayectorias y valuación; escenario `sigade_congelado_2026-06-30` |
| `sigade.py` | Lectura del perfil de vencimientos de SIGADE |
| `terms.py` | Lectura de `contratos/` |
| `buckets.py` | Tramos del protocolo |
| `calendar.py` | Arma las cuatro tablas de salida |

La amortización se expresa en fracciones del valor nominal original y se aplica a prorrata del saldo vigente en cada fecha. Así se respetan las recompras y los canjes parciales sin necesidad de conocer el valor nominal original.

## Salidas (`data/calendario/`)

- `flujos.csv`: todos los flujos de las dos fuentes, valuados, con el tramo de cada uno.
- `calendario.csv`: flujos de base por tramo y por dimensión.
- `necesidad_divisas.csv`: pagos firmes que se liquidan en una moneda distinta del peso, por tramo y por moneda de liquidación. La deuda dólar-linked pagadera en pesos queda afuera por construcción, porque su moneda de liquidación es ARS.
- `comparacion_sigade.csv`: motor contra SIGADE por instrumento.

## Términos contractuales (`contratos/`)

Hay tres tablas obligatorias y una optativa, y cada fila cita su fuente (`source_id` y `referencia`).

`terminos.csv`, una fila por instrumento:

| Columna | Contenido |
|---|---|
| `instrument_id` | Identificador de `instruments.csv` (lote C) |
| `deudor`, `tipo_acreedor`, `residencia_tenedor` | `tipo_acreedor`: privado, multilateral, bilateral, BCRA, sector_publico o desconocido. `residencia_tenedor`: residente, no_residente, mixta o desconocida |
| `moneda_cuenta`, `indexacion`, `moneda_liquidacion` | `indexacion`: ninguna, CER, UVA o dolar_linked |
| `estado` | firme o contingente |
| `fecha_corte`, `saldo_corte` | El saldo debe coincidir con `outstanding_principal` de SIGADE. En instrumentos CER se expresa en unidades CER, como en SIGADE (UCP) |
| `fecha_emision`, `primer_periodo`, `vencimiento`, `frecuencia_meses`, `fin_de_mes` | Calendario de períodos. En los capitalizables, cada período es una fecha de capitalización |
| `periodo_final_corto` | true si el vencimiento cae fuera de la grilla y cierra un último período corto (LECAP y BONCAP, Par) |
| `base` | 30/360 (convención ISDA), 30E/360 (meses de treinta días: el día 31 cuenta como 30 en ambos extremos), ACT/365, ACT/360 o ACT/ACT |
| `tipo_tasa` | fija (anual), fija_por_periodo (por ejemplo, la TEM), flotante o cero |
| `indice`, `margen`, `multiplicador` | Sólo para tasas flotantes: tasa = índice × multiplicador + margen |
| `tope_indice`, `tope_margen` | Tope de una tasa flotante: la tasa no supera tope_indice + tope_margen (letras del BCRA: LIBOR o SOFR menos un punto). Sin trayectoria del índice del tope, el interés queda sin monto |
| `capitaliza` | true si el interés se suma al capital y se paga al vencimiento |

`tasas.csv` tiene los escalones de tasa fija (`desde`, `tasa`), y `amortizaciones.csv` las fechas y fracciones del valor nominal original. Sin filas de amortización, el instrumento amortiza al vencimiento.

`fechas.csv` (optativa) enumera todas las fechas de fin de período de un instrumento cuando la norma las lista en lugar de seguir una grilla (los BONAR USD 6% de las RC 11/2026 y 16/2026, por ejemplo). Para ese instrumento reemplaza a `primer_periodo` y `frecuencia_meses`, y la última fecha tiene que ser el vencimiento.

### Capitalizables a tasa efectiva mensual (LECAP y BONCAP)

La norma fija el pago al vencimiento como VPV = VNO × (1 + Tm)^((DÍAS/360) × 12), con DÍAS contados entre la emisión y el vencimiento en meses de treinta días (RC 23/2026, SRC-0606, fórmula en imagen guardada en R2; RC 4/2025, CLM-G-017). SIGADE informa al corte un saldo que ya incluye la capitalización hasta el último aniversario mensual de la emisión (CLM-G-022 y CLM-G-023), y no proyecta la capitalización posterior: su perfil paga al vencimiento el saldo al corte.

Para reproducir la fórmula legal, los períodos se anclan en la fecha de emisión (`primer_periodo` = emisión más un mes, `fin_de_mes` si la emisión es fin de mes), con `periodo_final_corto=true` y `base=30E/360`. Cada período completo capitaliza Tm; el último, más corto, capitaliza (1 + Tm)^f − 1, con f la fracción del mes en 30E/360. En los nueve instrumentos de tasa fija del lote G, el pago al vencimiento coincide con el cálculo independiente de Grok desde el valor nominal dentro de 3,5 por millón, que es el redondeo del coeficiente de SIGADE.

Con una tasa por período sin capitalización, un período corto paga Tm × f.

### Operaciones posteriores al corte (`operaciones.csv`)

Por D-008, el análisis suma las operaciones del Tesoro posteriores al corte de SIGADE. El archivo opcional `contratos/operaciones.csv` tiene una fila por operación: `instrument_id`, `fecha` (liquidación), `tipo` (`emision`, `reapertura`, `canje_entrada`, `rescate`, `canje_salida`), `valor_nominal` (siempre positivo, en valor nominal original), `source_id` y `referencia`.

- Un instrumento emitido después del corte va en `terminos.csv` con `saldo_corte` 0 y una fila `emision` en su fecha de emisión.
- Las reaperturas suman valor nominal y los rescates y canjes de salida lo restan. El cambio rige desde el inicio del período en que se liquida, porque quien compra a mitad de período cobra el cupón completo (y paga el devengado en el precio).
- El motor convierte valor nominal en saldo con el factor de capitalización acumulado desde la emisión, en los instrumentos que capitalizan, o con la fracción aún no amortizada, en los demás.
- El precio de colocación o de rescate es financiamiento y no entra como flujo contractual.

## Prueba piloto: bonos step up 2030 y 2035 en USD

Los términos de GD30, AL30, GD35 y AL35 (INS-C-0398, 0404, 0399 y 0405) se cargaron desde la estructura financiera de la Oficina Nacional de Crédito Público (SRC-0106, hoja A.1) y el prospecto del canje de 2020 (SRC-0108, p. S-32). El motor reproduce el perfil de SIGADE en las 94 fechas y tipos de flujo, con una diferencia máxima de 0,000001 USD.

La prueba encontró un error en la fuente oficial. En SRC-0106, la fila del Global 2035 USD repite la amortización del 2030 (13 cuotas, la primera del 4%) y su tabla de tasas salta del 09/07/2028 al 09/07/2029. El prospecto, la fila del bono de ley argentina y SIGADE coinciden entre sí: 10 cuotas iguales desde el 09/01/2031, y 4,75% desde julio de 2027 y 5% desde julio de 2028. Los términos usan esa versión y lo anotan en `notas`.

## Controles sobre el conjunto

- La valuación con el escenario congelado reproduce las columnas en USD de SIGADE. En 13 de las 15 monedas la coincidencia es exacta. En la deuda CER, la diferencia es de 1,5 por diez millones, porque SIGADE convierte con un tipo UCP redondeado (1,855623) y el escenario usa el CER publicado (799,2033).
- El principal de base suma 471.689.807.580 USD, frente a un saldo de 471.689.788.348 USD en SIGADE y en el cuadro A.1.1. La diferencia de 19.232 USD es ese mismo redondeo.
- SIGADE escribe la fecha de servicio con año de dos dígitos, y Python lee 69 a 99 como 1969 a 1999. Los vencimientos de 2069 a 2089 quedaban en el pasado. El cargador toma la fecha de las columnas Año, Mes y Día y verifica que coincida con la fecha de servicio.

## Lotes G y G3: términos de bonos y letras

El lote G agregó 70 instrumentos y el G3 otros siete (BONAR USD 6%, los cuatro Par y el bono del Consenso Fiscal), de modo que `contratos/` cubre 81. El motor los compara con SIGADE fecha por fecha (`comparacion_sigade.csv`). Un flujo coincide si la diferencia es de hasta 0,01 unidades o de hasta una parte en cien millones del monto de SIGADE (columna `max_dif_rel`).

| Resultado | Instrumentos | Motivo |
|---|---|---|
| Coinciden | 54 | |
| Flotantes sin trayectoria | 12 | BADLAR, rendimiento de las reservas y Bocon PR17: el interés queda sin monto. La amortización y los flujos con monto coinciden |
| LECAP y BONCAP a tasa fija | 9 | Diferencia esperable: SIGADE no proyecta la capitalización posterior al corte. El motor paga entre 5% y 37% más al vencimiento, en total unos 14,1 billones de pesos, en línea con los 14,2 billones que calcula Grok |
| BONCAP TAMAR | 5 | Capitalizan por mes desde la emisión (lote G2). El pago al vencimiento queda sin monto porque depende de la TAMAR promedio de todo el plazo |
| Discount CER 2033 | 1 | Diferencia relativa de 2,1 por cien mil: SIGADE no reparte las cuotas en partes exactamente iguales |

### Base 30/360 y febrero

El lote G3 mostró dos reglas de SIGADE que el motor ahora reproduce:

- El último día de febrero, al inicio de un período, cuenta como día 30 (base US). Del 29-02-2028 al 31-03-2028 hay 30 días, no 32 (BONAR USD 6% 2028, INS-C-0360).
- En una grilla regular de fin de mes, cada período completo devenga sus meses nominales: del 31-01 al 28-02 es un mes, como del 28-02 al 31-03 (Consenso Fiscal, INS-C-0358). Cuando las fechas vienen listadas en la norma (`fechas.csv`), que ya están corridas a días hábiles, se cuenta día por día: del 26-02-2027 al 31-03-2027 hay 35 días, y SIGADE paga eso.

Las correcciones que Claude Code hizo sobre la entrega están en `docs/verificaciones/2026-10-15_lotes-g-h.md`.

## Lo que falta

- **Términos para el resto de los títulos.** Quedan 51 operaciones del lote G sin cargar (duales, Par, BONAR USD con fechas listadas, letras vencidas y antiguas); ver `inbox/lote-g/unresolved.md`.
- **BONCAP TAMAR.** Los términos ya están anclados en la emisión (lote G2). La norma (RC 9, 16, 21, 23 y 36 de 2026; imágenes de la RC 36/2026 en R2) fija VPV = VNO × (1 + TAMAR TEM)^((DÍAS/360) × 12), con TAMAR TEM = [(1 + (TAMAR + MARGEN)/(365/32))^(365/32)]^(1/12) − 1 y TAMAR igual al promedio simple desde 10 días hábiles antes de la emisión hasta 10 días hábiles antes del vencimiento. El motor todavía no implementa esa conversión ni el promedio de todo el plazo. Como el saldo de SIGADE incorpora la TAMAR transcurrida hasta el corte, hará falta además el valor nominal original para aplicar la fórmula exacta. Se resuelve antes de la fase 4, junto con las trayectorias de TAMAR; hasta entonces el pago queda sin monto.
- **Duales.** El módulo de opciones existe, pero `contratos/` todavía no tiene una forma de cargar las dos ramas. Hasta entonces, los duales quedan con la proyección de SIGADE.
- **CER con rezago y días hábiles.** El motor no aplica el rezago de 10 días hábiles del CER ni ajusta las fechas por feriados. Con el escenario congelado no cambia nada; con trayectorias de CER sí, y hay que agregarlo antes de la fase 4.
- **Préstamos de organismos.** Los préstamos a tasa SOFR quedan con la proyección de SIGADE, que congela la tasa al corte. Para la fase 4 hacen falta trayectorias de SOFR.
- **Perímetro.** El inventario cubre la Administración Central. El BCRA y el sector público consolidado se agregan en la fase 3, junto con la eliminación de tenencias intra sector público.
- **Acreedor y residencia.** Para bonos y letras, SIGADE no informa el tenedor; quedan como desconocidos.
