# Grok a Claude: lote M (rama `grok/lote-m`, sin_revisar)

Alejandro aprobó el lote M. Entrega en `inbox/lote-m/`: fuentes SRC-1014 a SRC-1019, claims CLM-M-001 a CLM-M-016, siete tablas, `unresolved.md` y `sintesis.md`. Sin PDFs ni imágenes en la rama (originales en la caja con sha256 en `documents_manifest.csv`). Los tres `contratos/*.csv` van solo con encabezado. Validación real de `argfx validate`: main solo y main más lote M dan el mismo resultado (1 error, el de INS-I-0007 de lote-i, y 2.275 advertencias); lote M no agrega ninguno.

## Pedido 1: bajas de TMF27, TMG27 y TZX27

**Para Claude:** no encontré la operación ni la fecha de ninguna de las tres bajas; la hipótesis de rescates con fondos de entes públicos o del BCRA fuera de licitación no se puede probar ni descartar con lo publicado. Lista de lo revisado en `tablas/bajas_tmf27_tmg27_tzx27_fuentes_revisadas.csv`. Solo hay agregados por acreedor (CLM-M-013 y CLM-M-014): agencias del sector público USD 200.249, 219.641 y 197.213 millones en 2025-12-31, 2026-03-31 y 2026-06-30. No afirmo relación con las bajas.

## Pedido 2: Discount, Par y Cuasipar en pesos

**Para Claude:**
- **Base de la norma:** el Anexo III del Decreto 1735/2004 no está publicado (el decreto sale sin anexos). El prospecto de 2005 (Anexo I) dice CER del período de 10 días anterior al 2003-12-31, sin aclarar corridos u hábiles (CLM-M-001 y CLM-M-002). Candidatos y serie diaria en `tablas/cer_bcra_2003_12_ventana_base.csv`: CER del 2003-12-31 1,45679881491; diez días corridos antes (2003-12-21) 1,45564200185.
- **Lo medido en Finanzas:** la relación VN actualizado sobre VN residual de las diez planillas (2024-03-31 a 2026-06-30) implica una base de **1,4568** (menos de 2 millonésimas de diferencia con el CER del 2003-12-31) y **CER del mismo día de corte, sin rezago**, para Par, Discount y Cuasipar (CLM-M-007, tabla `base_cer_implicita_par_discount_cuasipar.csv`). Si alguno de los extremos llevara diez días de rezago, la base saldría distinta (0,08% o cerca de 1%). Es la valuación de Finanzas al corte, no el cálculo de pagos según la norma.
- **Capitalización:** Discount 1,2699367 (prospecto: 3,04% y 1,77% capitalizado, 10 semestres cada tramo) y Cuasipar 1,3885928 (3,31%, 20 semestres); Par no capitaliza (CLM-M-008 a CLM-M-011). Coinciden con Finanzas.
- **VN al 2026-06-30** (suma de decretos 1735/04 y 563/10, A3500 1.483,0198, millones de pesos): Par original 2.838,882, actualizado 1.557.416,129; Discount original 4.337,878, residual 3.253,409, actualizado 2.266.617,540; Cuasipar 23.434,051 y 17.851.683,088 (CLM-M-004 a CLM-M-006 y tabla `par_discount_cuasipar_vn_finanzas_2026-06-30.csv`).
- **SIGADE** (CLM-M-012): `saldo_corte` UCP por CER del corte da el VN actualizado de Finanzas por A3500, y UCP por 1,4568 da el residual en pesos por el factor de capitalización (diferencias de 2e-9 a 8e-7). Los UCP incluyen los dos decretos. Con esto, `indice_base` de los tres sería 1,4568 y `rezago_habiles` 0 según la valuación de Finanzas; la decisión de qué cargar en `terminos.csv` es tuya (no lo cargué).

## Pedido 3: RC 53 y 60/2026 y SIGADE al 2026-09-30

**Para Claude:** sigue sin publicación (OPC septiembre da 404, ONCP colocaciones al 30-09 da 404, Finanzas lista hasta 2026-06-30). La RC 60/2026 no figura en el monitor de la OPC. Detalle en `unresolved.md` y `tablas/rc53_rc60_2026_publicacion_revision_lote_m.csv`.

## Pista sobre una contradicción previa

**Para Claude:** la diferencia entre la Ley 27.556 y SIGADE en fechas y cuotas del BONCER 2026 y 2028 (lote G) se explica por el art. 4 del Decreto 676/2020 (lote L); ver `unresolved.md` punto 4.

## Para Alejandro

**Para Alejandro:** nada que decidir en este lote; el hueco principal (qué operación explica las tres bajas) necesita datos que ONCP o Finanzas no publican por instrumento.
