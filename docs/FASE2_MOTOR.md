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
- En los instrumentos CER o UVA, el valor nominal publicado está en pesos y el saldo en unidades del índice (D-010). La columna `indice_inicial` de `terminos.csv` hace la conversión, y el cargador rechaza operaciones sobre esos instrumentos si falta. Es el CER del día de emisión, porque así arma SIGADE sus unidades: el valor nominal en circulación dividido por el saldo de SIGADE da 736,0 en TZXM8 (CER del 01-04-2026: 735,986), 668,234 en TZXY7 (668,234) y 788,979 en TXMD8 (788,979). Las normas ajustan por el CER de diez días hábiles antes de la emisión y del vencimiento; ver "Rezagos y días hábiles".
- Algunas conversiones con el BCRA no publican el valor nominal efectivo. Se cargan montos derivados de circulaciones y porcentajes oficiales cuando el rango de incertidumbre es estrecho (lote I3, `tablas/derivaciones_conversiones_bcra.csv`), con "DERIVADO" en `referencia`. Las que no se pueden derivar quedan afuera, y el saldo de los instrumentos afectados queda sobrestimado hasta el próximo corte de SIGADE.
- Si una operación deja el saldo negativo, el motor se detiene: falta alguna operación anterior.
- Rige la fecha de liquidación: entra toda operación liquidada después del corte, porque el saldo de SIGADE ya incluye lo liquidado hasta ese día.
- `comparacion_sigade.csv` marca con `con_operaciones` los instrumentos que tienen operaciones posteriores al corte, en los que la diferencia con SIGADE es esperable.

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

## Duales y tasas TAMAR

Un dual paga, al vencimiento, la mayor de dos ramas. La primera es la fila de `terminos.csv`, cargada como la clasifica SIGADE; la segunda va en `contratos/duales.csv`, una fila por instrumento, con su moneda, indexación, tasa, capitalización, base y calendario. El saldo de la segunda rama es el de la primera por `factor_saldo`: en un dual CER/TAMAR, las unidades CER de SIGADE por el CER del día de emisión dan el valor nominal en pesos. Con `saldo_es_valor_nominal`, el motor capitaliza ese valor nominal desde la emisión. Las operaciones posteriores al corte pasan a la segunda rama con el mismo factor.

Las dos ramas se valúan en la moneda de pago y se elige la mayor. Si a una le falta trayectoria (TAMAR, por ejemplo, en el escenario congelado de SIGADE), el pago queda sin monto y `lower_bound` lleva el de la primera rama: el dual paga por lo menos eso.

Las tasas TAMAR de las normas recientes se cargan como flotantes con `tem_dias` = 32 y `promedio_plazo` = true. El motor convierte la tasa anual (índice más margen) en TEM = [(1 + r/(365/32))^(365/32)]^(1/12) − 1, la aplica por mes con el período final corto en 30/360 y promedia la TAMAR desde la emisión hasta el vencimiento. Así reproduce VPV = VNO × (1 + TAMAR TEM)^((DÍAS/360) × 12) de la RC 32/2026 (fórmulas en imagen guardadas en R2 bajo SRC-0910). El rezago de diez días hábiles está en "Rezagos y días hábiles".

Cargados: TXMD8 y TXMD9 (INS-C-0409 e INS-C-0408), CER o TAMAR más 3%, y TMVE8 (INS-I-0005), dólar linked o el valor nominal en USD al tipo de cambio inicial (A3500 del 28-07-2026, 1.499,8387) capitalizado a TAMAR TEM sin margen (RC 46/2026 art. 3). Con el lote J se sumaron los BONTE duales CER/TAMAR más 3% INS-C-0410 (RC 32 art. 5), INS-C-0411 (TXMJ9, RC 23 art. 3) e INS-C-0412 (RC 25 art. 1), y el TTD26 (INS-C-0362, RC 4/2025), tasa fija 2,14% mensual o TAMAR sin margen. Con el escenario congelado de SIGADE quedan sin monto, con piso en la primera rama.

