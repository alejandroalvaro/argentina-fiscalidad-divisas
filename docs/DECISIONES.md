# Decisiones del investigador

Registro de las definiciones metodológicas que tomó Alejandro. Cada una indica la fecha, la fuente que la sostiene y cómo se aplica en el código.

## D-001. Reservas netas: definición del FMI (2026-10-14)

**Decisión.** El trabajo usa la definición de reservas internacionales netas del TMU del acuerdo EFF (FMI, Country Report 26/105, párr. 11, SRC-0312).

- Reservas brutas: activos líquidos del BCRA frente a no residentes en moneda convertible (BPM6).
- Se restan: pasivos en divisas con vencimiento original de hasta un año, compras netas al FMI desde el inicio del programa, forwards netos, swaps (PBOC, BIS, ESF), encajes en moneda extranjera, SEDESA, ALADI y depósitos de no residentes.
- **No se restan los depósitos en divisas del Tesoro en el BCRA.** Texto del TMU: "Neither the Federal government's foreign liabilities nor its FX deposits at the BCRA are considered as gross foreign liabilities of the BCRA."
- El TMU de la segunda revisión (informe del personal técnico del FMI de mayo de 2026, SRC-1263, p. 117 del PDF) mantiene esa definición y la misma frase (verificado el 2026-10-15). Las tenencias de DEG del BCRA suman a los activos; los depósitos del Tesoro en DEG solo se informan.

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

**Reemplazada por D-007**, que agrega un cuarto régimen y conserva las letras (a), (b) y (c).

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

## D-007. Cuatro regímenes de percepción para el modelo SFC (2026-10-15)

**Decisión.** El modelo compara cuatro regímenes, con igual carga tributaria. Reemplaza a D-004 y conserva sus letras, para que las referencias a (a), (b) y (c) en D-005 y en `docs/APORTES_PROPUESTOS.md` sigan valiendo.

- (a) Pesos, el régimen argentino actual: el derecho se determina en USD y se paga en pesos, y el exportador liquida las divisas en el mercado de cambios según la normativa del BCRA.
- (b) Brasil: el exportador vende las divisas a instituciones autorizadas por el BCB, a tipo libremente pactado, y puede mantenerlas en el exterior (Lei 14.286/2021, SRC-0505).
- (c) Dólares, la propuesta de Mosler (D-006): el derecho se percibe directamente en USD y se acredita en una cuenta del Tesoro.
- (d) Dólares con fondo de estabilización: el derecho se percibe en USD como en (c), y las divisas entran a un fondo con reglas de acumulación y de uso.

**Relación con el protocolo.** `docs/protocolo/CLAUDE_CODE_TASKS.md` (fase 4) define tres regímenes: (1) cobro en ARS y compras FX, (2) cobro directo USD y (3) cobro USD con fondo de estabilización. Corresponden a (a), (c) y (d). D-007 agrega Brasil, (b), y prevalece sobre el protocolo.

**Aplicación.**
- En (c) y (d) la fracción percibida en divisas es la alícuota vigente (D-005), de modo que los dos regímenes en USD recaudan lo mismo y difieren sólo en el destino de las divisas.
- Las reglas del fondo en (d) (cuándo acumula, cuándo y para qué se usa, su tope) siguen abiertas. No se fijan por defecto; se definen antes de la fase 4 a partir de los precedentes de fondos de estabilización (CLM-A-008) y de la decisión de Alejandro.
- El modelo no codifica en los supuestos la superioridad de ningún régimen, como pide el protocolo.


## D-008. Análisis lo más cerca posible de la fecha actual (2026-10-15)

**Decisión.** El análisis incorpora las emisiones, los rescates y los canjes posteriores al corte de SIGADE, hasta la fecha más reciente con información oficial. Un corte trimestral publicado con casi tres meses de demora deja fuera justamente la coyuntura que el trabajo quiere describir.

**Fundamento.** La base SIGADE se publica por trimestre: la del 30/06/2026 apareció el 18/09/2026 (SRC-0102). Entre un corte y su publicación el Tesoro licita LECAP, BONCAP, duales y bonos en dólares cada dos semanas, y esos instrumentos vencen dentro del horizonte de 12 meses que mide la necesidad de divisas.

**Aplicación.**
- El saldo al corte de SIGADE sigue siendo la base auditada. Las operaciones posteriores se cargan aparte: las emisiones como instrumentos nuevos, y los rescates y canjes como reducciones del saldo, cada una con su resolución y el resultado de la licitación como fuente. El motor necesita para eso una forma de registrar emisiones y rescates después del corte.
- La frontera es la fecha de liquidación: entra lo liquidado después del corte, porque el saldo de SIGADE incluye lo liquidado hasta ese día.
- La fecha hasta la que llegan esas operaciones (`fecha_datos`) se informa en cada salida junto al corte de SIGADE, y en el manuscrito se distingue lo que viene de SIGADE de lo que se reconstruyó desde las licitaciones.
- Cuando se publica un corte nuevo de SIGADE, se coteja con la reconstrucción, se publican las diferencias y el corte avanza.
- No se proyectan emisiones futuras como si fueran contratos. El refinanciamiento de lo que vence pertenece a los escenarios de la fase 4.

## D-009. Intereses capitalizados y resultado financiero (2026-10-15)

**Decisión.** El trabajo mide los intereses en base devengada, además de la base caja que usa el resultado fiscal publicado, y muestra la diferencia.

**Fundamento.** LECAP, BONCAP y otros instrumentos que capitalizan intereses o se colocan con descuento no registran gasto de intereses hasta el vencimiento, y en algunos casos ni siquiera entonces, según cómo se contabilice el pago. El resultado financiero publicado puede así mostrar superávit mientras los intereses se acumulan en el saldo de la deuda. Pagar al vencimiento lo capitalizado modifica el resultado financiero y no el primario, de modo que el debate argentino sobre el superávit financiero depende de este criterio de registro. También interesa el costo: capitalizar a tasas de licitación puede resultar más caro que pagar los intereses a su vencimiento con otra fuente.

**Aplicación.**
- El motor ya separa `interes_capitalizado` (devengado, sin pago) de `interes` y `amortizacion`. Con esos flujos se construye, mes a mes, el interés devengado de la Administración Central.
- En la fase 3 se reconstruye el resultado financiero con intereses devengados y se lo compara con el publicado, citando la metodología oficial de registro de intereses capitalizados y de descuentos de emisión.
- La comparación de costo usa las tasas de las licitaciones y se presenta como estimación, con sus supuestos explícitos.
- El texto describe lo que muestran los números y deja la valoración al lector, como pide el protocolo.

## D-010. Valor nominal de los instrumentos CER en pesos (2026-10-15)

**Decisión.** Las operaciones sobre instrumentos ajustados por CER se cargan con el valor nominal en pesos, tal como lo publican los resultados de licitación y las resoluciones.

**Aplicación.** El saldo de esos instrumentos sigue en unidades CER, como en SIGADE. La columna `indice_inicial` de `contratos/terminos.csv` (el CER de la fecha de referencia de la emisión) convierte los pesos en unidades, y el cargador rechaza operaciones sobre instrumentos CER o UVA si falta.
