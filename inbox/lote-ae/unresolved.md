# Sin resolver, lote AE

1. **Zips de ARCA por NCM (117 meses):** no se descargaron, por indicación de Claude. Falta bajarlos con `fetch-sources`. Solo se verificó con HEAD que responden 200 los de 2017-01, 2018-01, 2020-01 y 2023-01. El de 2026-09 pesa más de 85 MB y se cortó antes de completarse.
2. **Derechos pagados por producto:** no hay serie oficial leída. Falta el cruce FOB por NCM por alícuota mensual, que depende del punto 1.
3. **Alícuotas 2020 a 2024 de trigo, maíz, girasol, cebada, sorgo, subproductos y carnes:** sin decreto leído; solo Chequeado y la BCR. Falta el texto de los decretos de 2018 a 2024 y el valor exacto de 2018 por mes. La tabla de tramos marca la confianza.
4. **Cosecha por campaña:** el reporte de Estimaciones (datosestimaciones.magyp.gob.ar) arma las tablas por ajax y el dataset CSV de datos.magyp.gob.ar responde 403 desde la box. Falta, con navegador o con un mirror.
5. **DJVE por fecha de registro:** el lote trae la apertura por mes de embarque. La lista diaria de registros individuales requiere navegador.
6. **FOB oficial:** una observación por mes. Falta la serie diaria o el promedio mensual (la API sirve datos diarios desde 1993).
7. **Compras del Tesoro en USD:** no hay serie diaria en dólares. Faltan montos para la mayoría de los días de 2024 y 2025; la variable 48 está en pesos. Falta leer la definición de la variable 78 para saber si incluye al Tesoro.
8. **Contradicción 2.727 contra 1.216:** la hipótesis (el Balance Cambiario cuenta octubre y noviembre y deja afuera enero y febrero) no está comprobada. Hace falta el cuadro de enero y febrero de 2025 del Balance Cambiario.
9. **Brasil, 2023 del imposto de exportação (R$ 4.422,9 millones):** sin explicación leída.
10. **Brasil, SGS:** los datos de 2026-10 son parciales y los recientes se revisan.
11. **Anexos de los decretos 526 y 877:** se cargaron las filas del complejo agroindustrial y carnes bovinas, no todo el anexo.
12. **Decretos citados sin leer en este lote:** 682/2025, 793/2018 en detalle y 38/2025.