### Saldo en valor nominal original

`terminos.csv` acepta `saldo_es_valor_nominal`: con `true`, `saldo_corte` es el VNO en circulación al corte y el motor capitaliza desde la emisión, como la fórmula legal. Así se cargan los BONCAP TAMAR con VNO publicado o sumado de licitaciones: TML27 (INS-C-0367), TMF28 (INS-C-0369) y TMG28 (INS-C-0371).

SIGADE capitaliza los BONCAP TAMAR con la TAMAR TEM del promedio de la TAMAR de bancos privados (BCRA, variable 44, SRC-0944) desde diez días hábiles antes de la emisión hasta diez días hábiles antes del último aniversario, con el margen dentro de la TEM. Con ese método, el saldo de SIGADE sobre el VNO publicado da 1,0496 en TMG28 y TMF28, lo mismo que el cálculo. En TMG27 (INS-C-0368) y TMF27 (INS-C-0370) el saldo de SIGADE corresponde a unos 413.000 y 486.000 millones de VNO menos que lo publicado. Ahí falta una operación (un rescate o una conversión antes del corte), así que esos dos siguen con el saldo de SIGADE, que el motor capitaliza desde el último aniversario.

Con el lote K, el TTD26 se cargó con el VNO de la cadena publicada (emisión, reapertura y rescate): 4.624.063,84 millones. Antes se había derivado con el mismo método, así: el saldo de SIGADE (7.498.004.805.716,07) dividido por (1 + TAMAR TEM)^17 = 1,62330 da 4.618.994 millones, que es DERIVADO. Según la ventana del promedio, el VNO va de 4.603.055 a 4.641.540 millones. Sumado a los 4.576.957 millones rescatados en la conversión del 28-04-2026, da 9,196 billones antes de la conversión. La rama TAMAR ya acumulaba 1,6233 por peso de VNO al 29-06-2026, por encima del 1,61144 que paga la rama fija al vencimiento: con TAMAR positiva, el TTD26 paga la rama TAMAR. La rama fija del motor queda 0,07% por encima de la fórmula legal, porque cuenta el período del 29-01 al 28-02-2025 como un mes entero y la ley cuenta 29 días; como esa rama no es la que se paga, se deja así.

## Rezagos y días hábiles

Las normas del CER y de la TAMAR trabajan con diez días hábiles de rezago. El CER ajusta entre el décimo día hábil anterior a la emisión y el décimo día hábil anterior a cada pago. La TAMAR se promedia, en forma aritmética simple sobre las tasas publicadas, desde diez días hábiles antes de la emisión hasta diez días hábiles antes del vencimiento.

**Calendario (`habiles.py`).** Hasta el último dato observado, un día es hábil si el BCRA publicó la Com. A 3500 ese día (`series/bcra_a3500.csv`, SRC-1900). Esa serie ya incluye los feriados, los días no laborables decretados y los inhábiles bancarios (6 de noviembre, 24 y 31 de diciembre). Después rige la regla de la Ley 27.399: feriados fijos, Carnaval, Jueves y Viernes Santo, trasladables al lunes según el art. 6 e inhábiles bancarios. A eso se suman los días decretados que ya se conocen (`series/feriados_decretados.csv`: el 7-12-2026, Res. JGM 164/2025, SRC-1903). Entre 2024 y 2026 la regla nunca marca inhábil un día hábil observado; solo le faltan los días puente decretados.

