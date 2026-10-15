# Grok a Claude: lote P (rama `grok/lote-p`, sin_revisar)

Alejandro aprobó el lote P. Entrega en `inbox/lote-p/`: fuentes SRC-1108 a SRC-1132 (la última en main era SRC-1107), claims CLM-P-001 a CLM-P-033, cuatro tablas, `unresolved.md` y `sintesis.md`. Sin PDFs, imágenes ni html en la rama (originales en la caja, `/workspace/lote_P/docs`, con sha256 en `documents_manifest.csv`). Los enlaces del Boletín Oficial llevan `/<id>/<AAAAMMDD>`.

## Pedido 1: SIGADE al 2026-09-30 y planilla de Finanzas del III trimestre

**Para Claude:** no salieron al 2026-10-15. Finanzas lista hasta el II Trimestre 2026 y las URL del 30-09 dan 404; la ONCP llega a la planilla del 31-08-2026; el monitor de la OPC llega a la RC 59/2026 (2026-10-06). El corte sigue en 2026-06-30 (CLM-P-005 a 007).

## Pedido 2: montos ejecutados de la RC 60/2026

**Para Claude:** no hay montos ni comunicado de A3 Mercados todavía. La RC 60 (firmada 2026-10-09, publicada 2026-10-14) convierte con el BCRA la LECAP S30O6 por 20% de D30N6, 40% de T30A7 y 40% de T31Y7; realización 2026-10-09, liquidación 2026-10-13. Los topes son USD 1.000 millones para D30N6 y $2 billones para T30A7 y T31Y7: no cargarlos como ejecutados. El VNO entregado sale de fórmulas que la copia HTML del Boletín Oficial no muestra. El último CE que ADEBA lista es el 14715 (2026-10-01) y los CE 14716 a 14760 no existen en ADEBA; las fichas de Mercados Argentina no tienen documentos de octubre (CLM-P-001 a 004).

## Pedido 3: préstamos de organismos a tasa SOFR

**Para Claude:**
- `tablas/prestamos_a_tasa_sofr_sigade_2026-06-30_con_condiciones_de_contrato.csv`: los 365 préstamos de SIGADE con Tipo de Tasa = TASA SOFR (USD 36.598 millones), por saldo, con saldo acumulado y marca del 90% (los primeros 154). SIGADE no trae margen, base de días ni tipo de SOFR.
- **Cobertura con contrato: 10 préstamos, USD 6.569 millones, 17,95% del saldo.** No llegué al 90%: cada préstamo tiene su contrato y solo pude bajar los modelos que el Poder Ejecutivo publicó con el decreto en InfoLEG; los firmados están en las fichas del BID y del Banco Mundial con enlaces que cargan por JavaScript.
- BID 5907, 5609, 5994, 6025 y 5952: SOFR compuesta diaria (Índice SOFR) más Costo de Fondeo del Banco más margen de capital ordinario; 5907, 5609 y 5994 suman 1,15% fijo; 6025 y 5952 no lo traen en la cláusula de intereses. ACT/360, pago semestral. Las cifras del Costo de Fondeo y del margen de capital ordinario no están en el contrato.
- CAF 11985 y 12272: SOFR a Plazo más 2,00%, piso de la tasa en cero, ACT/360. BCIE 2322: Term SOFR 6 meses más margen trimestral (251 pb en enero-marzo de 2023), ACT/360, semestral. BIRF 9814-AR: SOFR (según Condiciones Generales) más Margen Variable, pago 15 de abril y 15 de octubre; plazo de la SOFR y base de días no definidos en el texto leído.
- **Contradicción:** el crédito de las represas (USD 940 millones, segundo por saldo) dice LIBOR 6 meses más 3,8% en el texto de 2022 y SIGADE lo trae como SOFR; no encontré el reemplazo.
- Resumen por entidad en `tablas/prestamos_a_tasa_sofr_resumen_por_entidad_y_cobertura.csv`; el snapshot del Banco Mundial al 2026-09-30 (`tablas/birf_argentina_prestamos_vigentes_snapshot_2026-09-30.csv`) da el tipo FSL pero no el margen.

## Preguntas

1. ¿Sirve que el lote Q siga con los contratos de los préstamos de mayor saldo sin leer (BID 4648, 5951, 4806, 5675; BIRF 8633, 9292, 8904; S. TRANSPORTE - CDB; CAF 12819), buscando el decreto de cada uno?
2. Para la fase 4, ¿alcanza con la estructura (referencia, base, frecuencia) y una tasa de referencia común, o necesitás el margen y el Costo de Fondeo de cada préstamo? Esas cifras no están en los contratos.
