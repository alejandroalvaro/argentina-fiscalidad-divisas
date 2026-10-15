# Lote G: términos contractuales de BONOS y LETRAS DEL TESORO, pendientes y supuestos

Alcance pedido: 125 operaciones SIGADE clasificadas BONOS (107) y LETRAS DEL TESORO (18) en `inbox/lote-c/instruments.csv`. Resultado: 4 ya cargadas en main (piloto), 70 cargadas en este lote y 51 sin cargar. Todo queda en `sin_revisar`.

## 1. Instrumentos duales (sin formato, no van a terminos.csv)

Cada uno toma el máximo de dos ramas, salvo el BONTE 43,25% que toma el mínimo. Se describen ambas ramas con lo que dice SRC-0106 (hoja B). Las condiciones numéricas completas están en la resolución de emisión, que no se descargó para este lote.

- INS-C-0361 BONCAP DUAL 15-09-2026 (Res. Conj. 4-E/2025, emisión 2025-01-29, íntegro al vencimiento). Rama fija: tasa efectiva mensual capitalizable de 2,17% (por el nombre; "ver resolución"). Rama variable: TAMAR TEM. Se paga la mayor.
- INS-C-0362 BONCAP DUAL 15-12-2026 (Res. Conj. 4-E/2025). Rama fija: 2,14% efectiva mensual (por el nombre). Rama variable: TAMAR TEM. Se paga la mayor.
- INS-C-0408, 0409, 0410, 0411, 0412 BONTE DUAL CER/TAMAR (Res. Conj. 32-E/2026 para 14-12-2029, 15-12-2028 y 28-06-2030; 23-E/2026 para 29-06-2029; 25-E/2026 para 30-06-2028; íntegros al vencimiento). Rama CER: ajuste por CER "ver resolución". Rama variable: TAMAR + 3%. Se paga la mayor. SIGADE los clasifica UCP con tasa cero y reporta solo el principal en unidades CER.
- INS-C-0357 BONAR DUAL 2036 (Res. Conj. 53-E/2023, vto. 2036-09-29, saldo SIGADE en DLK). ONCP: "el máximo valor entre: tipo de cambio de origen ajustado por CER+3% o tipo de cambio al vencimiento +3%". Capital íntegro al vencimiento "al tipo de cambio aplicable". Contradicción de fechas: ONCP dice pagos semestrales los días 20 de marzo y septiembre, el perfil SIGADE los proyecta los días 29 (primer pago 2026-09-29).
- INS-C-0415 BONTE 43,25% o 1%+CER vto. 2027-05-23 (Res. Conj. 18-E/2022). Rama fija: 43,25% nominal anual. Rama CER: 1% más variación del CER. Se paga la menor. ONCP: cuatro cuotas anuales de 25% desde 2024-05-23, intereses semestrales 23 de mayo y noviembre.

- INS-C-0361 BONCAP DUAL/$/15-09-2026 (saldo SIGADE 2,455,829,845 USD)
- INS-C-0362 BONCAP DUAL/$/15-12-2026 (saldo SIGADE 5,055,903,371 USD)
- INS-C-0408 BONTE DUAL CER/TAMAR$/14-12-29 (saldo SIGADE 4,667,053,945 USD)
- INS-C-0409 BONTE DUAL CER/TAMAR$/15-12-28 (saldo SIGADE 1,953,404,865 USD)
- INS-C-0410 BONTE DUAL CER/TAMAR/$/28-6-30 (saldo SIGADE 2,635,039,376 USD)
- INS-C-0411 BONTE DUAL CER/TAMAR/$/29-6-29 (saldo SIGADE 2,911,470,630 USD)
- INS-C-0412 BONTE DUAL CER/TAMAR/$/30-6-28 (saldo SIGADE 1,701,745,920 USD)
- INS-C-0357 BONAR DUAL 2036/DLK/29-09-2036 (saldo SIGADE 640,874,451 USD)
- INS-C-0415 BONTE/$/43,25%/23-05-2027 (saldo SIGADE 93,459,468 USD)

## 2. Contradicciones y errores de fuente (se citan ambas fuentes, se indica la usada)

