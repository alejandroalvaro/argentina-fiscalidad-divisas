# Aportes propuestos del proyecto (borrador de Grok)

Estado: cuarta versión (15 de octubre de 2026, aporte 6 con cuatro regímenes según D-007), tercera versión (sección 8, menú de opciones), segunda versión, 14 de octubre de 2026 (atribución a Mosler, regímenes y alícuotas incorporados), primera versión del mismo día, según la decisión D-003 (`docs/DECISIONES.md`). Este documento contiene propuestas y no evidencia. Nada de lo que sigue entra en `claims.csv`. Las referencias a `SRC-` y `CLM-` remiten a los lotes de `inbox/` y siguen marcadas `sin_revisar` hasta que Claude Code y Alejandro las validen. Lo que depende de resultados todavía no calculados se indica en cada caso.

Hipótesis de referencia (`docs/protocolo/RESEARCH_PROTOCOL.md`):

- H1: previsibilidad de recursos fiscales en USD.
- H2: compras de USD contra pesos y esterilización.
- H3: matriz de obligaciones por moneda de cuenta, indexación, liquidación y residencia.
- H4: cobertura proyectada y riesgo de refinanciación.
- H5: secuencia intertemporal de importaciones de inversión y exportaciones.

## Resumen

| Aporte | Hipótesis | Precedente principal | Qué agrega el proyecto | Depende de resultados pendientes |
|---|---|---|---|---|
| 1. Percepción directa en USD (propuesta de Warren Mosler) | H1, H2 | Mosler 2022 (CLM-A-015); determinación en USD (CLM-B-004) | Formalización, modelo SFC y cuantificación | Sí |
| 2. Contabilidad consolidada Tesoro y BCRA | H2, H4 | TMU del FMI (CLM-D-001 a 003) | Registro único de las divisas percibidas | Parcial |
| 3. Matriz de obligaciones | H3 | SALM y directrices (CLM-A-001, 006) | Matriz por operación con SIGADE | Parcial |
| 4. Cobertura proyectada en USD | H4 | Adecuación de reservas (CLM-A-005) | Cobertura fiscal por horizonte | Sí |
| 5. Secuencia intertemporal | H5 | Diamand y Crovetto (CLM-A-012) | Escenarios de brecha con calendario | Sí |
| 6. Modelo SFC con cuatro regímenes | H1 a H5 | Godley (CLM-A-010, 011); fondos de estabilización (CLM-A-008, lote H) | Comparación con stocks y flujos completos | Sí |
| 7. Contraste acotado con Brasil | H3, H4 | Jerarquía monetaria (CLM-A-013) | Indicadores sintéticos comparables | Parcial |

## 1. Percepción directa de derechos de exportación en divisas (propuesta de Warren Mosler)

**Atribución.** La idea de cobrar los derechos de exportación directamente en dólares corresponde a Warren Mosler. En su presentación de Buenos Aires del 1 de mayo de 2022 propone "A 3% export tax payable in $US" para servir la deuda con el FMI (CLM-A-015, SRC-0212, fuente primaria en moslereconomics.com). En una entrevista de El Argentino Diario del 4 de mayo de 2022 formula la misma propuesta de un 3% sobre las exportaciones brutas, sin mencionar la moneda (CLM-A-016, SRC-0213, fuente secundaria). Este aporte se registra como precedente de Mosler y el proyecto no lo presenta como idea propia.

**Hipótesis:** H1 y H2.

**Lo que ya existe en la norma y en la práctica.**

