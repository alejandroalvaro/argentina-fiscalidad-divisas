# Lote P: lo que no se pudo resolver (sin_revisar)

Todo queda `sin_revisar`. No se infirió nada por analogía.

## 1. SIGADE al 2026-09-30 y planilla de Finanzas del III trimestre (pedido 1)

**Para Claude:** no salieron. Finanzas: último trimestre listado II 2026 (deuda_publica_30-06-2026_0.xlsx); deuda_publica_30-09-2026.xlsx, deuda_publica_30-09-2026_0.xlsx y deuda_publica_30-09-26.xlsx dan 404 (CLM-P-005). ONCP: última planilla colocaciones_31-08-26_preliminar.xlsx (CLM-P-006). OPC: el monitor llega al 2026-10-06 (CLM-P-007). El corte de la fase 2 sigue en 2026-06-30. Sugiero revisar de nuevo en el próximo lote.

## 2. Montos ejecutados de la RC 60/2026 (pedido 2)

**Para Claude:**
- Lo que hay: la norma (CLM-P-001 a CLM-P-003). Operación con el BCRA, realización 2026-10-09, liquidación 2026-10-13, LECAP S30O6 contra 20% de D30N6, 40% de T30A7 y 40% de T31Y7.
- Lo que falta: el VNO de cada instrumento. El art. 4 lo da por fórmulas con precios de BYMA de las 13:30 del 2026-10-09 y la copia HTML del Boletín Oficial no muestra las fórmulas; tampoco se conoce el VNO de S30O6 en poder del BCRA. No se calculó nada por falta de precios.
- No hay comunicado de A3 Mercados: el CE más reciente que lista ADEBA es el 14715 (2026-10-01), y las fichas de D30N6, T30A7 y T31Y7 en Mercados Argentina no tienen documentos de octubre (CLM-P-004). El CE 14699 de septiembre (conversión de LELINK D30S6) lleva fecha de emisión 2026-09-25 y la licitación de esa conversión fue el 2026-09-22; para octubre la realización fue el 2026-10-09 y la liquidación el 2026-10-13, y al 2026-10-15 no hay CE posterior al 14715. Conviene revisar de nuevo.
- Para el motor: los topes de la RC 60 (USD 1.000 millones y $2 billones por bono) no son montos ejecutados y no deben cargarse como tales.

## 3. Préstamos de organismos a tasa SOFR, fase 4 (pedido 3)

**Para Claude:**
- **Lista:** `tablas/prestamos_a_tasa_sofr_sigade_2026-06-30_con_condiciones_de_contrato.csv` (365 préstamos ordenados por saldo, con saldo acumulado y marca del 90%). SIGADE no trae margen, base ni tipo de SOFR.
- **Cobertura lograda: 10 contratos, USD 6.569 millones, 17,95% del saldo SOFR; el 90% pedido no se alcanzó.** El cuello de botella es que cada préstamo tiene su propio contrato y solo encontré los modelos que el Poder Ejecutivo publicó con el decreto en InfoLEG. Los PDF firmados están en las fichas del BID (iadb.org/es/proyecto/AR-L####) y del Banco Mundial, pero los enlaces a los archivos se cargan por JavaScript y no se pudieron bajar. Para seguir: buscar por decreto, empezando por los de mayor saldo sin contrato: BID 4648 (USD 787 millones), BID 5951 (650; modelo en Decreto 1002/2024, anexo no bajado), BID 4806, BID 5675, BIRF 8633, BIRF 9292, BIRF 8904, S. TRANSPORTE - CDB (679), CAF 12819 SWAP (400).
- **Qué dicen los 10 contratos leídos:** ver `tablas/condiciones_de_tasa_segun_contratos_leidos.csv`. Resumen: BID = SOFR compuesta diaria más Costo de Fondeo más margen de capital ordinario (más 1,15% fijo en 5907, 5609 y 5994), ACT/360; CAF = SOFR a Plazo más 2,00%, ACT/360; BCIE 2322 = Term SOFR 6 meses más margen trimestral, ACT/360.
- **Alerta sobre las cifras:** el Costo de Fondeo del BID, el margen de capital ordinario del BID, el Margen Variable del BIRF y el margen del BCIE posterior a marzo de 2023 son valores que cada organismo publica aparte y no están en los contratos. Sin ellos no se puede reconstruir la tasa de cada préstamo; solo se puede fijar la estructura (referencia, base y frecuencia).
- **Contradicción para revisar:** el crédito de las represas dice LIBOR 6 meses más 3,8% en el texto de 2022 y SIGADE lo clasifica como TASA SOFR. No se encontró el documento que lo cambia (la cláusula 35.3 prevé reemplazo de la tasa de pantalla). Es el segundo préstamo SOFR por saldo (USD 940 millones).
- **BIRF:** de los 80 préstamos del BIRF en SIGADE, el Banco Mundial publica el tipo (FSL) pero no el margen (campo Interest Rate en 0,0). Es una columna en la tabla principal solo cuando el número de préstamo y la fecha de firma coinciden con SIGADE.
- **Lo que no se hizo:** no se extendieron las condiciones de un contrato a otros préstamos de la misma entidad, aunque tengan el mismo origen. Por ejemplo, los BID más viejos (4648, 4806) se firmaron con otras Normas Generales y no se leyeron.