1. Bono Global USD Step Up 2035 (SRC-0106 hoja A.1 fila 7): repite la amortización del 2030 y la lista de tasas salta el tramo 2028-2029. No se carga aquí porque INS-C-0399 e INS-C-0405 ya están en main con el prospecto (SRC-0108) y la fila de ley argentina (fila 19). Ver CLM-G-001 y CLM-G-002.
2. Global EUR Step Up 2041 (INS-C-0394, hoja A.1 fila 15): el texto dice "09-97-2021". Se leyó 09-07-2021 por la secuencia de tramos. Ver CLM-G-003.
3. Bono CER 2,5% 2031 (INS-C-0388): SRC-0106 hoja B fila 33 dice capital íntegro al vencimiento. La Res. Conj. 40/2022 (SRC-0602) dice diez cuotas semestrales iguales desde 2027-05-30. Se cargó la resolución; SIGADE coincide con ella. Ver CLM-G-004 y CLM-G-005.
4. BONTE USD 6,5% 2029 (INS-C-0422): ONCP dice capital "al tipo de cambio aplicable", SIGADE registra moneda de pago USD. Se cargó moneda de liquidación USD (SIGADE). Falta la Res. Conj. 62-E/2025 para decidir. Ver CLM-G-007.
5. BONAR Dual 2036: fechas de pago 20 (ONCP) frente a 29 (SIGADE). Ver CLM-G-008. No se carga (dual).
6. Discount CER 5,83% 2033 (INS-C-0426): SIGADE no reparte cuotas exactamente iguales y la suma de principal futuro difiere del saldo por 0,09 unidades CER. Ver CLM-G-016.
7. SRC-0106 está fechado al 31-08-2026 y el corte SIGADE es 2026-06-30. Las filas de SRC-0106 posteriores al corte (por ejemplo LECAP 16-10-2026, LELINK 10-05-2027, LECER 29-01-2027, BONAR USD 31-10-2029, BONTE Dual TAMAR o DLK 31-01-2028) no tienen operación en instruments.csv y no se cargaron.

## 3. Sin cargar porque el formato o la fuente no alcanzan

### 3.1 Bonos Par (período final fuera de grilla)
Intereses el 31-mar y 30-sep con último pago el 31-dic-2038, y amortización en 20 cuotas iguales (19 en mar y sep desde 2029-09-30 más una el 2038-12-31). El cargador genera fechas con frecuencia fija desde `primer_periodo` hasta `vencimiento`, así que 2038-12-31 queda fuera de la grilla semestral. Hace falta una regla de período final corto o una lista de fechas.
- INS-C-0448 PAR/$+CER/T.FIJA/2038 (saldo SIGADE 1,050,165,432 USD)
- INS-C-0449 PAR/EUR/T.FIJA/2038 (saldo SIGADE 649,056,664 USD)
- INS-C-0450 PAR/JPY/T.FIJA/2038 (saldo SIGADE 111,491,761 USD)
- INS-C-0451 PAR/U$S/T.FIJA/2038 (saldo SIGADE 35,819,560 USD)

### 3.2 BONAR USD 6% (fechas enumeradas)
La Res. Conj. 11/2026 (SRC-0601) enumera las fechas de pago (31 de marzo, 30 de abril, 29 de mayo, 30 de junio, 31 de julio ... 29 de enero, 26 de febrero ... 29 de octubre de 2027) y no sigue una regla de fin de mes. El perfil SIGADE usa fechas parecidas con ajustes de día hábil. Hace falta un cargador con lista explícita de fechas (por ejemplo `fechas.csv`). El BONAR 2028 (INS-C-0360) corresponde a la Res. Conj. 16/2026, que no se descargó.
- INS-C-0359 BONAR/U$S/6%/29-10-2027 (saldo SIGADE 2,000,370,497 USD)
- INS-C-0360 BONAR/U$S/6%/31-10-2028 (saldo SIGADE 2,000,369,685 USD)

### 3.3 BONAR en pesos Consenso Fiscal 2028 (cuotas no explícitas)
INS-C-0358: SRC-0106 hoja B fila 7 trae 125 cuotas mensuales, tasa 6,72763943919512% y fechas, pero no dice que las cuotas sean iguales ni da su fórmula. El perfil SIGADE muestra cuotas crecientes (344.108.033,38 en 2026-07-31 hasta 404.687.036,05 en 2028-12-31). Las fracciones de amortización no figuran en SRC-0106. Falta la Resolución 66/2018.
- INS-C-0358 BONAR/$/6,72763943%/31-12-2028 (saldo SIGADE 7,558,957 USD)

### 3.4 Letra BCRA 2031
INS-C-0446 (vto. 2031-06-30): no hay fila equivalente en SRC-0106 hoja D (las siete letras listadas vencen entre 2032-04-20 y 2034-01-08). Falta la norma de emisión.
- INS-C-0446 LETRA/U$S/BCRA/30-06-2031 (saldo SIGADE 3,878,320 USD)

