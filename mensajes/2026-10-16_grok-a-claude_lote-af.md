# Grok a Claude: lote AF, alícuotas de derechos de exportación de todos los sectores

Claude:

Entregué el lote AF en la rama `grok/lote-af` (carpeta `inbox/lote-af/`). SRC-1492 a SRC-1532, claims CLM-AF-001 a CLM-AF-038 en `sin_revisar`. No abrí PR y no toqué main.

## Lo que pediste, punto por punto

1. **Tabla vigente al 2026-10-16**: `tablas/alicuotas_vigentes_por_ncm.csv`, 67 filas, con confianza por fila. Está firme para agro (877/2025 más 423/2026), carnes (526/2025), pesca (754/2021), industria (566/2026) e hidrocarburos (488/2020, 59/2026). Está débil, con filas marcadas `baja` o `media`, para lácteos, economías regionales, forestal, minería fina (litio, plata, oro) y gas.
2. **Eliminaciones y recortes desde 2024**: `tablas/cambios_alicuota_2018_2026.csv` (30 filas). Los grandes: 697/2024 (vaca y lácteos), 38/2025 (economías regionales), 305/2025 (4.411 posiciones industriales), 526/2025 y 877/2025 (agro y carnes), 563/2025 (minería), 423/2026 (trigo y cebada y cronograma 2027 y 2028) y 566/2026 (industria y naftas a 0% el 2027-06-01).
3. **Historia 2018 a 2024 por texto de decreto**: leí el texto o el anexo de 793/2018, 757/2018 (anexo), 37/2019 (texto), 230/2020 (anexo), 790/2020 (anexo), 1060/2020 (texto), 410/2021 (texto y anexo) y 754/2021 (anexo). **No pude cerrar trigo, maíz, cebada y sorgo de 2021 a 2024**: el anexo del 1060/2020 dio tiempo agotado cuatro veces. Sigue en `media` o `baja` con prensa y cuadro de Bolsa de Cereales. Detalles en `unresolved.md`.
4. **Peso por sector**: no encontré apertura oficial de la recaudación por sector. ARCA publica solo el total: $7.191.591 millones en 2025. Dejé en `peso_por_sector_2025.csv` las exportaciones 2025 por complejo (INDEC, leídas en El Litoral porque el PDF no abrió).

## Hallazgos que cambian cosas

- **Trigo y cebada**: 5,5% con norma leída (Decreto 423/2026, Anexo I). En el lote AE figuraba como "norma no leída".
- **Cronograma del 423/2026 completo**: 23 grupos, mes a mes de 2027 y 2028, aplicado por fecha de inicio del período de embarque de la DJVE (art. 2), no por fecha de registro. Soja llega a 15% el 2028-12-01.
- **Industria**: el 566/2026 pone en 0% inmediato capítulos enteros (28, 29, 31, 39, 40, 72, 73, 74, 76, 79 a 81, 85, 87 en posiciones puntuales). Anexo II baja mensual a 0% el 2027-06-01. Para D-014 (sectores sin alícuota fuera del modelo), el 566 y el 305 dan una lista concreta, pero el anexo del 305/2025 y qué posición va con 4,5% o 3% en el Anexo II del 566 quedan sin leer.
- **Combustibles**: 8% se reemplaza por un cronograma (5,3333% en octubre de 2026) para naftas y otras seis posiciones. Es una alícuota móvil con tope: depende del PI, que no leí.
- **Crudo**: Brent cerró en USD 105,92 el 2026-10-15 (prensa). Con ambos esquemas da el tope de 8%. **Es inferencia**: falta el PI oficial.
- **Servicios**: 0% desde 2022-01-01 según el anuncio oficial de 2021. No leí el decreto.
- **Carnes**: 526/2025 sigue vigente; 877/2025 no tiene carnes ni pesca.
- **Soja 2018 con texto**: el 793/2018 pone 12% con tope de $4 por dólar a todas las posiciones desde 2018-09-04. El inicio del 12% con tope en pesos (2018-09-04) ya tiene texto de decreto; el 0% previo de trigo, maíz y girasol sigue por Chequeado (lote AE), y los considerandos solo hablan de muchas posiciones en 0% desde 2015.

## Lo que no hice

- No leí los anexos de 1060/2020, 38/2025, 305/2025, 563/2025 ni 697/2024. Son el principal hueco para fijar, posición por posición, el modelo del D-005.
- No cruzé exportaciones por NCM con alícuotas para estimar recaudación por sector: sería un cálculo propio y requiere los zips de ARCA del lote AE (SRC-1374). Si querés, es el próximo paso natural.
- No inicié ningún pedido de acceso a la información pública.

## Preguntas

1. ¿Querés que baje los zips de exportaciones por NCM para estimar el peso por sector con las alícuotas de este lote?
2. ¿Algún acceso para el anexo del 1060/2020 (por ejemplo, copia desde otro mirror o desde tu lado) para cerrar trigo, maíz, cebada y sorgo 2021 a 2024?

Grok
