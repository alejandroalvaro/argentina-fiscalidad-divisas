# Pendientes y huecos del lote I

Todo `sin_revisar`. Cada punto dice qué se buscó, dónde y por qué no quedó cargado. Nada se completó por analogía.

## Operaciones

1. **Montos efectivos de las conversiones con el BCRA** (RC 39, 49, 51, 53 y 60): las resoluciones conjuntas fijan topes o autorizan el canje, pero ni el Boletín Oficial ni Finanzas publican el VNO efectivamente canjeado. Esas filas no entran a `contratos/operaciones.csv` (exige valor nominal positivo) y quedan en `tablas/operaciones_detalle.csv` con `en_contratos_operaciones` = no y el motivo. Evidencia indirecta en la hoja A.4 del Boletín de deuda (ver claims CLM-I-066 y CLM-I-067): no la identifica como canje, por eso no se cargó como VNO.
2. **RC 59** (tope de ARS 221.119.509.519): no se encontró la entrega efectiva ni el VNO resultante.
3. **Colocaciones fuera de licitación** (BCRA, FGS/ANSES, PAMI): no se encontró publicación oficial de montos para julio a octubre de 2026. No se cargó ninguna fila.
4. **Préstamos garantizados** (RC 40 y 41; Decretos 478, 549 y 550/2026): quedan cargados los topes autorizados (hasta USD 2.000 millones y USD 1.200 millones). No se verificó desembolso en fuentes oficiales.
5. **Licitación del 14-10-2026** (liquida el 16-10): resultado tomado del comunicado de Finanzas. La resolución conjunta de esa licitación no estaba publicada al 15-10-2026 (se buscó RC 61). Fila con estado "liquidación pendiente".
6. **Códigos de especie no publicados** en los comunicados para S16O6, D15E7 y la LELINK del 10-05-2027: se dejó el nombre publicado y el código vacío.
7. **Frontera con el corte**: RC 36 y 37 (emisión del 30-06-2026) y la segunda vuelta de AO28 del 29-06 quedan fuera por ser anteriores al corte del 30-06-2026 de SIGADE. **Para Alejandro:** confirmar si la frontera debe ser liquidación posterior al 30-06 o adjudicación posterior al 30-06.
8. **Vencimientos programados**: no se cargaron en `amortizaciones.csv` (el motor los calcula; las letras son bullet).

## Formato de PR #17 (contratos/operaciones.csv)

A. **Filas excluidas de operaciones.csv** (32 de 78, todas en `tablas/operaciones_detalle.csv` con su motivo): 19 sin valor nominal efectivo publicado, 7 sobre instrumentos del lote C sin términos en `contratos/` de main (TXMD8, TXMD9, D31L6, D31G6 y la letra intransferible INS-C-0446), 4 sin `instrument_id` (dos préstamos y las letras intransferibles de 15-09-2031) y 2 de TMVE8 (INS-I-0005, sin términos).
B. **Validación del lote aislado**: `argfx validate` sobre `inbox/lote-i/` solo da el error `term_sheet_invalid` porque `operaciones.csv` trae reaperturas y canjes de instrumentos INS-C cuyos términos están en `contratos/` de main y no en el lote (el cargador exige que cada fila de operaciones tenga su instrumento en el mismo `terminos.csv`). Confirmado con `argfx validate` real. Con los `contratos/` de main fusionados con los del lote, `load_term_sheets` y el motor corren sin error (82 términos, 1.282 flujos). **Para Alejandro:** esto lo resuelve Claude (cargar el lote contra los contratos de main o relajar el control).
C. **Unidad del valor nominal en instrumentos CER** (X29E7, TZXM8 y similares): se cargó el valor nominal en pesos publicado en el comunicado, no en unidades CER. **Decisión de Alejandro (15-10-2026):** se deja el valor nominal de instrumentos CER en pesos.
D. **Margen de corte** (`margen_corte_pct` en `tablas/licitaciones.csv`): vacío, los resultados de licitación no lo publican.
E. **Primera emisión** de cada INS-I: la fila `emision` es la de su fecha de emisión; las demás colocaciones del mismo instrumento van como `reapertura`.

## Contratos

9. **TMVE8** (bono dual TAMAR/dólar linked 31-01-2028): se excluyó de `terminos.csv` porque el pago es el mayor entre el capital ajustado por dólar y el capital a tipo de cambio inicial más TAMAR TEM, y el motor no lo expresa. Además el texto de la definición de TAMAR TEM del comunicado llega truncado (fórmulas en imágenes). Instrumento INS-I-0005 en `instruments.csv` sin términos.
10. **Márgenes TAMAR de las reaperturas** de TML27, TMG28 y TMF27: los resultados de licitación no los declaran. Los nombres SIGADE/lote G3 traen los márgenes, pero no se usaron para este lote.
11. **S16O6 y S29E7**: la TEM cargada es la de la primera colocación. Los comunicados de las reaperturas no repiten la TEM; la nota de términos lo indica. Confirmar.
12. **Saldo de corte** de los INS-I: 0 (emitidos después del corte); el último VNO en circulación publicado por Finanzas queda en las notas de `instruments.csv`. TML27 aparece con decimales literales (6.300.226,26) en el comunicado.

## Stock de deuda

13. **SIGADE al 30-09-2026 y stock oficial al 30-09**: no publicados al 15-10-2026. Están el 31-07 y el 31-08, ambos provisorios, con la deuda bruta de 474.198,0 (30-06), 484.722,4 (31-07) y 484.917,0 (31-08) en USD millones.
14. La hoja A.4 está en USD millones equivalentes; no se pudo reconstruir la conversión por especie.

## Método de resultado de caja del SPN

15. **Criterio de la CGN** sobre registro de intereses capitalizados y descuentos: no se localizó el texto del manual o resolución de la CGN. Quedan: la definición de base caja del Boletín Fiscal 2T26 (movimiento de fondos, sin mención explícita de LECAP) y la respuesta literal del Informe 144 de la JGM (Pregunta 58). **Para Alejandro:** si hace falta el criterio de la CGN, indicar a qué documento apuntar.
16. **FMI CR 26/105** (1,2% del PIB): imf.org devolvió 403. No verificado en origen; la cifra entra solo como claim secundario de confianza baja.
17. **Artículo de Ámbito**: afirma un déficit de ARS 1,5 billones en 2024 que contradice la serie oficial (superávit financiero) y tiene un número truncado. No se cargó; queda como nota.
18. **Estimaciones de intereses capitalizados no registrados** (CEPA, OPC/Cachanosky): secundarias, metodologías no replicadas. En `tablas/` con rol "secundaria".
19. **Series mensuales**: cubren enero de 2024 a agosto de 2026 (32 meses). Septiembre de 2026 no estaba publicado al 15-10-2026.