### 3.5 Vencidas antes del 31-08-2026 (no figuran en SRC-0106) 
Los vencimientos que informa SIGADE caen en julio y agosto de 2026. Falta la resolución de emisión de cada una.
- INS-C-0623 LECAP/$/TAMAR+5%/31-08-2026 (saldo SIGADE 4,538,040,825 USD)
- INS-C-0629 LETRA/DLK/0%/31-07-2026 (saldo SIGADE 3,098,296,516 USD)
- INS-C-0615 LECAP/$/14-8-2026 (saldo SIGADE 2,909,456,868 USD)
- INS-C-0621 LECAP/$/31-07-26 (saldo SIGADE 2,253,380,654 USD)
- INS-C-0617 LECAP/$/17-7-2026 (saldo SIGADE 1,978,378,104 USD)
- INS-C-0622 LECAP/$/31-08-2026 (saldo SIGADE 1,779,413,495 USD)
- INS-C-0630 LETRA/DLK/0%/31-08-2026 (saldo SIGADE 1,525,556,376 USD)
- INS-C-0626 LETES/$+CER/31-07-2026 (saldo SIGADE 1,094,767,534 USD)

### 3.6 Instrumentos antiguos que SRC-0106 no cubre
Bonos de consolidación (Bocon) distintos del PR17, bonos Global y BONTE del canje de 2005 y anteriores, series PRO(P) y PRE(P) en UCP y el Bono Consolidado 2089 no figuran en las hojas A.1 a OL. Sin prospecto ni norma en el lote, no se completan por analogía con otro bono.
- INS-C-0432 GLOBAL BOND/U$S/11,375%/2017 (saldo SIGADE 5,051,820 USD)
- INS-C-0424 BONTES/U$S/12,125%/2005 (saldo SIGADE 2,904,166 USD)
- INS-C-0352 BOCON PRO.2ºS./U$S/L./10/PRO4 (saldo SIGADE 2,336,593 USD)
- INS-C-0454 PRO4(P) (saldo SIGADE 1,287,175 USD)
- INS-C-0423 BONTES/U$S/11,75%/2006 (saldo SIGADE 911,162 USD)
- INS-C-0354 BOCON PRO.3ºS./U$S/L./07/PRO6 (saldo SIGADE 610,555 USD)
- INS-C-0438 GLOBAL BOND/U$S/9,75%/2027 (saldo SIGADE 536,000 USD)
- INS-C-0389 BONO CONSOLIDADO/$/T.CERO/2089 (saldo SIGADE 493,328 USD)
- INS-C-0431 GLOBAL BOND/U$S/11,375%/2010 (saldo SIGADE 393,000 USD)
- INS-C-0433 GLOBAL BOND/U$S/11,75%/2009 (saldo SIGADE 360,000 USD)
- INS-C-0428 GLOBAL B./U$S/11,375%/2017(P) (saldo SIGADE 205,214 USD)
- INS-C-0436 GLOBAL BOND/U$S/7%-15,5%/2008 (saldo SIGADE 135,650 USD)
- INS-C-0430 GLOBAL BOND/U$S/11%/2006 (saldo SIGADE 134,000 USD)
- INS-C-0452 PRE6(P) (saldo SIGADE 131,187 USD)
- INS-C-0356 BOCON PRO.5ºS./U$S/L./07/PRO10 (saldo SIGADE 100,924 USD)
- INS-C-0437 GLOBAL BOND/U$S/8,375%/2003 (saldo SIGADE 100,000 USD)
- INS-C-0434 GLOBAL BOND/U$S/11,75%/2015 (saldo SIGADE 72,000 USD)
- INS-C-0435 GLOBAL BOND/U$S/12,375%/2012 (saldo SIGADE 67,000 USD)
- INS-C-0453 PRO2(P) (saldo SIGADE 44,399 USD)
- INS-C-0351 BOCON PRO.1ºS./U$S/L./07/PRO2 (saldo SIGADE 25,261 USD)
- INS-C-0429 GLOBAL BOND/U$S/11%/2005 (saldo SIGADE 25,000 USD)
- INS-C-0439 GLOBAL/U$S/7%-15,5%/2008(P) (saldo SIGADE 18,297 USD)
- INS-C-0455 PRO6(P) (saldo SIGADE 12,746 USD)
- INS-C-0353 BOCON PRO.3ºS./$/C.A./07/PRO5 (saldo SIGADE 40 USD)
- INS-C-0350 BOCON PRO.1ºS./$/C.A./07/PRO1 (saldo SIGADE 30 USD)
- INS-C-0355 BOCON PRO.5°S./$/C.A./07/PRO9 (saldo SIGADE 22 USD)

## 4. Supuestos incluidos en lo cargado (revisar antes de usar)

