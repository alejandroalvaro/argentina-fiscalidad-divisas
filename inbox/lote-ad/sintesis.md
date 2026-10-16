# Síntesis, lote AD (datos para la fase 4), primera entrega

Fecha: 2026-10-16. Todo `sin_revisar`. Este es un primer paso: cubre el calendario del pago, las reglas de alícuota, la liquidación reciente, los programas de tipo de cambio diferencial, las compras del Tesoro en 2026 y la norma de Brasil. Las series mensuales largas (derechos por complejo, precios y cantidades, CIARA-CEC 2018 en adelante) quedan para un lote AE.

## 1. Tres fechas distintas para un mismo dólar de exportación
- **Registro de la DJVE.** Fija la alícuota: la Ley 21.453 (arts. 6 y 7) aplica el régimen vigente a la fecha de cierre de cada venta, con independencia de cuándo ingresen las divisas (CLM-AD-004). La DJVE tiene un período de embarque; en el listado del 15/10/2026 aparecen opciones de 30 y 360 (CLM-AD-009). Se da por cumplida con el 90% de la cantidad declarada (CLM-AD-005).
- **Oficialización del embarque.** Es el momento imponible (CLM-AD-008). El pago puede ser anticipado, o con plazo de espera y garantía: 15 días corridos desde el libramiento en el caso general, y en el segundo párrafo hasta el menor entre 120 días, la liquidación efectiva y el vencimiento para liquidar (CLM-AD-007; vigencia sin verificar).
- **Liquidación de divisas.** La fija la normativa del BCRA, que no leí. El Decreto 38/2025 ató la alícuota diferencial a liquidar el 95% de las divisas dentro de 15 días hábiles de la DJVE (CLM-AD-010).

Para la fase 4 esto importa porque el derecho puede cobrarse antes, durante o después de que el dólar entre al mercado de cambios, y en esos tres regímenes la distancia cambia quién tiene los dólares en cada momento.

## 2. El comportamiento de pago responde a la expectativa de alícuota
ARCA explica el +99,2% interanual de septiembre de 2026 ($1.121.551 millones) por el adelantamiento de derechos en junio y julio de 2025, cuando se esperaba la baja, que dejó menos pagos en los meses siguientes (CLM-AD-012). Y explica junio de 2026 (-27,8%) por la alta base de junio de 2025, último mes de la baja temporal del Decreto 38/2025 (CLM-AD-013). El Decreto 682/2025 abrió una ventana de 0% con tope de USD 7.000 millones de DJVE, que se llenó en septiembre de 2025 (CLM-AD-011); CIARA-CEC y Clarín citan USD 7.100 millones liquidados ese mes (CLM-AD-003).

## 3. Alícuotas y shocks (tabla `cambios_alicuota_agro.csv`)
Soja: 18% más $4 por USD (2018), 30% (diciembre de 2019), 33% (marzo de 2020), 26% y luego 24% con los decretos de 2025 (CLM-AD-014 a 017). A diciembre de 2025: aceite y pellets 22,5%, trigo y cebada 7,5%, maíz y sorgo 8,5%, girasol 4,5%; el trigo pasó a 5,5% en junio de 2026. La tabla está incompleta para 2021 a 2024 (ver `unresolved.md`).

## 4. Dólar soja y similares (tabla `programas_tipo_cambio_diferencial.csv`)
PIE I: $200 por USD, septiembre de 2022, USD 8.123 millones. PIE II: contratos por USD 3.395 millones (preliminar). PIE III: $300 por USD, abril a junio de 2023, USD 5.110 millones. Decreto 378/2023: $340 por USD para economías regionales hasta el 31/8/2023. Según una nota, el BCRA retuvo alrededor de 65%, 75% y 30% de lo liquidado en cada edición, lo que sugiere un patrón: cuanto más prolongado el incentivo, menos reservas netas por dólar liquidado. No lo afirmo; está en una sola fuente periodística.

## 5. Compras del Tesoro (2026)
Ocho compras al BCRA entre enero y julio por USD 6.874 a 6.875 millones, frente a una meta de 6.700 (CLM-AD-023). El programa financiero prevé 4.900 en 2027 (CLM-AD-024). Es la única referencia para el régimen 1; falta la serie oficial y 2024 a 2025.

## 6. Brasil
El imposto de exportação sobre petróleo bruto al 12% es temporal: 60 días desde el 10/7/2026, prorrogado 60 días desde el 8/9/2026 (CLM-AD-025 y 026). Es un ejemplo de derecho a la exportación como herramienta temporal con prórroga por plazo fijo.

## Qué no está
Ver `unresolved.md`: derechos por complejo, DJVE por producto, CIARA-CEC de 2018 en adelante, precios FOB, cantidades, cosecha, compras 2024 y 2025, serie diaria del BCRA y recaudación de Brasil.
