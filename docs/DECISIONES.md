# Decisiones del investigador

Registro de las definiciones metodológicas que tomó Alejandro. Cada una indica la fecha, la fuente que la sostiene y cómo se aplica en el código.

## D-001. Reservas netas: definición del FMI (2026-10-14)

**Decisión.** El trabajo usa la definición de reservas internacionales netas del TMU del acuerdo EFF (FMI, Country Report 26/105, párr. 11, SRC-0312).

- Reservas brutas: activos líquidos del BCRA frente a no residentes en moneda convertible (BPM6).
- Se restan: pasivos en divisas con vencimiento original de hasta un año, compras netas al FMI desde el inicio del programa, forwards netos, swaps (PBOC, BIS, ESF), encajes en moneda extranjera, SEDESA, ALADI y depósitos de no residentes.
- **No se restan los depósitos en divisas del Tesoro en el BCRA.** Texto del TMU: "Neither the Federal government's foreign liabilities nor its FX deposits at the BCRA are considered as gross foreign liabilities of the BCRA."
- El TMU de la segunda revisión (informe del personal técnico del FMI de mayo de 2026, SRC-1263, p. 117 del PDF) mantiene esa definición y la misma frase (verificado el 2026-10-15). Las tenencias de DEG del BCRA suman a los activos; los depósitos del Tesoro en DEG solo se informan. Según el lote Y, el núcleo de la definición es el mismo en el acuerdo de abril de 2025 y en la primera revisión (agosto de 2025, SRC-1270), así que D-001 vale para todo el programa.

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
- `argfx devengados` (2026-10-16): interés capitalizado neto de lo que traen las ampliaciones, descuentos y primas de colocación repartidos hasta el vencimiento, y la tenencia del FGS acotada por categoría para el perímetro del SPN. Ver `docs/FASE3_CONCILIACION.md`.
- La comparación de costo usa las tasas de las licitaciones y se presenta como estimación, con sus supuestos explícitos.
- El texto describe lo que muestran los números y deja la valoración al lector, como pide el protocolo.

## D-010. Valor nominal de los instrumentos CER en pesos (2026-10-15)

**Decisión.** Las operaciones sobre instrumentos ajustados por CER se cargan con el valor nominal en pesos, tal como lo publican los resultados de licitación y las resoluciones.

**Aplicación.** El saldo de esos instrumentos sigue en unidades CER, como en SIGADE. La columna `indice_inicial` de `contratos/terminos.csv` (el CER de la fecha de referencia de la emisión) convierte los pesos en unidades, y el cargador rechaza operaciones sobre instrumentos CER o UVA si falta.

## D-011. Letras en garantía del FODER: deuda contingente en poder del sector público (2026-10-16)

**Decisión.** Las 109 "LETRAS EN GARANTÍA" de SIGADE (USD 3.774 millones al 30-06-2026) se tratan como deuda contingente, igual que los avales, y como tenencia del sector público.

**Fundamento.**
- El Tesoro emite estas letras y las entrega al FODER como garantía del pago del precio de venta de las centrales de energías renovables. Solo hay que pagar si un generador ejerce la opción de venta (Decreto 882/2016, art. 14, verificado en el texto oficial, SRC-1279; Ley 27.191, art. 7).
- Si no se ejerce, vencen cada 31 de diciembre y vuelven al fiduciante sin pago (Decreto 471/2017, art. 3; OPC, Análisis de la Deuda Pública Indirecta, SRC-1286, lote Z).
- El FODER es un fideicomiso con el Estado Nacional como fiduciante y fideicomisario.
- SIGADE las registra en deuda en situación de pago normal, con un calendario mecánico de USD 266 millones por año. Eso es una decisión de registro, no un compromiso de pago.

**Aplicación.**
- `src/argfx/contracts/sigade.py`: sus flujos salen con `status = contingente` y quedan fuera de la necesidad firme de divisas. La necesidad bruta a 12 meses baja de 22.411 a 22.145 millones de USD.
- `scripts/build_tenencias.py`: figuran como tenencia `directo` del FODER en la consolidación.
- No se encontró evidencia de que se haya ejercido alguna opción de venta. Si apareciera, el tramo ejecutado pasa a firme.
- Lo emitido (7.417 millones) baja hasta el saldo de SIGADE (3.774 millones) en ocho bajas registradas en la planilla trimestral de Finanzas (A.1.2 y A.2.2, línea "Letras en garantía", lote AA), siete en cuartos trimestres. Son compatibles con vencimientos anuales sin pago, aunque la planilla no dice la causa. La baja de junio de 2026 (318 millones) no tiene explicación.