1. **Base de cálculo no indicada en SRC-0106** para INS-C-0386, 0387, 0425, 0426, 0427, 0413, 0414, 0422: se cargó 30/360 porque el perfil SIGADE la reproduce al céntimo (comparación contra SIGADE, no contra el texto). Pendiente de confirmar en la norma de emisión de cada uno. INS-C-0388 sí tiene la base en la resolución.
2. **Tasas flotantes** (TAMAR, BADLAR, rendimiento de reservas BCRA): no se carga ningún valor de tasa. La base (ACT/365 o ACT/360) es provisional porque SRC-0106 no la indica; no altera el capital. Los días de pago trimestrales de los BONTE BADLAR (INS-C-0416) se anclaron al vencimiento porque SRC-0106 solo dice "trimestralmente". Para los BONCAP TAMAR el margen se cargó como fracción anual (0,065 por TAMAR+6,5%) y no se sabe si es sobre TNA o TEM.
3. **Tope de las Letras BCRA** (LIBOR o SOFR TERM menos un punto): el formato no tiene campo de tope; queda en `notas`.
4. **BONCAP y LECAP a tasa efectiva mensual** (INS-C-0363, 0364, 0365, 0366, 0614, 0616, 0618, 0619, 0620): períodos mensuales anclados hacia atrás desde el vencimiento (SRC-0106 no da el día de capitalización). El primer período corto cuenta como una tasa mensual completa. No se sabe si el plazo se capitaliza en meses enteros o por días/30.
5. **SIGADE no proyecta la capitalización**: el principal SIGADE al vencimiento es igual al saldo al corte con interés cero (CLM-G-011). El motor sí proyecta la capitalización, así que la comparación fecha por fecha da diferencias de 6% a 36% en esos nueve instrumentos. No se resuelve cuál es el saldo correcto; se necesita saber si el saldo SIGADE incluye el devengado hasta el corte.
6. **Instrumentos CER** (UCP): saldo en unidades CER como en SIGADE, sin retraso CER aplicado.
7. **Hoja B, BONTE USD 6,5% y 6%**: moneda de pago tomada de la tabla de saldos SIGADE.
8. **Tramos anteriores a 2013 de Discount y Cuasipar** (con capitalización parcial) no se cargaron; solo el tramo en efectivo posterior, que es el que afecta flujos desde el corte.

## 5. Verificación realizada

- `saldo_corte` copiado tal cual de `outstanding_principal` en `instruments.csv`.
- Las fracciones de cada instrumento suman 1 y las fechas de amortización caen en la grilla de períodos.
- No se corrió `make validate-grok` ni el motor del repositorio porque no hubo acceso al clon en el Mac (equipo sin conexión). En su lugar se reimplementó la lógica de `src/argfx/contracts` (engine.py, terms.py, schedule.py, daycount.py y sigade.py leídos desde main) y se comparó cada instrumento contra el perfil SIGADE fecha por fecha. Resultado en `verificacion_motor.csv`. Hay que repetirlo con el motor real al integrar.

## Actualización 2026-10-15 (capitalización y pendientes)

Estado de los pendientes del lote, todo en `sin_revisar`:

1. Fechas explícitas: `contratos/fechas_explicitas.csv` (51 filas) cubre INS-C-0359 (RC 11/2026, art. 4) e INS-C-0360 (RC 16/2026, art. 5, con el 29-02-2028). El cargador de main no lee listas de fechas: decisión de formato pendiente. Los Par con período final corto fuera de la grilla siguen sin cubrir.
2. Resoluciones de emisión de los duales: obtenidas la RC 4/2025 (BONCAP Dual 15-09-2026 y 15-12-2026), la RC 23/2026, la RC 25/2026 y la RC 32/2026 (BONTE Dual CER/TAMAR 2028, 2029 y 2030) y la RC 18/2022 (BONTE 23-05-2027, menor entre tasa fija y 1% más CER). Sin encontrar: BONAR Dual 2036 (SRC-0106 cita "Res. Conj. 53-E/2023"; la RC 53/2023 que aparece publicada trata otra materia). Res. 66/2018 obtenida, pero su Anexo IF-2018-12038106-APN-SECF#MF no está en el texto, así que faltan las fracciones de las 125 cuotas.
3. Tope de las letras BCRA: `contratos/topes_propuesta.csv` es una propuesta de formato (7 filas); el motor no la carga.
4. Base 30/360: confirmada por norma en RC 4/2025, 23/2026, 24/2025, 25/2026, 62/2025 (INS-C-0422), 11/2026, 16/2026, 40/2022 y Res. 66/2018. De los ocho instrumentos sin base en SRC-0106 quedan sin confirmar en norma seis: INS-C-0386, 0387, 0413, 0425, 0426 y 0427. INS-C-0414 e INS-C-0422 quedan confirmados.
5. Contradicción señalada: SRC-0106 describe el BONTE USD 6,5% 2029 con pago "al tipo de cambio aplicable" (CLM-G-007); la RC 62/2025 dice pago en dólares (CLM-G-033).
6. Saldo SIGADE y capitalización: el saldo incluye la capitalización devengada al 30-06-2026 (CLM-G-022). La convención del lote para el exponente (períodos mensuales desde el vencimiento hacia atrás) difiere de la fórmula legal con exponente DÍAS/30 y del coeficiente de SIGADE (meses enteros desde la emisión).
