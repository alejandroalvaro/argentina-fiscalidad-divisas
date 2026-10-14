# Aportes propuestos del proyecto (borrador de Grok)

Estado: primera versión, 14 de octubre de 2026, según la decisión D-003 (`docs/DECISIONES.md`). Este documento contiene propuestas y no evidencia. Nada de lo que sigue entra en `claims.csv`. Las referencias a `SRC-` y `CLM-` remiten a los lotes de `inbox/` y siguen marcadas `sin_revisar` hasta que Claude Code y Alejandro las validen. Lo que depende de resultados todavía no calculados se indica en cada caso.

Hipótesis de referencia (`docs/protocolo/RESEARCH_PROTOCOL.md`):

- H1: previsibilidad de recursos fiscales en USD.
- H2: compras de USD contra pesos y esterilización.
- H3: matriz de obligaciones por moneda de cuenta, indexación, liquidación y residencia.
- H4: cobertura proyectada y riesgo de refinanciación.
- H5: secuencia intertemporal de importaciones de inversión y exportaciones.

## Resumen

| Aporte | Hipótesis | Precedente principal | Qué agrega el proyecto | Depende de resultados pendientes |
|---|---|---|---|---|
| 1. Regla de percepción directa en USD | H1, H2 | Determinación en USD (CLM-B-004) | Regla operativa y comparación con igual carga | Sí |
| 2. Contabilidad consolidada Tesoro y BCRA | H2, H4 | TMU del FMI (CLM-D-001 a 003) | Registro único de las divisas percibidas | Parcial |
| 3. Matriz de obligaciones | H3 | SALM y directrices (CLM-A-001, 006) | Matriz por operación con SIGADE | Parcial |
| 4. Cobertura proyectada en USD | H4 | Adecuación de reservas (CLM-A-005) | Cobertura fiscal por horizonte | Sí |
| 5. Secuencia intertemporal | H5 | Diamand y Crovetto (CLM-A-012) | Escenarios de brecha con calendario | Sí |
| 6. Modelo SFC con tres regímenes | H1 a H5 | Godley (CLM-A-010, 011) | Comparación con stocks y flujos completos | Sí |
| 7. Contraste acotado con Brasil | H3, H4 | Jerarquía monetaria (CLM-A-013) | Indicadores sintéticos comparables | Parcial |

## 1. Regla de percepción directa de derechos de exportación en divisas

**Hipótesis:** H1 y H2.

**Lo que ya existe en la norma y en la práctica.**

- Los derechos de exportación se determinan en dólares, y la Ley 23.905 admite el pago en esa moneda (CLM-B-004, SRC-0004).
- El Ministerio de Economía indica que hoy el pago se realiza en moneda nacional y que el dólar se usa solo para la determinación (CLM-B-005, SRC-0015).
- El contravalor de las exportaciones debe ingresarse y liquidarse en el mercado de cambios en los plazos que fija el BCRA (CLM-B-011, CLM-B-013, CLM-B-014).
- El BCRA puede comprar y vender divisas por cuenta del Ministerio de Economía (CLM-B-020) y recibe en depósito los fondos del gobierno (CLM-B-019).
- Existe una opción limitada para expresar en USD ciertos saldos de comercio exterior y compensarlos contra tributos aduaneros (CLM-B-006, CLM-B-007).
- Entre los precedentes internacionales del lote A figuran la gestión conjunta de deuda en moneda extranjera y reservas (CLM-A-002, SRC-0201) y los fondos de estabilización (CLM-A-008, SRC-0206). En las fuentes relevadas no se encontró un precedente explícito de percepción de derechos de exportación en divisas para el Tesoro (`inbox/lote-a/unresolved.md`). Esto se registra como un faltante de búsqueda y no permite afirmar que el precedente no exista.

**Lo que el proyecto propone.**

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

## 6. Modelo stock-flujo consistente con tres regímenes

**Hipótesis:** H1 a H5.

**Lo que ya existe.**

- Godley (1999) desarrolla modelos de economía abierta con stocks y flujos completos (CLM-A-010, CLM-A-011, SRC-0208).

**Lo que el proyecto propone.**

- Un modelo SFC que compare tres regímenes de percepción con igual carga tributaria. Separa el Tesoro, el BCRA y el sector público consolidado, y evita contar un mismo activo externo dos veces (principios del protocolo, D-001).
- Sensibilidad a exportaciones, tipo de cambio, refinanciación y shocks productivos.

**Pendiente.** Fase 4 del repositorio. Los regímenes concretos están por definir con Alejandro.

## 7. Contraste acotado con Brasil

**Hipótesis:** H3 y H4.

**Lo que ya existe.**

- Kaltenbrunner y Painceira estudian la acumulación de reservas de Brasil desde la jerarquía monetaria (CLM-A-013).
- El BCB y el Tesouro publican series de cuenta corriente, renta primaria, reservas y deuda (CLM-E-003 a CLM-E-006).

**Lo que el proyecto propone.**

- Usar indicadores sintéticos comparables y la clasificación por indexador derivada de los códigos de título. Esta clasificación no es oficial (D-002, CLM-E-010) y en 2026-07 muestra una participación cambial de 2,75% del stock de la DPF.
- Registrar las rupturas metodológicas antes de comparar, como las dos series de deuda bruta (CLM-E-001, CLM-E-002).

**Pendiente.** El cotejo con el RMD del Tesouro (`inbox/lote-e/unresolved.md`). El contraste no pretende reconstruir cada título brasileño.

## Cuestiones abiertas para Alejandro

- Cuáles son los tres regímenes del modelo SFC (aporte 6) y qué fracción del derecho se percibiría en divisas en la regla del aporte 1.
- Si conviene una búsqueda sistemática de precedentes de percepción tributaria en divisas fuera de las fuentes del lote A, antes de presentar el aporte 1 como original.
