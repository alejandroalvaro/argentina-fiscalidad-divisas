# Sin resolver, lote AD

Fecha de acceso: 2026-10-16. Este lote cubre sobre todo los puntos 2, 3 (parcial), 5, 6 y 7 del pedido de la fase 4. Los puntos 1 y 4 en serie mensual quedan para un lote AE, porque requieren bajar y procesar archivos grandes de ARCA, INDEC y Agricultura.

## Punto 1. Derechos de exportación por producto o complejo, mensuales
1. **No encontré una serie oficial de derechos pagados por producto o complejo.** La búsqueda no devolvió ningún conjunto de datos.gob.ar con esa apertura. Los informes mensuales de ARCA traen el total y explican cada mes con alícuotas y precios (cargados solo para abril, junio y septiembre de 2026).
2. **Los archivos mensuales de comercio exterior de ARCA** (`download.aspx?filename=AAAAMM.zip`, enero de 2017 a septiembre de 2026) traen FOB, peso y posición NCM, no derechos pagados. El zip de 2026-09 se cortó antes de completarse en tres intentos (85 MB recibidos, archivo inválido). Con FOB por posición y la alícuota vigente se podría estimar el derecho devengado por complejo, y esa estimación no sería la recaudación. Para un lote AE.
3. **Diferencia entre IMIG y Recursos tributarios:** no encontré documento que la explique. Lo único leído son las razones de ARCA para el salto de septiembre 2026 (CLM-AD-012), que son de comportamiento de pago, no de definición de series. Falta la nota metodológica de cada serie.
4. **Anuario de estadísticas tributarias de ARCA** (posible apertura anual por producto): no lo busqué en este lote.

## Punto 2. Cuándo se paga
5. **Serie diaria o mensual de DJVE registradas por producto (Agricultura):** la página de estadísticas existe ("Registro de DJVE para granos y subproductos al 15 de octubre de 2026") pero el lector web no devolvió las tablas; el listado diario trae registros individuales. Alphacast tiene una serie diaria acumulada desde 2011-01-03 a 2026-10-13 en toneladas, pero es un agregador (plan "Professional"), no la fuente. Hace falta navegador para bajar el listado o la estadística.
6. **Texto vigente de la reglamentación:** leí los extractos de la Ley 21.453 (arts. 5, 6, 7 y el 90% de cumplimiento), Res. 296/2002 y RG 4852/2020 punto 2.1. No verifiqué que la RG 4852/2020 siga sin modificaciones en 2026, ni el número del artículo del 90%, ni el plazo de 90% del Decreto 682/2025 (liquidar en tres días hábiles, solo en una síntesis de búsqueda).
7. **Plazos para liquidar divisas por posición** (el "plazo del ítem de mayor valor FOB"): no los cargué; están en la normativa del BCRA (Comunicación A), no leída.

## Punto 3. Liquidación de divisas
8. **CIARA-CEC mensual:** solo está la serie estática de datos.gob.ar hasta 2017-12 (180 meses). La distribución API de la misma serie llega a 2026-09 pero con huecos (julio y octubre de 2025, febrero a abril de 2026 vacíos) y la consigna era usar el CSV estático, así que no la cargué. Falta 2018 a agosto de 2026, que está en las planillas mensuales de la web de CIARA (`ciaracec.com.ar/ciara/Información/Liquidación Mensual`, enlaces a archivos no leídos).
9. **Cobros de exportaciones del balance cambiario del BCRA por sector, y prefinanciación separada:** no los busqué en este lote.

## Punto 4. Precios, cantidades, cosecha
10. **Precios FOB oficiales de Agricultura** (base del derecho) para soja, aceite, harina, maíz, trigo y girasol: sin buscar.
11. **Cantidades exportadas mensuales** (INDEC o Agricultura) y **estimaciones de cosecha por campaña:** sin buscar. Las cantidades saldrían de los zip de ARCA del punto 2 de este archivo.

## Punto 5. Shocks de alícuota
12. **La tabla de cambios de alícuota está incompleta:**
    - Falta la alícuota anterior del Decreto 793/2018 y el detalle de maíz, trigo, girasol, cebada y carnes en 2018 y 2019.
    - Faltan los niveles de 2021 a 2024 en un decreto: solo están en la síntesis de una búsqueda secundaria (33% poroto, 31% subproductos). Los cambios de 2022 y 2023 no se cargaron.
    - Faltan los decretos de 2024 (697/2024 aparece citado en el 526/2025) y de enero a julio de 2025 con detalle por producto.
    - Las cifras de los decretos 526/2025 y 877/2025 por posición están en anexos que no leí.
13. **Programa de Incremento Exportador I, II y III:** las cifras vienen de prensa y de un comunicado de Agricultura con datos preliminares. El PIE II son contratos de venta, no divisas liquidadas, y no leí el tipo de cambio de su decreto. Las cifras de dólar soja mensuales liquidadas por CIARA-CEC no están cargadas.
14. **Dólar soja de 2020 y otros regímenes** (por ejemplo desgravaciones del Decreto 280/2019): sin buscar.

## Punto 6. Compras de divisas del Tesoro
15. **Solo hay 2026 y de prensa.** Falta 2024 y 2025, la fuente oficial (Tesorería, comunicados de Economía, BCRA) y los montos en pesos de cada compra. La resolución de recompra de letras del BCRA (Res. 27/2026, $18,4 billones a $1.391,3141 por dólar) apareció en la búsqueda, pero no la cargué porque es de otro lote.
16. **Totales que no coinciden:** 6.875 (cuadro de Machado), 6.800 (Economía) y 6.783 (Bloomberg Línea). La suma de las ocho compras da 6.874.
17. **Compras diarias del BCRA en el mercado:** solo el acumulado anual citado por prensa (12.350 millones de USD al 8 de julio). Falta la serie diaria oficial.

## Punto 7. Brasil
18. **Recaudación mensual de imposto de exportação (Receita Federal) y cambio contratado de exportación del BCB (SGS):** sin buscar. Solo cargué la norma del 12% sobre petróleo (Gecex 938/2026 y 957/2026). No leí cuánto recaudó esa alícuota ni la base legal general del imposto de exportação.

## Otros
19. **Fuentes secundarias:** CLM-AD-003, 014, 017, 019, 021, 023 y 024 usan prensa, consultoras o bolsa. Hay que contrastarlas con el decreto o el comunicado oficial.
20. **Cuidado con el límite de la lectura web:** ninguna fuente se descargó como original, salvo el CSV de datos.gob.ar. Los `.txt` de `fuentes/` son extractos de lo que devolvió la herramienta de lectura.
