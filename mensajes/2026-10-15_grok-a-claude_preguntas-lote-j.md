# Preguntas abiertas del lote J

El lote J ya está en main. Alejandro pidió dejar estas preguntas a Claude para que las resuelva, o las decida con él. Ninguna está resuelta ni ajustada en los datos. Detalle en `inbox/lote-j/unresolved.md` y en la nota `2026-10-15_grok-a-claude_lote-j.md`.

**Para Claude:**

1. **Saldo de SIGADE del TTD26 (INS-C-0362).** El saldo es 7.498.004.805.716,07 y parece ya capitalizado, pero no hay valor nominal original con fuente oficial. Por eso `factor_saldo` 1,0 y `saldo_es_valor_nominal` false en `contratos/duales.csv` son provisionales. Pregunta: ¿qué representa ese saldo, capital original o capital con intereses capitalizados? Según eso, ajustar o confirmar ambos campos, consultándolo con Alejandro si hace falta.

2. **BONAR Dual 2036 (INS-C-0357).** No encontré norma de emisión ni fechas. El anexo III del DNU 164/2023 fija los términos (dólares, pago en pesos, CER o A3500, 3%, hasta 13 años) pero no emisión ni vencimiento, y la "Res. Conj. 53-E/2023" no apareció. No cargué filas. Pregunta: ¿tienen Claude o Alejandro la norma o el dato de emisión y vencimiento?

3. **Saldo de SIGADE sobre el valor nominal de los BONCAP TAMAR.** Las razones son TML27 1,0000, TMG28 1,0496, TMF28 1,0497, TMF27 0,9930 y TMG27 0,8273, sin explicar. TMG27 queda 17,3% por debajo y TMG28 y TMF28 casi 5% por encima. Tabla en `tablas/vno_boncap_tamar_2026-06-30.csv` (TMF28 es derivado por suma, sin total publicado). Pregunta: ¿se explican por la fecha de congelamiento de SIGADE, por rescates o por la forma de registrar el saldo? Decidir con Alejandro qué cifra usar.

4. **Base de cálculo de la RC 4/2025.** La norma dice 30/360 y usé 30E/360, la convención del repositorio para los BONCAP (CLM-G-023). Pregunta: ¿confirmar 30E/360 también para esta resolución, o pasar a 30/360?

5. **Imagen de la TAMAR TEM en la RC 4/2025.** La del Boletín Oficial es de baja resolución y la leí con la estructura de las RC 23, 25 y 32. Pregunta: ¿se revisa con una versión de mayor resolución o se acepta la lectura actual? (`tablas/ttd26_ramas.csv`)

6. **Pendientes sin cambios.** Siguen sin monto las conversiones con el BCRA de las RC 39, 51, 53 y 60, y falta SIGADE al 2026-09-30. Pregunta: ¿se piden a Alejandro o se esperan fuentes nuevas?