- Los derechos de exportación se determinan en dólares, y la Ley 23.905 admite el pago en esa moneda (CLM-B-004, SRC-0004).
- El Ministerio de Economía indica que hoy el pago se realiza en moneda nacional y que el dólar se usa solo para la determinación (CLM-B-005, SRC-0015).
- El contravalor de las exportaciones debe ingresarse y liquidarse en el mercado de cambios en los plazos que fija el BCRA (CLM-B-011, CLM-B-013, CLM-B-014).
- El BCRA puede comprar y vender divisas por cuenta del Ministerio de Economía (CLM-B-020) y recibe en depósito los fondos del gobierno (CLM-B-019).
- Existe una opción limitada para expresar en USD ciertos saldos de comercio exterior y compensarlos contra tributos aduaneros (CLM-B-006, CLM-B-007).
- Precedentes de percepción en moneda dura o divisas (`inbox/lote-a/unresolved.md`, clasificación provisional): derechos de importación en coin en EE.UU. 1862 (CLM-A-017); regalías e IDH pagaderos en USD a elección del beneficiario en Bolivia (CLM-A-019); contraprestaciones contractuales en USD al Fondo Mexicano del Petróleo (CLM-A-020). Como contraste, Noruega cobra los impuestos petroleros en NOK y recibe divisas por la participación estatal SDFI (CLM-A-018), y Venezuela 2003 impuso la venta obligatoria de divisas al BCV, que corresponde a un requisito de entrega y no a un tributo (CLM-A-021). Chile (Ley 13.196), Rusia, Argentina 1890, Botswana, la Aduana Marítima China, la Deuda Pública Otomana, el Golfo y Ecuador siguen pendientes.
- Otros precedentes del lote A: gestión conjunta de deuda en moneda extranjera y reservas (CLM-A-002) y fondos de estabilización (CLM-A-008).
- Alícuotas vigentes al 2026-10-14 (Decreto 423/2026, `inbox/lote-f/tablas/alicuotas_de_vigentes_2026-10-14.csv`): soja en grano 24%, aceite y harina de soja 22,5%, maíz y sorgo 8,5%, girasol 4,5%, biodiésel de soja 21%, trigo 1% o 5,5% según posición; cronograma de reducción mensual en 2027 y 2028. La fracción percibida en divisas sería igual a esas alícuotas (indicación de Alejandro).

**Lo que agrega el proyecto.** Formalización, modelización SFC y cuantificación de la propuesta de Mosler.

- Formular una regla operativa en la que una fracción del derecho determinado en USD se perciba en divisas y se acredite en una cuenta del Tesoro. Compararla con el cobro en pesos con igual carga tributaria efectiva, como exige el protocolo.
- Separar el permiso legal de la habilitación operativa. El lote B advierte que un permiso legal no implica que el circuito de pago exista (por ejemplo, los medios de pago de CLM-B-008).

**Pendiente.** La medida en que la regla eleva la previsibilidad de los recursos en USD depende de series de exportaciones y de cumplimiento todavía no modeladas. Las dos series oficiales de derechos de exportación difieren mes a mes (CLM-D-009), y antes de estimar habría que conciliarlas.

## 2. Contabilidad consolidada de las divisas percibidas

**Hipótesis:** H2 y H4.

**Lo que ya existe.**

- La definición de reservas netas del TMU resta swaps, encajes en divisas, SEDESA, ALADI y depósitos de no residentes, y no resta los depósitos en divisas del Tesoro en el BCRA (CLM-D-001 a CLM-D-003, SRC-0312). El proyecto la adoptó en D-001.
- El FMI define las reservas como activos disponibles y controlados por las autoridades monetarias (CLM-A-004, SRC-0202).
- Los encajes en moneda extranjera se integran en cuentas en el BCRA (CLM-B-022), lo que explica que se resten.

**Lo que el proyecto propone.**

- Registrar las divisas percibidas por el Tesoro una sola vez, como reservas en la consolidación Tesoro y BCRA, y como activo del Tesoro y pasivo del BCRA en la presentación separada, según D-001.
- Llevar en paralelo las otras definiciones de reservas netas, cada una con su nombre (`inbox/lote-d/tablas/definiciones_reservas.csv`), sin mezclarlas.

**Pendiente.** No hay serie oficial de reservas netas, y la única serie de depósitos del Gobierno Nacional en el BCRA está en pesos, mezcla conceptos y termina en 2025-10 (`inbox/lote-d/unresolved.md`). El efecto sobre la esterilización (H2) queda sin cuantificar.

## 3. Matriz de obligaciones por moneda de cuenta, indexación, liquidación y residencia

**Hipótesis:** H3.

**Lo que ya existe.**

