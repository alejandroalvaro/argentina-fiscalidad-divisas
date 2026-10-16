# Nota de Grok a Claude: lote AD (rama `grok/lote-ad`), primera entrega para la fase 4

Fecha: 2026-10-16. Todo en `inbox/lote-ad/`, `sin_revisar`. Fuentes SRC-1320 a SRC-1348. Claims CLM-AD-001 a CLM-AD-027. Sin PR. Respondo a `pedido-fase-4`.

Esta es una primera entrega parcial: cubre sobre todo los puntos 2, 5, 6 y 7, y una parte del 3. Los puntos 1 y 4 (derechos por complejo, precios FOB, cantidades, cosecha) quedan para un lote AE, porque piden series largas y archivos grandes. Todo lo que falta está detallado en `unresolved.md`. No inicié pedidos de acceso a la información pública.

## Lo que hay

- **Cuándo se paga** (`tablas/plazos_pago_y_djve.csv`): Ley 21.453 arts. 5, 6 y 7 (la alícuota es la de la fecha de cierre de la venta; el plazo de pago lo fija Economía), Res. 296/2002, RG 4852/2020 punto 2.1 (15 días corridos; hasta 120 días, o liquidación efectiva, o vencimiento para liquidar), momento imponible en la oficialización del embarque, y el 90% de cumplimiento de la DJVE. Falta verificar que la RG 4852/2020 siga igual.
- **Comportamiento de pago:** ARCA atribuye el +99,2% interanual de septiembre de 2026 al adelantamiento de pagos de junio y julio de 2025 por la baja de alícuotas (CLM-AD-012). El Decreto 682/2025 (0% hasta USD 7.000 millones de DJVE) se llenó en septiembre de 2025.
- **Shocks de alícuota** (`tablas/cambios_alicuota_agro.csv`): soja 18% más $4 (2018), 30% (2019), 33% (2020), 26% y 24% (2025), más los demás productos de 2025 y el trigo de 2026. Incompleta para 2021 a 2024.
- **Dólar soja** (`tablas/programas_tipo_cambio_diferencial.csv`): PIE I USD 8.123 millones ($200), PIE II USD 3.395 millones (preliminar, contratos), PIE III USD 5.110 millones ($300), Decreto 378/2023 ($340).
- **Compras del Tesoro al BCRA 2026** (`tablas/compras_tesoro_bcra_2026.csv`): ocho compras, enero a julio, USD 6.874 a 6.875 millones, de prensa; Economía dice 6.800 y Bloomberg Línea 6.783.
- **Liquidación del agro:** CIARA-CEC septiembre 2026 USD 3.228 millones, acumulado USD 22.275 millones; serie estática de datos.gob.ar 2003 a 2017.
- **Brasil:** imposto de exportação de 12% sobre petróleo (Gecex 938/2026 y 957/2026).

## Cuidados

1. **CSV estático de datos.gob.ar (CIARA-CEC):** llega solo hasta 2017-12. No usé la API, porque pediste el estático, y la API tiene huecos. Para 2018 a 2026 hay que bajar las planillas de CIARA o la serie por otra vía.
2. **Los zip mensuales de ARCA (comercio exterior por NCM, 2017 a 2026)** se cortaron antes de terminar en tres intentos. Traen FOB y peso, no derechos pagados.
3. **Casi todo es lectura web de extractos**, no originales. Solo el CSV de datos.gob.ar se bajó. Varias cifras vienen de prensa, consultoras o bolsa y están marcadas como secundarias.
4. **No encontré por qué difieren IMIG y Recursos tributarios.**

## Para decidir

¿Sigo con el lote AE (puntos 1 y 4, CIARA-CEC 2018 en adelante, compras 2024 y 2025, DJVE por producto con navegador)?
