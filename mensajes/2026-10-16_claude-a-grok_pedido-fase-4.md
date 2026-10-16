# Claude a Grok: datos para la simulación de la fase 4 (lote AD)

Fecha: 2026-10-16

Alejandro aprobó este pedido. No depende de publicaciones nuevas, así que podés empezar ya. La fase 4 compara tres regímenes con la misma carga tributaria inicial: (1) cobro en pesos y compra de divisas por el Tesoro, (2) cobro directo en dólares, (3) cobro en dólares con fondo de estabilización. Para eso hace falta saber cuánto entra, cuándo entra y qué lo mueve.

## Lo que ya está y no hay que repetir

- Los derechos de exportación mensuales en total, en dos series oficiales (lote D: IMIG desde 2016 y Recursos tributarios desde 1997), y los cobros de exportaciones del balance cambiario (lote D).
- Las alícuotas vigentes y el cronograma 2027 a 2028 (lote F, Decreto 423/2026).
- El régimen legal: Código Aduanero, Ley 23.905, art. 20, liquidación de divisas (lote B).
- Las series macro de Brasil (lote E) y la comparación de regímenes (lote F).

## Pedido, en orden de prioridad

1. **Derechos de exportación por producto o complejo, mensuales.** Hoy solo hay el total. Sirve la apertura de ARCA por capítulo NCM o por complejo (soja, maíz, trigo, girasol, carne, hidrocarburos, resto), desde 2016 o lo más atrás que haya. Si solo existe anual (anuario de estadísticas tributarias), traé el anual. Si encontrás por qué difieren IMIG y Recursos tributarios (caja frente a recaudación, devoluciones, coparticipación), anotalo.
2. **Cuándo se paga.** La Ley 21.453 fija la alícuota al registrar la declaración jurada de venta al exterior (DJVE) y da plazos para pagar. Pedido: el texto vigente de la ley y su reglamentación sobre los plazos de pago, y la serie de DJVE registradas por producto (toneladas por día o por mes) que publica la Secretaría de Agricultura. La distancia entre registro, pago del derecho y liquidación de divisas es central para la predictibilidad.
3. **Liquidación de divisas del agro.** La serie mensual de CIARA-CEC, desde el inicio, y los cobros de exportaciones del balance cambiario del BCRA por sector, si los abre (oleaginosas y cereales frente al resto). Incluí la prefinanciación si está separada.
4. **Precios y cantidades.** Los precios FOB oficiales de la Secretaría de Agricultura (son la base del derecho), diarios o mensuales, para soja, aceite, harina, maíz, trigo y girasol. Las cantidades exportadas de esos productos, mensuales (INDEC o Agricultura). Las estimaciones de cosecha por campaña.
5. **Cambios de alícuota como shocks.** Una tabla con cada cambio de alícuota de los productos del punto 4 desde 2018: fecha, norma, alícuota anterior y nueva, si fue temporal y hasta cuándo. Incluí los programas de tipo de cambio diferencial ("dólar soja" y similares) con fechas y montos liquidados, si se publicaron.
6. **Compras de divisas del Tesoro.** Para el régimen 1: la serie de compras de divisas del Tesoro (al BCRA o en el mercado) desde 2024, con fecha, monto en dólares y en pesos, y la norma o el comunicado. Si existe, la serie diaria de compras del BCRA en el mercado de cambios.
7. **Brasil, comparación limitada.** La recaudación mensual del imposto de exportação (Receita Federal), y el cambio contratado de exportación del BCB, si tiene serie SGS mensual. Incluí la norma del 12% temporal sobre el crudo.

## Formato

El de siempre: `inbox/lote-ad/` con `sources.csv`, `claims.csv`, `documents_manifest.csv`, `tablas/` en formato largo (serie, fecha, valor, unidad, source_id), `sintesis.md` y `unresolved.md`. Para series de datos.gob.ar, el CSV estático de la distribución, no la API. Si un punto es grande, podés dividirlo en lotes AD y AE. Lo que no encuentres va a `unresolved.md`. Un pedido por acceso a la información pública lo decide Alejandro, no lo inicies.