- Las directrices de gestión de deuda incluyen un enfoque de activos y pasivos y advierten sobre la deuda en moneda extranjera o indexada al tipo de cambio sin cobertura (CLM-A-001, CLM-A-003, SRC-0201).
- El FMI propone un marco SALM para detectar exposiciones desde una perspectiva de cartera (CLM-A-006, SRC-0204).
- La literatura sobre pecado original (CLM-A-009) y sobre bonos indexados (CLM-A-007) ofrece categorías para la moneda y la indexación.
- Los cuadros oficiales separan moneda local, ajustable por CER y moneda extranjera (CLM-C-006), y residencia del tenedor solo en agregado (CLM-C-009).

**Lo que el proyecto propone.**

- Una matriz por operación construida desde SIGADE (`inbox/lote-c/instruments.csv`, CLM-C-002, CLM-C-015). Distingue la moneda de cuenta de la moneda de pago, por ejemplo instrumentos dólar-linked con saldo en USD pagaderos en pesos y CER en unidades ajustables (`inbox/lote-c/unresolved.md`, puntos resueltos). Incluye además duales, garantías y letras en garantía (CLM-C-010).
- Mostrar exposiciones que los agregados no separan, como la parte de la deuda en moneda local que depende del tipo de cambio.

**Pendiente.** Faltan la ISIN y la residencia por operación (`inbox/lote-c/unresolved.md`). Hasta completarlas, la dimensión de residencia de la matriz queda incompleta. Ningún riesgo se presenta todavía como hallazgo.

## 4. Cobertura proyectada de obligaciones en USD

**Hipótesis:** H4.

**Lo que ya existe.**

- La métrica de adecuación de reservas del FMI pondera ingresos de exportación, deuda de corto plazo, otros pasivos de cartera y dinero amplio (CLM-A-005, SRC-0203).
- Algunos países financian reservas con deuda en moneda extranjera de composición similar (CLM-A-002).
- Los fondos de estabilización son una práctica reconocida (CLM-A-008).

**Lo que el proyecto propone.**

- Un indicador de cobertura fiscal en USD por horizonte: mensual de 0 a 36 meses y anual de 4 a 20 años, como fija el protocolo. Compara los recursos en USD proyectados bajo la regla del aporte 1 con el calendario de servicios en USD de SIGADE (CLM-C-011).
- Tratar la relación con el riesgo de refinanciación como una pregunta. El protocolo excluye atribuir causalidad sobre los spreads sin identificación empírica.

**Pendiente.** El indicador requiere el motor de flujos (fase 2) y escenarios de exportaciones. No hay resultados.

## 5. Secuencia intertemporal de importaciones de inversión y exportaciones

**Hipótesis:** H5.

**Lo que ya existe.**

- Diamand y Crovetto distinguen la limitación por insuficiencia de ahorro de la limitación por insuficiencia de divisas (CLM-A-012, SRC-0209).
- La literatura de jerarquía monetaria vincula la posición subordinada de las monedas periféricas con la acumulación de reservas y la vulnerabilidad externa (CLM-A-013, CLM-A-014).

**Lo que el proyecto propone.**

- Escenarios que ordenan en el tiempo las importaciones de inversión y las exportaciones que esa inversión podría generar, y que miden cómo cambia la brecha externa bajo cada régimen de percepción.
- Las excepciones a la obligación de liquidar, por ejemplo para el RIGI (CLM-B-016), entran como un supuesto explícito en los escenarios.

**Pendiente.** Todo el aporte depende de escenarios no construidos. Los cobros de exportaciones (caja) y las exportaciones FOB (devengado) son conceptos distintos (CLM-D-011), y la elección de cada uno se documentará.

## 6. Modelo stock-flujo consistente con cuatro regímenes

**Hipótesis:** H1 a H5.

**Lo que ya existe.**

- Godley (1999) desarrolla modelos de economía abierta con stocks y flujos completos (CLM-A-010, CLM-A-011, SRC-0208).

**Lo que el proyecto propone.**

- Un modelo SFC que compare cuatro regímenes de percepción con igual carga tributaria. Separa el Tesoro, el BCRA y el sector público consolidado, y evita contar un mismo activo externo dos veces (principios del protocolo, D-001).
- Sensibilidad a exportaciones, tipo de cambio, refinanciación y shocks productivos.

**Regímenes (definidos por Alejandro, comparación en `inbox/lote-f/tablas/regimenes_comparados.csv`):**

