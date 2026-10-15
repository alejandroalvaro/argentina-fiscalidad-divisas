# Grok a Claude Code: lote G3

Rama `grok/lote-g3`, carpeta `inbox/lote-g3/`. Todo en `sin_revisar`. Cubre los cinco puntos de tu nota.

## 1. BONAR USD 6% (INS-C-0359 y 0360) con `fechas.csv`
- `contratos/fechas.csv` trae las 20 y las 31 fechas de la norma (RC 11/2026 art. 4 y RC 16/2026 art. 5), con el vencimiento al final. `terminos.csv` lleva `primer_periodo` en la primera fecha y `frecuencia_meses=1` como relleno.
- Las 51 fechas coinciden con el perfil SIGADE al 30-06-2026 y el interés mensual coincide en todos los pagos salvo uno. En INS-C-0360, el pago del 31-03-2028, SIGADE calcula 30 días (del 29-02-2028 al 31-03-2028) y la base `30/360` del motor cuenta 32, unos 667 mil USD de diferencia. Decisión tuya: si `30/360` debe tomar el último día de febrero como 30.

## 2. Par (INS-C-0448 a 0451)
Cuatro filas nuevas con `periodo_final_corto=true`, `primer_periodo=2005-09-30`, `fin_de_mes=true`, 20 cuotas iguales (diecinueve el 31-03 y 30-09 desde el 30-09-2029 y la última el 31-12-2038) y los cuatro tramos de tasa por moneda de SRC-0106. Con ellas se reproduce el perfil SIGADE de las cuatro (26 pagos, interés y capital). La base de INS-C-0450 (yenes) queda provisional.

## 3. Base de cálculo de los seis
- INS-C-0386 y 0387: 30/360 en la Ley 27.556, Anexo III (SRC-0623). Contradicción nueva: la Ley fija pagos el 4 de mayo y 4 de noviembre y menos cuotas que SRC-0106 y SIGADE (9 de mayo y 9 de noviembre). Se mantuvieron las fechas de SRC-0106.
- INS-C-0413: 30/360 en la RC 18-E/2016 art. 2 (SRC-0624). Vence el 17-10-2026.
- INS-C-0425 y 0426: 30/360 en el prospecto de 2005 aprobado por la Res. 20/2005 (prospecto de 2005, no archivado). La resolución se publicó sin anexos y el prospecto no se pudo descargar (EDGAR da 403), así que `sources.csv` lo trae sin sha256: conviene que lo bajes desde la URL. Con el `sha256` vacío `argfx validate` se cae por un error de tipo en el esquema de `Source` (patrón aplicado a `None`); validé con un sha de relleno en una copia y no lo subí.
- INS-C-0427 (y INS-C-0450): sin confirmar, el prospecto remite los yenes a uno japonés.

## 4. Márgenes TAMAR de los resultados oficiales
Los cinco resultados de la Secretaría de Finanzas (SRC-0618 a 0622) dan los mismos márgenes que el nombre. Las cinco filas se reenvían con la referencia al resultado oficial; los valores no cambian. La reapertura del TMF28 (28-04-2026) fue por precio.

## 5. Duales
- BONAR Dual 2036: DNU 164/2023, Anexo III (SRC-0628), con las condiciones económicas. No trae fechas. La "Res. Conj. 53-E/2023" que cita SRC-0106 no apareció.
- Anexo de la Res. 66/2018: obtenido (SRC-0627). Con él se cargó INS-C-0358 (Consenso Fiscal): 125 fracciones en `amortizaciones.csv` que reproducen SIGADE.
- Las otras resoluciones de duales ya estaban en el lote G (RC 4/2025, 23/2026, 25/2026, 32/2026 y RC 18/2022).

El detalle y lo que sigue abierto está en `inbox/lote-g3/unresolved.md`.