**CER.** Con `rezago_habiles` en `terminos.csv`, el flujo lleva `index_date`, el décimo día hábil anterior al pago, y la valuación usa el CER de esa fecha. Las unidades de SIGADE son valor nominal sobre el CER del día de emisión (`indice_inicial`), y la norma usa como base el CER de diez días hábiles antes (`indice_base`). Por eso el motor multiplica el saldo por `indice_inicial / indice_base` y convierte las operaciones con `indice_base`. Así, el pago es VN × CER(pago − 10) / CER(emisión − 10). La convención de SIGADE está verificada en TZXY7, TZXM8, TXMD8, TXMD9, los BONTE duales 2028 a 2030 y, con el lote K, en once BONCER y LETES CER más (INS-C-0372, 0374 a 0378, 0381 a 0383, 0624 y 0625: las unidades por el CER de emisión dan el VNO publicado con diferencia menor a 1 por millón). El rezago está cargado en todos ellos y en la LECER X29E7 (INS-I-0007). Siguen con la convención de SIGADE, sin rezago, TZXD7, TZX27 y TZX28 (INS-C-0373, 0379 y 0380, cuyas unidades no cierran con lo emitido) y los BONCER con cupón y los bonos CER anteriores a 2024.

**TAMAR.** Con `rezago_habiles` en la fila de tasa flotante (en `terminos.csv` o en `duales.csv`), la ventana se corre diez días hábiles y el promedio es la media simple de los días hábiles con las dos puntas incluidas. Se cargó en los cinco BONCAP TAMAR y en las ramas TAMAR de los siete duales (TMVE8 incluido: la RC 46/2026 usa la misma ventana).

**Escenario.** `argfx calendario` agrega al escenario congelado de SIGADE el CER y la TAMAR observados antes del corte (`series/`), porque las ventanas con rezago empiezan antes del corte. Desde el corte, el CER sigue en el valor de SIGADE y la TAMAR queda sin trayectoria, como antes. Con el CER congelado, el rezago al pagar no cambia nada y solo actúa el cambio de base: los CER con rezago pagan entre 1% y 4,6% más que la proyección de SIGADE, según cuánto subió el CER en las dos semanas previas a la emisión (4,6% en TZXM7, emitido en mayo de 2024). Por eso dejan de coincidir con SIGADE: es una diferencia contractual, no un error.

## Lo que falta

- **Términos para el resto de los títulos.** Quedan 51 operaciones del lote G sin cargar (duales, Par, BONAR USD con fechas listadas, letras vencidas y antiguas); ver `inbox/lote-g/unresolved.md`.
- **BONCAP TAMAR TMG27.** Sigue sobre el saldo de SIGADE. TMF27 pasó a la fórmula exacta con el VNO publicado en septiembre (3.906.522 millones), 485.000 menos que lo emitido, sin operación publicada que lo explique; en TMG27 falta un dato equivalente.
- **BONAR Dual 2036.** Cargado con el lote K (rama dólar linked en `terminos.csv`, rama CER en `duales.csv`, ambas al 3%). La RC 53/2023 no apareció: la fecha de emisión (2023-09-29, la de la estructura de ONCP y SIGADE, contra 2023-10-20 de las colocaciones) mueve la rama CER 7%, y no está confirmado si el máximo rige servicio por servicio, como dice ONCP, o sobre el total, como lo resuelve el motor.
- **Rezago en los CER restantes.** Falta verificar las unidades de SIGADE de TZXD7, TZX27 y TZX28 (posibles rescates en la conversión con el BCRA de la RC 31/2026) y de los bonos CER anteriores (BONCER con cupón 2026 a 2031, Discount, Par y Cuasipar). Hasta entonces siguen con la convención de SIGADE. Tampoco tienen rezago el A3500 de los dólar linked ni la BADLAR de los BONTE. Las fechas de pago no se corren por feriados.
- **Préstamos de organismos.** Los préstamos a tasa SOFR quedan con la proyección de SIGADE, que congela la tasa al corte. Para la fase 4 hacen falta trayectorias de SOFR.
- **Perímetro.** El inventario cubre la Administración Central. El BCRA y el sector público consolidado se agregan en la fase 3, junto con la eliminación de tenencias intra sector público.
- **Acreedor y residencia.** Para bonos y letras, SIGADE no informa el tenedor; quedan como desconocidos.