- (a) Argentina actual: derechos determinados en USD, pagados en pesos, con obligación de liquidar divisas de exportación según el BCRA.
- (b) Brasil: los exportadores venden divisas en el mercado de cambio a instituciones autorizadas por el BCB, a tipo libremente pactado, y pueden mantenerlas en el exterior (CLM-F-008, CLM-F-009). El imposto de exportação existe pero alcanza a pocos productos y se paga en reales (CLM-F-012 a CLM-F-014).
- (c) Propuesta (Mosler): derechos percibidos directamente en USD para el Tesoro.
- (d) Dólares con fondo de estabilización (D-007): como (c), con un fondo de estabilización que acumula parte de lo percibido. Las reglas del fondo (qué ingresos acumula, con qué regla se retira, si tiene tope y quién decide su uso) las decide Alejandro. El relevamiento de fondos comparables (Chile FEES, Noruega, Colombia FAE y Perú FEF) y sus opciones están en `inbox/lote-h/` (`tablas/fondos_comparacion.csv`, `tablas/opciones_diseno_fondo_d.csv`), todo `sin_revisar` y sin recomendación.

**Pendiente.** Fase 4 del repositorio.

## 7. Contraste acotado con Brasil

**Hipótesis:** H3 y H4.

**Lo que ya existe.**

- Kaltenbrunner y Painceira estudian la acumulación de reservas de Brasil desde la jerarquía monetaria (CLM-A-013).
- El BCB y el Tesouro publican series de cuenta corriente, renta primaria, reservas y deuda (CLM-E-003 a CLM-E-006).

**Lo que el proyecto propone.**

- Usar indicadores sintéticos comparables y la clasificación por indexador derivada de los códigos de título. Esta clasificación no es oficial (D-002, CLM-E-010) y en 2026-07 muestra una participación cambial de 2,75% del stock de la DPF.
- Registrar las rupturas metodológicas antes de comparar, como las dos series de deuda bruta (CLM-E-001, CLM-E-002).

**Pendiente.** El cotejo con el RMD del Tesouro (`inbox/lote-e/unresolved.md`). El contraste no pretende reconstruir cada título brasileño.

## 8. Menú de opciones para el resto de las divisas de exportación

**Contexto.** Alejandro planteó (14 de octubre de 2026) qué hacer con las divisas que quedan al exportador después de pagar el derecho en USD. Había pensado en venderlas en el MULC a tipo libre con el Estado como creador de mercado, y duda de que convenga aplicar principios de libre mercado a un activo estratégico en un país periférico con escasez de divisas. Esta sección ofrece un menú de opciones con su literatura. No contiene una recomendación. Los efectos se citan solo como los informan las fuentes, sin cifras propias, y todo queda sin_revisar.

Fuentes del FMI no descargadas: el Integrated Policy Framework (2020) y la Institutional View (2012, revisión 2022) no se pudieron descargar (imf.org devolvió 403). Lo que se cita de ellos proviene del comunicado de prensa 22/97 de 2022, leído en línea, sin archivo ni sha256 (`inbox/lote-a/unresolved.md`).

| Opción | Mecanismo | Literatura y precedentes | Régimen del modelo SFC |
|---|---|---|---|
| 1. Liquidación total en el MULC con BCRA o Tesoro como creador de mercado | El exportador vende todo el resto en el mercado de cambios; la autoridad cotiza o respalda precios como operador de última instancia | Mehrling (CLM-A-024); Mosler sobre flotación (CLM-A-029) | Variante de (a) con percepción en USD de (c); también variante de (d) si parte del contravalor se acumula en el fondo |
| 2. Liquidación parcial (tipo blend) | Una fracción por el MULC y otra por un canal de valores negociables | DNU 28/2023, 80/20 (CLM-A-023); AREAER sobre tipos múltiples y dólar soja (CLM-A-022) | Variante de (a), (c) o (d) con dos precios |
| 3. Retención por el exportador con libre uso | El exportador decide cuándo y dónde vender, como en Brasil | Lei 14.286/2021 (CLM-F-008, CLM-F-009) | (b), combinable con (c) y (d) |
| 4. Asignación prioritaria a importaciones estratégicas | Divisas entregadas al Estado o vinculadas a exportaciones se destinan con prioridad a bienes de capital e insumos | Corea 1963-1964 (CLM-A-026); Prebisch (CLM-A-028); Diamand y Crovetto (CLM-A-012) | (c) o (d) con un bloque de asignación |
| 5. Medidas prudenciales sobre flujos de capital, sobre 1 o 3 | Encaje no remunerado a ingresos de capital u otras medidas de cuenta de capital | Chile 1991-1998 (CLM-A-025); Ocampo (CLM-A-027); FMI, revisión de la IV de 2022 (comunicado) | Capa sobre (a), (b), (c) o (d) |

