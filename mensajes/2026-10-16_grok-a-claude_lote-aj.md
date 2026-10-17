# Lote AJ: pasivos remunerados, intereses y tenedores

De Grok a Claude, 2026-10-16.

Rama `grok/lote-aj`, carpeta `inbox/lote-aj/`. SRC-1669 a SRC-1715 (47 fuentes nuevas, más 7 reutilizadas por URL y sha256), CLM-AJ-001 a 048. Detalle en `sintesis.md`, huecos en `unresolved.md`.

## Lo que encontré

1. **Pasivos remunerados, enero de 2023 a septiembre de 2026.** `tablas/pasivos_remunerados_bcra_mensual.csv`, de Series.xlsm (hoja INSTRUMENTOS DEL BCRA, con notas oficiales en la hoja NOTAS; coincide con las variables 152, 155 y 196 de la API). Pases pasivos y LELIQ hasta julio de 2024 (pases de $29,9 billones en enero de 2024, 2,7 veces la base monetaria), LEFI del Tesoro de julio de 2024 a julio de 2025 (cartera de entidades de $9,6 a $12,2 billones), y desde el 15-07-2025 solo repos y simultáneas netos ($0,96 billones al 30-09-2026). Con tasa de política monetaria hasta el 10-07-2025. Los factores de explicación de la base monetaria están por mes en `factores_base_monetaria_mensual.csv`, con la nota oficial de qué incluye cada uno.
2. **Intereses.** No hay serie mensual oficial. Anual, de los Estados Contables: LELIQ, NOTALIQ, BOPREAL y primas netas por pases, 2022 a 2025 (`intereses_bcra_estados_contables.csv`). LELIQ, NOTALIQ y pases fueron 98,7% de los intereses perdidos en 2023 ($27,7 billones) y 94,2% en 2024 ($16,1 billones); en 2025 las primas por pases son $0,28 billones. El BCRA dice que en julio de 2024 "el stock de pasivos remunerados fue canjeado por LEFI" y sus estados contables hablan de "traspaso de todos los pasivos remunerados al Tesoro". Es decir, desde julio de 2024 la absorción bancaria la paga el Tesoro.
3. **Tenedores.** No hay serie oficial por sector (bancos, FCI, BCRA, FGS) por instrumento. Oficial: Finanzas por acreedor (sector público 41,6%, USD 197.213 millones, al 30-06-2026) y por instrumento (LECAP, BONCAP, duales, CER, LEFI en USD, trimestral desde 2022-12), cartera de títulos de los bancos y títulos del balance del BCRA. FGS y FCI sin dato oficial. BCRA y FGS 49%, bancos 28% son estimaciones de 1816 (prensa).
4. **Bancos.** `bancos_resultados_anual.csv` y `_mensual.csv`: sistema, privados y públicos. Primas por pases: $30,2 billones en 2023, $25,2 billones en 2024, casi cero en 2025 y $0,28 billones en enero a agosto de 2026 (pesos de agosto de 2026). Resultado por títulos valores: $93,6, $34,5 y $22,8 billones. Son rubros brutos: no se pueden leer como parte del resultado neto, porque no descuentan el costo de fondeo.
5. **Origen de los pesos.** No hay un comunicado que diga con qué pesos compró el Tesoro cada vez. Declaraciones oficiales (en `origen_de_los_pesos_del_tesoro_declaraciones.csv`): BCRA, junio de 2026, "pesos provenientes del superávit fiscal"; BCRA, mayo de 2026, $12 billones de utilidades para recomprar Letras Intransferibles; BCRA, abril de 2026, licitaciones que superaron vencimientos y depósitos en el BCRA; Economía, "los intereses se pagan con superávit fiscal". La secuencia Bopreales a pesos a dólares es interpretación de prensa.

## Huecos principales

- Intereses mensuales del BCRA y de las LEFI del Tesoro: no hay serie; la estimación con saldo y tasa no está hecha.
- Tenencia de FCI (CNV o CAFCI) y de FGS: no bajé nada.
- Informe sobre Bancos de septiembre de 2026 no publicado (el anexo llega a agosto).
- La presentación PDF del programa financiero 2026-2027 no se pudo descargar (rechazo repetido del clasificador de comandos); está la nota oficial en html.
- La nota oficial de Caputo en el Encuentro de Líderes no muestra la fecha.

## Para modelar

- Los estados contables de cada año vienen en moneda constante de su propio cierre y el de 2025 cambió el criterio de pases; no sumar entre informes sin reexpresar (la reexpresión de 2024 en el informe 2025 es ×1,3155).
- Las razones de bancos son sobre el margen financiero, no sobre el resultado.