## D-012. Fondo de estabilización del régimen (d): configuración base (2026-10-16)

**Origen.** Alejandro pidió la configuración que mejor sirva al objetivo, no una preferencia suya. Esta es la configuración base, armada con los precedentes del lote H. La fase 4 la contrasta con sus variantes y con el régimen (c) sin fondo, y se confirma o se corrige con esos resultados.

**Objetivo del fondo en este trabajo.** Los derechos llegan con la cosecha y varían mucho de un mes a otro y de un año a otro. Los pagos en divisas se concentran en enero y julio. El fondo existe para convertir un ingreso volátil y estacional en un flujo previsible para el Tesoro, que es lo que mide H1.

**Configuración base.**
- **Ingresos: regla de referencia.** Cada mes, el Tesoro recibe una transferencia fija igual a la doceava parte de la recaudación de referencia: el promedio de los derechos en dólares de los últimos cinco años, recalculado con las alícuotas vigentes para que una rebaja decretada no infle la referencia. Lo que entra por encima de esa referencia va al fondo. Precedentes: el promedio móvil de seis años de Colombia (CLM-H-016, CLM-H-017) y la pauta de rendimiento de Noruega (CLM-H-011).
- **Retiros: automáticos y por fórmula.** Si en un mes entra menos que la referencia, el fondo completa la diferencia. Ante una caída de la recaudación anual de 20% o más (sequía, precios), el fondo puede adelantar hasta el pago en divisas del semestre siguiente. No hay retiros discrecionales. Precedente: el disparador del 20% de Colombia.
- **Tope: en meses de servicio.** Cuando el saldo supera doce meses del servicio en divisas a acreedores fuera del sector público (la necesidad consolidada de la fase 3), el excedente se destina a cancelar deuda en divisas. Precedente: el umbral de 4% del PBI de Perú, que habilita destinar el exceso a deuda (CLM-H-020, CLM-H-021), medido aquí en la unidad que importa para el problema.
- **Rendimientos:** quedan en el fondo, como en Chile y Noruega.
- **Custodia:** depósito en dólares del Tesoro en el BCRA, separado por ley. Cuenta una sola vez, como reservas (D-001).
- **Gobierno:** la ley fija las fórmulas, un directorio con Economía, el BCRA y la Jefatura de Gabinete administra (como el FEF de Perú) y el Congreso es el único que puede cambiar las reglas. Publicación mensual del saldo y de los movimientos, como piden los Principios de Santiago (CLM-H-027 a CLM-H-029).

**Variantes que la fase 4 contrasta:** referencia de tres, cinco o seis años; tope de seis, doce o dieciocho meses; retiro solo por fórmula frente a fórmula más disparador; y el régimen (c) sin fondo. El criterio para elegir son las medidas de `docs/FASE4_DISENO.md` (meses con faltante, dispersión del ingreso del Tesoro, compras de divisas con pesos), sin fijar de antemano cuál gana.

## D-013. Destino del resto de las divisas del exportador: configuración base (2026-10-16)

**Origen.** Alejandro pidió la opción que no desaliente al exportador a liquidar y traer las divisas, y que no afecte la caja del Estado.

**Punto de partida.** En los regímenes (c) y (d) la caja del Tesoro ya queda cubierta con el derecho cobrado en dólares, sea cual sea el destino del resto. Lo que se decide aquí afecta las reservas del BCRA y el mercado de cambios, no la recaudación.

**Qué desalienta a liquidar, según los precedentes:**
- la brecha entre el tipo de cambio oficial y otro precio disponible;
- los tipos diferenciales transitorios, que enseñan a esperar el próximo programa. El dólar soja anticipó liquidaciones grandes y concentradas (CLM-AD-019 a CLM-AD-022), y la ventana de 0% de 2025 adelantó pagos y DJVE (CLM-AD-011, CLM-AD-012);
- la obligación de vender a un precio que el exportador considera atrasado.