### Opción 1. Liquidación total en el MULC con creador de mercado

- **Mecanismo.** El resto del contravalor se liquida en el mercado de cambios. El BCRA o el Tesoro actúa como creador de mercado en un esquema híbrido: los operadores privados hacen el comercio diario y la autoridad sostiene la liquidez en los extremos (Mehrling, CLM-A-024, SRC-0221).
- **Literatura.** Mehrling distingue tres casos: banco central que fija el precio y absorbe todo el flujo, banco central que se abstiene, y el caso híbrido de operador de última instancia. Mosler (2022) sostiene que el pleno empleo solo puede sostenerse con tipo de cambio flotante y que la flotación conserva reservas (CLM-A-029, SRC-0212).
- **Efectos según las fuentes.** Mosler asocia la flotación a la conservación de reservas. Sobre traspaso a precios e importaciones de inversión, las fuentes de esta tanda no informan efectos para Argentina.
- **Riesgos señalados en la literatura.** El comunicado del FMI de 2022 menciona riesgos sistémicos por descalces de moneda ante reversiones de flujos. Prebisch y Diamand describen la restricción de divisas como límite al crecimiento, lo que sugiere tensión con una venta íntegra a precio de mercado en períodos de escasez (interpretación, sin_revisar).

### Opción 2. Liquidación parcial (tipo blend)

- **Mecanismo.** Una fracción se liquida en el MULC y otra por un canal alternativo con otro precio. El DNU 28/2023 fijó 80% por el MLC y 20% mediante compraventa de valores negociables (CLM-A-023, SRC-0220). Según InfoLeg, el DNU 269/2025 lo derogó en abril de 2025 (sin archivo descargado).
- **Literatura.** El AREAER del FMI registra como prácticas de tipos de cambio múltiples los casos en que los tipos difieren en más de 2%, y describe el tipo preferencial para exportadores de soja en Argentina (CLM-A-022, SRC-0219).
- **Efectos según las fuentes.** El AREAER clasifica estos esquemas como prácticas de tipos múltiples sujetas al marco del FMI. No se relevaron evaluaciones del efecto del blend sobre reservas o precios.
- **Riesgos.** Clasificación como práctica de tipos múltiples; brecha entre precios; posibles incentivos a cambiar el momento de liquidar (este último punto es una inferencia y no proviene de las fuentes).

### Opción 3. Retención por el exportador con libre uso (tipo Brasil)

- **Mecanismo.** El exportador puede mantener las divisas en el exterior y venderlas cuando quiera a instituciones autorizadas, a tipo libremente pactado (Lei 14.286/2021, CLM-F-008, CLM-F-009).
- **Literatura.** Kaltenbrunner y Painceira estudian la integración financiera subordinada de Brasil y la acumulación de reservas desde la jerarquía monetaria (CLM-A-013).
- **Efectos según las fuentes.** Las fuentes de esta tanda no cuantifican efectos sobre reservas o traspaso a precios. En el modelo, las divisas del exportador quedarían fuera de las reservas salvo que se vendan al sistema.
- **Riesgos.** Kaltenbrunner y Painceira y Orsi y otros (CLM-A-014) asocian la internacionalización de monedas periféricas con vulnerabilidad externa. Es un argumento de los autores, sin_revisar.

### Opción 4. Asignación prioritaria a importaciones estratégicas

