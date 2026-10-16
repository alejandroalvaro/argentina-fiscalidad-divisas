# Lote V: fuentes y usos de los dólares del Tesoro en el BCRA, 2024-01 a 2026-09

Todo `sin_revisar`. Hecho el 2026-10-15 (hora de Brasilia). Ids de fuente: SRC-1222 a SRC-1262; se reutilizan SRC-1191, 1192, 1195 a 1198, 1200, 1206, 1212 a 1217 de lotes anteriores.

## Qué es la tabla y qué no es

No existe una serie oficial en USD de los flujos del Tesoro. La tabla mensual (`tablas/fuentes_y_usos_dolares_del_tesoro_en_el_bcra_mensual_2024-01_a_2026-09.csv`, más su versión larga con fuente por celda) se arma con series diarias del BCRA y tiene la forma:

variación del saldo = organismos (variable 79) + otras operaciones del sector público (variable 80) + compras del Tesoro al BCRA (menos la variable 48 dividida por el tipo de cambio) + residuo

- Saldo: variable 1266 (millones de ARS) dividida por la variable 84, como en el lote U. Supone que todo el saldo está en dólares.
- Ingresos y egresos de cada bloque son la suma de los días positivos y de los días negativos del mes. No se compensan dentro del día ni entre días.
- Cada mes va de la última fecha del mes anterior a la última fecha del mes. Enero de 2024 parte del 2024-01-02, primer dato de la serie.
- Residuo medio absoluto: unos USD 26 millones por mes (33 meses). El mayor es octubre de 2025 (menos USD 94 millones). Residuos mensuales de USD 30 millones o más, que no se explican con estas fuentes: 2024-02 (+66), 2024-05 (+73), 2024-08 (+74), 2024-12 (-49), 2025-02 (+56), 2025-05 (+46), 2025-09 (-38), 2025-10 (-94), 2026-02 (+44), 2026-04 (-71), 2026-05 (+44), 2026-08 (+47), 2026-09 (+30).

La apertura pedida por instrumento (BONTE, BONAR, repo, pagos de bonos, FMI) no se puede hacer con series oficiales: el BCRA agrupa las colocaciones y los pagos de bonos dentro de "otras operaciones del sector público" y las compras de dólares del Tesoro en el mercado quedan en esa misma variable. La atribución por instrumento se hace solo donde un documento da monto y mes (tabla de días grandes y tabla de explicaciones del informe monetario).

## Hallazgos

1. Los dólares del Tesoro en el BCRA no suben por compras propias en el mercado sino por tres canales: desembolsos de organismos, colocaciones de deuda en USD y compras de dólares al BCRA con pesos. En 2024 el Tesoro compró USD 15.616 millones al BCRA (el Balance Cambiario de diciembre de 2025 da 15.640: coincide). En 2025 compró USD 2.727 millones según el cálculo y USD 1.216 según el Balance Cambiario (no coincide, ver unresolved). En 2026 hasta septiembre: USD 6.875 millones.
2. No hay en todo el período un solo mes con ventas netas del Tesoro al BCRA en la variable 48.
3. Abril de 2025: el saldo sube de USD 1.951 a 15.448 millones (organismos +13.663). El informe monetario lo atribuye al desembolso inicial del FMI. Mayo de 2025: cae a USD 3.068 millones. El 2025-05-06 la variable 80 muestra menos USD 12.002 millones y la Resolución Conjunta 21/2025 fija la compra de letras al BCRA por USD 12.000 millones de valor efectivo con liquidación ese día. Es el salto mejor documentado.
4. Octubre de 2025: el saldo cae de USD 2.327 a 92 millones, el mínimo mensual de la serie. El informe monetario atribuye la caída a ventas de dólares del Tesoro en el mercado. La variable 80 suma menos USD 2.085 millones en octubre. Noviembre se recompone con compras al BCRA por USD 1.105 millones.
5. Mayo de 2026: el saldo sube de USD 1.365 a 3.058 millones (desembolso del FMI de USD 1.043 millones hacia fin de mes, más compras al BCRA por USD 1.700 millones el 2026-05-18, sin motivo documentado). La salida de USD 1.040 millones de la Resolución Conjunta 30/2026 (liquidación el 2026-05-29) no se ve en los depósitos: la variable 80 muestra menos USD 507 millones ese día. Queda sin explicar.
6. Compras al BCRA seguidas de pagos: las compras de dólares del Tesoro al BCRA de fin de 2024, enero y febrero de 2025, enero de 2026 y julio de 2026 anteceden a los vencimientos de bonos de enero y julio. Los informes de octubre, noviembre y diciembre de 2024 y de enero y febrero de 2025 lo dicen expresamente.
7. Pagos de cupones: la suma de dos días da USD 2.594 millones el 8 y 10 de julio de 2024 (el informe dice unos 2.600) y USD 4.208 millones el 8 y 10 de julio de 2025 (el informe dice unos 4.200).
8. Pagos al FMI: coinciden por monto con el informe monetario el 2024-02-06, 2024-04-30, 2024-08-06 y, con el dato de un tercero, el 2026-09-25.

## Para la pregunta de investigación (previsibilidad de la liquidez en dólares del Tesoro)

- El saldo es bajo y volátil: de USD 56 millones (2024-01-19) a 15.561 millones (2025-04-21), con 1.125 millones al 2026-09-30.
- Los saltos grandes (abril y mayo de 2025, agosto de 2025, mayo de 2026) tienen fecha y monto documentados por norma, comunicado o informe monetario. Los egresos por cupones caen en fechas contractuales (enero y julio). Lo que ninguna fuente de este lote anticipa es el monto y el momento de las compras de dólares al BCRA y de las ventas del Tesoro en el mercado.
- El NIR del FMI (D-001) no resta estos depósitos (dato de la nota de Claude); esta tabla da los saldos y flujos que habría que restar.

## Revisión (todavía en vigor)

Al 2026-10-15, 22:02 hora de Brasilia: no hay planilla del III trimestre, ni SIGADE al 2026-09-30, ni RC 60/2026 en el monitor de la OPC, ni comunicado con montos (ADEBA, último CE 14715). Ver `tablas/revision_sigade_finanzas_rc60_lote_v.csv`.

## Archivos

- `tablas/fuentes_y_usos_..._mensual_2024-01_a_2026-09.csv`: tabla ancha con el texto del informe monetario de cada mes y los ids de fuente.
- `tablas/fuentes_y_usos_..._mensual_largo_con_fuente_por_celda.csv`: cada celda con su fuente.
- `tablas/dias_con_movimientos_mayores_a_750_millones_usd_y_atribucion_documental.csv`: días grandes con atribución solo donde un documento da monto y fecha o mes; el resto dice sin atribuir.
- `tablas/explicacion_bcra_de_la_variacion_mensual_de_reservas_2024-01_a_2026-09.csv`: texto literal del informe monetario (faltan abril y septiembre de 2025, donde el párrafo no se pudo ubicar).
- `tablas/revision_sigade_finanzas_rc60_lote_v.csv`.
