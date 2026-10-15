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

Hay tres tablas, y cada fila cita su fuente (`source_id` y `referencia`).

`terminos.csv`, una fila por instrumento:

| Columna | Contenido |
|---|---|
| `instrument_id` | Identificador de `instruments.csv` (lote C) |
| `deudor`, `tipo_acreedor`, `residencia_tenedor` | `tipo_acreedor`: privado, multilateral, bilateral, BCRA, sector_publico o desconocido. `residencia_tenedor`: residente, no_residente, mixta o desconocida |
| `moneda_cuenta`, `indexacion`, `moneda_liquidacion` | `indexacion`: ninguna, CER, UVA o dolar_linked |
| `estado` | firme o contingente |
| `fecha_corte`, `saldo_corte` | El saldo debe coincidir con `outstanding_principal` de SIGADE. En instrumentos CER se expresa en unidades CER, como en SIGADE (UCP) |
| `fecha_emision`, `primer_periodo`, `vencimiento`, `frecuencia_meses`, `fin_de_mes` | Calendario de períodos. En los capitalizables, cada período es una fecha de capitalización |
| `base` | 30/360, ACT/365, ACT/360 o ACT/ACT |
| `tipo_tasa` | fija (anual), fija_por_periodo (por ejemplo, la TEM), flotante o cero |
| `indice`, `margen`, `multiplicador` | Sólo para tasas flotantes: tasa = índice × multiplicador + margen |
| `capitaliza` | true si el interés se suma al capital y se paga al vencimiento |

`tasas.csv` tiene los escalones de tasa fija (`desde`, `tasa`), y `amortizaciones.csv` las fechas y fracciones del valor nominal original. Sin filas de amortización, el instrumento amortiza al vencimiento.

## Prueba piloto: bonos step up 2030 y 2035 en USD

Los términos de GD30, AL30, GD35 y AL35 (INS-C-0398, 0404, 0399 y 0405) se cargaron desde la estructura financiera de la Oficina Nacional de Crédito Público (SRC-0106, hoja A.1) y el prospecto del canje de 2020 (SRC-0108, p. S-32). El motor reproduce el perfil de SIGADE en las 94 fechas y tipos de flujo, con una diferencia máxima de 0,000001 USD.

La prueba encontró un error en la fuente oficial. En SRC-0106, la fila del Global 2035 USD repite la amortización del 2030 (13 cuotas, la primera del 4%) y su tabla de tasas salta del 09/07/2028 al 09/07/2029. El prospecto, la fila del bono de ley argentina y SIGADE coinciden entre sí: 10 cuotas iguales desde el 09/01/2031, y 4,75% desde julio de 2027 y 5% desde julio de 2028. Los términos usan esa versión y lo anotan en `notas`.

## Controles sobre el conjunto

- La valuación con el escenario congelado reproduce las columnas en USD de SIGADE. En 13 de las 15 monedas la coincidencia es exacta. En la deuda CER, la diferencia es de 1,5 por diez millones, porque SIGADE convierte con un tipo UCP redondeado (1,855623) y el escenario usa el CER publicado (799,2033).
- El principal de base suma 471.689.807.580 USD, frente a un saldo de 471.689.788.348 USD en SIGADE y en el cuadro A.1.1. La diferencia de 19.232 USD es ese mismo redondeo.
- SIGADE escribe la fecha de servicio con año de dos dígitos, y Python lee 69 a 99 como 1969 a 1999. Los vencimientos de 2069 a 2089 quedaban en el pasado. El cargador toma la fecha de las columnas Año, Mes y Día y verifica que coincida con la fecha de servicio.

## Lo que falta

- **Términos para el resto de los títulos.** Con los cuatro bonos piloto, el calendario usa términos propios para 4 de las 753 operaciones; el resto viene de la proyección de SIGADE. La extracción de los 107 bonos y las 18 letras se encarga a Grok (lote G), y cada término se verifica contra SIGADE antes de entrar.
- **Duales.** El módulo de opciones existe, pero `contratos/` todavía no tiene una forma de cargar las dos ramas. Hasta entonces, los duales quedan con la proyección de SIGADE.
- **CER con rezago y días hábiles.** El motor no aplica el rezago de 10 días hábiles del CER ni ajusta las fechas por feriados. Con el escenario congelado no cambia nada; con trayectorias de CER sí, y hay que agregarlo antes de la fase 4.
- **Préstamos de organismos.** Los préstamos a tasa SOFR quedan con la proyección de SIGADE, que congela la tasa al corte. Para la fase 4 hacen falta trayectorias de SOFR.
- **Perímetro.** El inventario cubre la Administración Central. El BCRA y el sector público consolidado se agregan en la fase 3, junto con la eliminación de tenencias intra sector público.
- **Acreedor y residencia.** Para bonos y letras, SIGADE no informa el tenedor; quedan como desconocidos.
