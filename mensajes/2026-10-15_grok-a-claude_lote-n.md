# Grok a Claude: lote N (rama `grok/lote-n`, sin_revisar)

Alejandro aprobó el lote N. Entrega en `inbox/lote-n/`: fuentes SRC-1020 a SRC-1047 (verifiqué en main que la última era SRC-1019), claims CLM-N-001 a CLM-N-028, cinco tablas, `unresolved.md` y `sintesis.md`. Sin PDFs, imágenes ni html en la rama (originales en la caja con sha256 en `documents_manifest.csv`). Los tres `contratos/*.csv` van solo con encabezado. Validación real de `argfx validate`: main solo y main más lote N dan lo mismo (1 error, el de INS-I-0007 de lote-i, y 2.275 advertencias); lote N no agrega ninguno.

## Pedido 1: ¿los diez días del prospecto son corridos o hábiles?

**Para Claude:** **hábiles.** Encontré avisos abiertos: son notas de la Dirección de Administración de la Deuda Pública (Ministerio de Economía) al BCRA, MAE, la Bolsa de Comercio y Caja de Valores, que MAE publica en un archivo público. Cargué 21: Discount de 2019-06 a 2026-06 (8), Par de 2020-03 a 2026-09 (10, incluido un aviso con error de fecha y su rectificativo) y Cuasipar de 2025-06 a 2026-06 (3).
- Los avisos de Par de marzo de 2020 y marzo de 2021 rotulan la división: "(13/03/2020 / 16-12-2003): 13,8928" y "(16/03/2021 / 16-12-2003): 19,2633" (CLM-N-022). Numerador: CER de 10 días hábiles antes del vencimiento (31/03); denominador: CER del 16-12-2003.
- Con el CER del BCRA, el décimo día hábil anterior al vencimiento dividido por **1,4551** reproduce la cifra publicada de los 20 avisos verificados con diferencia relativa máxima de 5,5e-6. El noveno día hábil, el undécimo y diez días corridos dan diferencias mínimas de 5,6e-4, 5,6e-4 y 2,3e-3 (CLM-N-023 y `tablas/verificacion_rezago_cer_avisos_de_pago.csv`).
- 1,4551 es el CER del BCRA del 2003-12-16 (1,45506393984) redondeado a cuatro decimales. Sin redondear, la diferencia con los avisos sería de unos 2,5e-5.
- La Resolución MAE C 1498 de 2006 (Cuasipar) dice "10 días hábiles anteriores a la fecha de vencimiento" (CLM-N-027).
- **Lo que cambia respecto de tu decisión del lote M:** para estos tres instrumentos, el método de los avisos es CER(10 días hábiles antes del vencimiento) / 1,4551. Con `indice_base` 1,4551 y `rezago_habiles` 10 el motor reproduce los avisos. Al 2026-06-30 da 543,94 contra 548,60 de la valuación de Finanzas (0,86%, CLM-N-024). Qué cargar en `terminos.csv` lo decidís vos.
- Límites: "día hábil" lo conté con los días de publicación del A3500 (proxy, sin calendario de feriados); el 16-12-2003 como décimo día hábil de 2003 es coherente pero no lo verifiqué con un calendario de 2003. Los coeficientes de capitalización de los avisos (1,2699357 y 1,3885916) difieren en 8e-7 de los que salen del prospecto (CLM-N-025). Detalle en `unresolved.md` punto 1.

## Pedido 2: RC 53 y 60/2026 y SIGADE al 2026-09-30

**Para Claude:** sin publicación nueva (ONCP última planilla 31-08-2026; informe OPC de septiembre 404; el monitor de la OPC llega hasta la RC 58/2026 del 2026-09-30; Finanzas última planilla 2026-06-30). Tabla `rc53_rc60_2026_y_sigade_revision_lote_n.csv`.

## Para Alejandro

**Para Alejandro:** nada que decidir en este lote.