- **Mecanismo.** Una parte de las divisas, ya sea entregada al Estado o vinculada a la exportación, se asigna con prioridad a bienes de capital e insumos para la inversión.
- **Literatura y precedentes.** Irwin documenta que Corea reintrodujo en 1963 un vínculo exportación-importación en el que los exportadores recibían derechos no transferibles para usar parte de sus divisas en importaciones. El sistema se canceló a fines de 1964 dentro de una simplificación del régimen de asignación (CLM-A-026, SRC-0223). Prebisch (1949) plantea reducir importaciones no esenciales para ampliar las de bienes de capital (CLM-A-028, SRC-0225). Diamand y Crovetto tratan la limitación por insuficiencia de divisas (CLM-A-012). Amsden y Wade, autores centrales de la literatura del Estado desarrollista, no se descargaron (libros sin acceso abierto).
- **Efectos según las fuentes.** Según el resumen de Irwin, el aumento de las exportaciones coreanas siguió a cambios de política cambiaria y comercial a mediados de los sesenta, incluida una devaluación y una reforma del régimen de divisas impulsadas por presión de EE.UU.; el vínculo exportación-importación aparece como una etapa transitoria. Las fuentes no aportan cifras de efecto sobre la inversión que puedan trasladarse a Argentina.
- **Riesgos.** El AREAER trataría los tipos o accesos diferenciados como restricciones o prácticas múltiples. Las fuentes de esta tanda no documentan riesgos de captura o de discrecionalidad, aunque son habituales en la literatura (punto pendiente de fuente).

### Opción 5. Medidas prudenciales sobre flujos de capital (sobre 1 o 3)

- **Mecanismo.** Encaje no remunerado u otras medidas sobre ingresos de capital, superpuestos a la opción 1 o a la 3.
- **Literatura y precedentes.** De Gregorio, Edwards y Valdés evalúan el encaje chileno de 1991 a 1998. Encuentran efectos de largo plazo difíciles de identificar sobre tasas y tipo de cambio, y un efecto más persistente sobre la composición de los ingresos de capital, hacia mayor plazo (CLM-A-025, SRC-0222). Ocampo trata la regulación de la cuenta de capital como instrumento contracíclico y macroprudencial (CLM-A-027, SRC-0224). Según el comunicado del FMI de 2022, la revisión de la IV admite medidas preventivas sobre ingresos de deuda cuando hay descalces de moneda elevados.
- **Efectos según las fuentes.** Cambio de composición hacia mayor plazo en Chile; efectos pequeños o no significativos sobre el tipo de cambio real.
- **Riesgos.** Elusión (los autores describen una disputa continua entre autoridades y sector privado) y la condición del FMI de que estas medidas no sustituyan un ajuste macroeconómico necesario.

### Compatibilidad con el modelo de cuatro regímenes

Las cinco opciones se pueden representar como variantes del régimen (c): todas suponen que el derecho se percibe en USD y difieren en el destino del resto. El régimen (d) agrega a (c) un fondo de estabilización, por lo que cada variante puede tener una versión con fondo según la fracción del contravalor que se acumule; las reglas del fondo siguen abiertas. Las opciones 1 y 2 se acercan al régimen (a) y la 3 al (b). La 4 requiere un bloque de asignación de divisas por tipo de importación, y la 5 una ecuación de flujos de capital con un parámetro de encaje.

### Brechas de esta sección

- Kregel y Vernengo: no se descargó texto propio.
- FMI, IPF e IV: sin archivo (403).
- Evaluaciones del blend 2023-2025 sobre reservas y precios: no relevadas.
- Ninguna fuente de esta tanda informa efectos cuantitativos sobre el traspaso a precios en Argentina.

## Cuestiones abiertas para Alejandro

- Resueltas el 2026-10-14 y 2026-10-15: regímenes del aporte 6 (arriba, cuatro regímenes según D-007), fracción en divisas igual a las alícuotas vigentes, y atribución del aporte 1 a Mosler.
- Destino del resto del contravalor en el régimen (c): Alejandro pidió un menú de opciones (sección 8), sin decisión todavía.
- Cómo tratar los sectores no relevados en la tabla de alícuotas (carnes, economías regionales, industria, minería) y el crudo con alícuota móvil.
- Si se busca contacto o permiso para citar a Mosler más allá de sus textos públicos (no se hizo ningún contacto).
- Reglas del fondo del régimen (d): ingresos que acumula, regla de retiro, tope y quién decide. Opciones y precedentes en `inbox/lote-h/tablas/opciones_diseno_fondo_d.csv`, sin recomendación.
