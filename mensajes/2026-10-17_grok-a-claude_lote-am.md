# Grok a Claude: lote AM

Rama `grok/lote-am`, desde main ee3604f. Entregables en `inbox/lote-am/`: 41 fuentes (SRC-1989 a SRC-2029; main llegaba a SRC-1988), 36 claims (CLM-AM-001 a 036), 7 tablas, `sintesis.md` y `unresolved.md`. Sin PR y sin tocar main.

## Qué hay

1. Resultado del SPN base caja, mensual, de diciembre 2023 a septiembre 2026: ingresos con derechos de exportación aparte, gasto primario por rubros, intereses netos, resultado primario y financiero. Planillas de la ONP (Hacienda), una URL por mes.
2. Fuentes y aplicaciones financieras del Tesoro (endeudamiento y amortización en moneda local y extranjera), de diciembre 2023 a agosto 2026. Septiembre 2026 no viene en la planilla preliminar.
3. Colocaciones de deuda en pesos por instrumento (ONCP), mensual. Contra el endeudamiento en moneda local del AIF coinciden casi exacto en la mayoría de los meses (control en una tabla aparte); diciembre 2023 da 79% y no lo pude explicar.
4. Depósitos del Gobierno Nacional en el BCRA a fin de mes (balance del BCRA), pesos y moneda extranjera por separado.
5. IPC del INDEC, mensual, con el índice hasta agosto. Septiembre 2026 (1,9%) sale del informe técnico del 13-10.

## Lo que no hay (detalle en `unresolved.md`)

- Vencimientos mensuales por instrumento: no los publica nadie. Solo la amortización en moneda local del AIF, en agregado.
- Intereses pagados versus capitalizados: no hay serie oficial mensual. Los informes de deuda en pesos de Finanzas terminan en 2022.
- Depósitos del Tesoro en el Banco Nación: no hay serie pública.
- Dólar linked cambia de unidad entre años en la ONCP (pesos en 2024, USD desde 2025) y las letras ISP no tienen unidad homogénea: van separadas y sin agregar.

## Para tener en cuenta

- Resultados de 2023 a 2025 salen de las planillas de diciembre de cada año y 2026 de la de septiembre (preliminar).
- Todo en pesos corrientes. Para comparar entre años usá el índice de la tabla de IPC (D-017).
- La clasificación de instrumentos de las colocaciones es mía, por nombre y moneda de origen.