**Configuración base: opción 1 del menú, con tipo de cambio único.**
- **Tipo único.** El resto se liquida en el mercado de cambios a un tipo único, sin desdoblamiento ni blend, y el BCRA actúa como creador de mercado de última instancia (Mehrling, CLM-A-024).
- **Plazos estables.** Rigen los plazos de liquidación vigentes (lote B), sin programas transitorios ni alícuotas que cambien de un mes a otro, porque la expectativa de un cambio es lo que demora la liquidación.
- **Previsibilidad de la alícuota.** El derecho se fija al registrar la DJVE (Ley 21.453) y se paga en dólares al embarque. Cuanto más previsible es la alícuota, menos sentido tiene esperar.

**Por qué no las otras como base:**
- el blend (opción 2) crea dos precios, cuenta para el FMI como práctica de tipos múltiples (CLM-A-022) e invita a elegir el momento;
- la retención tipo Brasil (opción 3) le da al exportador la mayor libertad, pero deja fuera del país las divisas que no vende, justo en los momentos de tensión;
- la asignación a importaciones (opción 4) y las medidas sobre flujos de capital (opción 5) quedan como capas opcionales.

**Variantes que la fase 4 contrasta:** la opción 3 (que equivale al régimen (b) para el resto) y la opción 2, con el mismo criterio de D-012. El efecto de la brecha sobre la liquidación entra como parámetro de comportamiento, rotulado como supuesto mientras no haya una estimación con fuente.

## D-014. Sectores sin alícuota relevada (2026-10-16)

**Decisión.** Antes de decidir cómo tratarlos, se relevan las alícuotas vigentes de todos los sectores y su historia desde 2018 (pedido del lote AF a Grok). Hasta entonces sigue D-005: los sectores sin alícuota quedan fuera del modelo, y cada salida informa qué fracción de las exportaciones cubre.

## D-015. La pregunta es el costo de la esterilización y quién lo cobra (2026-10-16)

**Origen.** Alejandro corrigió la pregunta: "no estamos probando si cobrar retenciones en dólares hace más previsible la liquidez del Tesoro (...) Lo que estamos probando es si eliminar la esterilización evita la emisión de pasivos en pesos que luego hay que remunerar con más emisión o con superávits fiscales que ahorcan el presupuesto nacional. Quién gana con la esterilización? Ese es el número. La liquidez del Tesoro depende del flujo de dólares y no del mecanismo, que lo que genera es un costo (un flujo negativo de pesos para el Tesoro o el Central, un flujo positivo para el sector bancario)".

**Decisión.** La pregunta principal pasa a ser: cuando los derechos de exportación se cobran en pesos y el sector público compra después los dólares con pesos, ¿cuántos pasivos remunerados en pesos se emiten para esterilizar esas compras, cuánto cuestan sus intereses, quién los paga (Tesoro o BCRA) y quién los cobra? Y, frente a eso, ¿cuánto de ese costo evita cobrar los derechos directamente en dólares (D-006)? La pregunta anterior, sobre la previsibilidad de la liquidez del Tesoro, queda en `docs/protocolo/RESEARCH_PROTOCOL.md` como antecedente.

**Consecuencias.**
- **La medida central es un flujo de pesos.** Los intereses de los pasivos remunerados que nacen de comprar divisas con pesos: pases y LEFI del BCRA, y LECAP, BONCAP y demás deuda del Tesoro colocada para conseguir los pesos con que compra los dólares. Se mide por pagador y por tenedor (bancos, fondos comunes, resto), con la base devengada de D-009.
- **La liquidez en dólares pasa a ser contexto.** El flujo de dólares es el mismo con cualquier mecanismo. La cobertura de vencimientos, los meses con faltante y el fondo de D-012 se siguen calculando, pero ya no deciden entre regímenes.
- **La equivalencia contable se muestra, no se supone.** Si el exportador paga el derecho en pesos al Tesoro y el Tesoro usa esos mismos pesos para comprarle los dólares al BCRA, (a) y (c) terminan con la misma base monetaria y las mismas reservas, porque el pago del derecho absorbe los pesos que el BCRA emitió al comprar esa parte de las divisas. El costo aparece cuando la secuencia se corta: el Tesoro gasta los pesos del derecho, el BCRA esteriliza lo que emitió y el Tesoro después necesita otros pesos, de superávit o de deuda remunerada, para comprar los dólares. El modelo tiene que mostrar en qué secuencia se produce el costo y estimar con datos cuál se dio en 2024 a 2026, sin dar por hecho que siempre aparece.
- **Datos que pasan a ser prioritarios.** Los pasivos remunerados del BCRA y sus intereses, la deuda en pesos del Tesoro por tenedor y las compras de divisas del Tesoro con su fuente de pesos (lote AI).
