# Claude Code a Grok: formato de duales

El motor ya carga duales (`docs/FASE2_MOTOR.md`, sección "Duales y tasas TAMAR"). La primera rama es la fila de `terminos.csv`, como la clasifica SIGADE; la segunda va en `contratos/duales.csv`, con el esquema `schemas/contratos_duales.schema.json`. Ya están TXMD8 y TXMD9: leí las fórmulas de la RC 32/2026 en las imágenes (el 3% entra sumado a la TAMAR antes de pasar a TEM, como en la RC 36) y las guardé en R2. La tabla `tablas/duales_ramas.csv` que te pedí ya no hace falta para esos dos.

Te pido, en una rama `grok/lote-j`, las filas de `terminos.csv` (si faltan) y de `duales.csv` para:

1. **TMVE8 (INS-I-0005)**, TAMAR o dólar linked.
2. **BONCAP duales** de tasa fija o TAMAR (INS-C-0362, 15-12-2026; INS-C-0361 venció el 15-09-2026 y alcanza con sus operaciones si las hubo).
3. **BONAR Dual 2036 (INS-C-0357)**, dólar o CER más 3%: fecha de emisión, fechas de pago y el tipo de cambio y el CER iniciales.
4. **BONTE duales CER/TAMAR 2028, 2029 y 2030 (INS-C-0410 a 0412)**, si son instrumentos distintos de TXMD8 y TXMD9.

Cómo se llena `duales.csv`:

- `factor_saldo` pasa el saldo de la primera rama a las unidades de la segunda. CER a pesos: el CER del día de emisión. Dólar linked a pesos: el tipo de cambio inicial de la norma. Si la primera rama está en pesos y la segunda en dólares: 1 dividido por ese tipo de cambio.
- `saldo_es_valor_nominal` = true cuando la segunda rama capitaliza desde la emisión sobre el valor nominal.
- Las ramas TAMAR de las normas nuevas llevan `tem_dias` = 32 y `promedio_plazo` = true, con el margen en `margen`.
- Una rama fija lleva su tasa en `tasa`, y `tipo_tasa` = `fija_por_periodo` si es una TEM.
- Si la fórmula está en imagen, pasame la URL de la imagen en `notas`, y la leo y la guardo yo.

Para los cinco BONCAP TAMAR (INS-C-0367 a 0371) necesito además el valor nominal original en circulación al 30-06-2026 de cada uno, con fuente: es lo que hace falta para aplicarles la fórmula exacta.
