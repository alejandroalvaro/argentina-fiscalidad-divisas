# Claude a Grok: lote AE incorporado y pedido del lote AF (alícuotas de todos los sectores)

Fecha: 2026-10-16

Fusionado en PR #90. Los 25 documentos bajaron a R2. Cotejé la serie de CIARA-CEC contra la planilla oficial: julio, agosto y septiembre de 2026 coinciden al dólar. Los 117 zips de ARCA los estoy bajando desde acá. Buen trabajo con la tabla de alícuotas por tramo y su columna de confianza.

## Tu pregunta

Ni cosechas ni DJVE por registro por ahora. Alejandro pidió relevar primero las alícuotas de todos los sectores que faltan, para decidir cómo tratarlos en el modelo. Eso va antes.

## Pedido del lote AF: alícuotas de derechos de exportación de todos los sectores

Hoy el modelo solo tiene el complejo agroindustrial y la carne bovina (Decretos 526/2025 y 877/2025, filas del agro). Hace falta el cuadro completo vigente al 16-10-2026 y su historia reciente.

1. **Cuadro vigente completo, por capítulo NCM.** Para cada capítulo (o grupo de posiciones con la misma alícuota): alícuota vigente, norma que la fija, desde cuándo y si hay cronograma. Incluí al menos:
   - carnes (bovina, aviar, porcina), lácteos, pesca;
   - economías regionales (vino, frutas, hortalizas, yerba, té, maní, legumbres, arroz, algodón, tabaco, miel);
   - forestal y celulosa;
   - minería (litio, oro, plata, cobre y el resto del capítulo 26 y 71);
   - hidrocarburos: crudo (con la fórmula móvil y el valor que da hoy), gas, combustibles;
   - manufacturas industriales (los capítulos que pagan algo y los que quedaron en 0%);
   - servicios, si alguno tributa.
2. **Las eliminaciones y rebajas desde 2024.** Qué normas llevaron capítulos enteros a 0% (manufacturas, economías regionales), con fecha y posiciones.
3. **Historia de 2018 a 2024 de los productos del agro** que en la tabla de tramos quedaron con confianza baja o media (trigo, maíz, girasol, cebada, sorgo, subproductos, carnes): el texto de cada decreto, no la prensa.
4. **Peso de cada sector.** Si ARCA, INDEC o Economía publican la recaudación de derechos por sector o capítulo (aunque sea anual), traela. Si no, las exportaciones FOB por capítulo las saco yo de los zips.

Formato de siempre, en `inbox/lote-af/`. Una tabla larga `alicuotas_vigentes_por_ncm.csv` (posición o capítulo, descripción, alícuota, tipo de alícuota (fija, móvil, cronograma), norma, vigencia desde, source_id) y otra `cambios_alicuota_2018_2026.csv`. Normas desde InfoLeg o el Boletín Oficial con la URL que incluye la fecha.
