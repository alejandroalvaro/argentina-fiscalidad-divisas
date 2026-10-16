# Síntesis, lote AE

Fecha de acceso: 2026-10-16. Fuentes SRC-1349 a SRC-1491. Claims CLM-AE-001 a CLM-AE-030, todos `sin_revisar`. Responde a `lote-ad-incorporado`.

## 1. Derechos por complejo
No hay serie oficial de derechos pagados por producto. Se arma con dos insumos:
- **Alícuotas por posición** (`tablas/alicuotas_derecho_exportacion_por_ncm_decretos_526_y_877_2025.csv`): anexos de los decretos 526/2025 y 877/2025, filas del agro.
- **Alícuotas por tramo 2015 a 2026** (`tablas/alicuotas_agro_por_tramos_2015_2026.csv`), con columna de confianza. La soja está bien cubierta (33% de 2021 a 2025, 26% y 24% después). Trigo, maíz y girasol de 2020 a 2024 no tienen decreto leído.
- **FOB por NCM:** son los 117 zips de ARCA, listados como filas de `sources.csv` (SRC-1375 a SRC-1491, 2017-01 a 2026-09) y no descargados. La descripción de columnas está en SRC-1374. Derecho devengado estimado = FOB por NCM por la alícuota del mes. Es una estimación del devengado, no la recaudación.

## 2. Liquidación de divisas
CIARA-CEC mensual de 2002-06 a 2026-09 (base oficial xlsx). Millones de USD: 2021 32.808; 2022 40.438; 2023 19.742; 2024 25.091; 2025 31.339; 2026 a septiembre 22.276. Coincide con el CSV estático del lote AD en el tramo común.

## 3. Precios FOB y DJVE
- FOB oficial mensual (instantánea del día 15) de 2018-01 a 2026-10, siete productos.
- DJVE registradas por producto y mes de embarque, campañas 2017/18 a 2026/27. Es la apertura por mes de embarque, no por fecha de registro.
- Cosecha por campaña: sin cargar.

## 4. Compras del Tesoro 2024 y 2025
- Prensa: 12/9/2024 USD 1.528 millones; octubre de 2024 USD 1.050 millones al Bank of New York; 15/1/2025 al menos USD 836 millones.
- BCRA: variable 78 (compras de divisas, USD) y variable 48 (efecto en pesos, días con movimiento).
- **Contradicción del lote V:** 2.727 calculado contra 1.216 del Balance Cambiario. Hipótesis: el balance cuenta octubre y noviembre (1.228,1) y deja afuera enero y febrero (1.499,3). Es inferencia sin comprobar.

## 5. RG 4852/2020
Sigue vigente como régimen general (15 días, hasta 120 días, o liquidación). Las RG 5646 y 5690 de 2025 modifican solo el procedimiento del Decreto 38/2025.

## 6. Brasil
BCB SGS 13962 a 13965 mensual desde 2008-09 (total, ACC, pago anticipado, demás) e impuesto de exportación de la Receita Federal 1994 a 2025.
