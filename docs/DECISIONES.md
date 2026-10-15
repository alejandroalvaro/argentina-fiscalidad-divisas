# Decisiones del investigador

Registro de las definiciones metodológicas que tomó Alejandro. Cada una indica la fecha, la fuente que la sostiene y cómo se aplica en el código.

## D-001. Reservas netas: definición del FMI (2026-10-14)

**Decisión.** El trabajo usa la definición de reservas internacionales netas del TMU del acuerdo EFF (FMI, Country Report 26/105, párr. 11, SRC-0312).

- Reservas brutas: activos líquidos del BCRA frente a no residentes en moneda convertible (BPM6).
- Se restan: pasivos en divisas con vencimiento original de hasta un año, compras netas al FMI desde el inicio del programa, forwards netos, swaps (PBOC, BIS, ESF), encajes en moneda extranjera, SEDESA, ALADI y depósitos de no residentes.
- **No se restan los depósitos en divisas del Tesoro en el BCRA.** Texto del TMU: "Neither the Federal government's foreign liabilities nor its FX deposits at the BCRA are considered as gross foreign liabilities of the BCRA."

**Fundamento.** Los encajes en divisas respaldan depósitos del sector privado, que puede retirarlos, y por eso se restan. Los depósitos del Tesoro son una acreencia dentro del sector público; al consolidar Tesoro y BCRA se cancelan, y las divisas quedan disponibles para quien las necesite.

**Aplicación.**
- Las series de reservas netas se calculan con esta definición. Toda otra definición que aparezca en fuentes o en la literatura se identifica por su nombre y no se mezcla con esta.
- Las divisas que el Tesoro perciba por derechos de exportación y deposite en el BCRA se cuentan una sola vez, como reservas. En la consolidación Tesoro + BCRA no se suman de nuevo como activo del Tesoro.
- En la presentación separada del Tesoro (perímetro del protocolo), esos depósitos sí figuran como activo en USD del Tesoro y como pasivo del BCRA.

## D-002. Brasil: deuda pública federal por indexador según los códigos de título (2026-10-14)

**Decisión.** Para el contraste con Brasil se usa la clasificación por indexador (cambial, Selic, IPCA, prefijado) que Grok derivó de los códigos de título (`inbox/lote-e/tablas/mapeo_indexador_dpf.csv` y `dpf_por_indexador_derivado.csv`), sin esperar el RMD oficial del Tesouro.

**Fundamento.** Brasil es un contraste acotado, y las reglas de la clasificación están documentadas (Decreto 3.859/2001, SRC-0424, y metadatos del Tesouro, SRC-0423).

**Aplicación.**
- Toda tabla o gráfico que use esta clasificación la rotula como "derivada a partir de los códigos de título, no oficial".
- Lo que no tiene regla documentada queda como `sin_clasificar` y se informa su participación; no se reparte entre indexadores.
- Si más adelante se incorpora el RMD, se coteja con la clasificación derivada y se publican las diferencias.

## D-003. Aportes propuestos en un archivo aparte (2026-10-14)

**Decisión.** Los aportes propios del proyecto se escriben en `docs/APORTES_PROPUESTOS.md`, separados de la evidencia (`claims.csv` de cada lote). Grok redacta la primera versión.

**Aplicación.** Cada aporte distingue entre lo que ya existe en la literatura o en la práctica (con `source_id` del lote A cuando corresponda) y lo que el proyecto propone. Todo aporte queda como propuesta hasta que el análisis lo sostenga, y ninguno entra a `claims.csv`.

## D-004. Tres regímenes de percepción para el modelo SFC (2026-10-14)

**Decisión.** El modelo stock-flujo consistente compara tres regímenes, con igual carga tributaria:

- (a) Argentina actual: el derecho se determina en USD y se paga en pesos, y el exportador debe liquidar las divisas en el mercado de cambios según la normativa del BCRA.
- (b) Brasil: el exportador vende las divisas a instituciones autorizadas por el BCB, a tipo libremente pactado, y puede mantenerlas en el exterior (Lei 14.286/2021, SRC-0505).
- (c) Propuesta: el derecho se percibe directamente en USD y se acredita en una cuenta del Tesoro.

**Aplicación.** La comparación descriptiva está en `inbox/lote-f/tablas/regimenes_comparados.csv`. El destino del resto del contravalor en el régimen (c) sigue abierto: `docs/APORTES_PROPUESTOS.md`, sección 8, lo plantea como un menú de opciones sin recomendación.

## D-005. Fracción percibida en divisas igual a la alícuota vigente (2026-10-14)

**Decisión.** En el régimen (c), la fracción del valor exportado que se percibe en USD es la alícuota del derecho de exportación vigente para cada posición.

**Aplicación.** Las alícuotas salen de `inbox/lote-f/tablas/alicuotas_de_vigentes_2026-10-14.csv` (Decreto 423/2026, Anexos I a III), con el cronograma mensual de 2027 y 2028 cuando corresponde. Los sectores que la tabla no cubre (carnes, economías regionales, industria, minería) y el crudo, cuya alícuota es móvil, quedan sin alícuota hasta que se releven; no se les asigna un valor supuesto.

## D-006. Atribución de la percepción en USD a Warren Mosler (2026-10-14)

**Decisión.** La idea de cobrar los derechos de exportación directamente en dólares se atribuye a Warren Mosler, que la propuso en Buenos Aires el 1 de mayo de 2022 ("A 3% export tax payable in $US", CLM-A-015, SRC-0212).

**Aplicación.** El proyecto presenta como propio la formalización, el modelo SFC y la cuantificación, y no la idea. Todo texto del manuscrito que describa la propuesta cita a Mosler.
