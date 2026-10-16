# Fase 4: diseño de la simulación

Borrador del 16-10-2026, antes de escribir el código. Fija qué se mide, cómo se arma el modelo, qué datos usa y qué decisiones siguen abiertas. Lo que dice el protocolo (`docs/protocolo/CLAUDE_CODE_TASKS.md`, fase 4) y D-007 prevalece sobre este documento.

## 1. Qué se mide

La comparación es entre regímenes con la misma carga tributaria: el mismo derecho en dólares (alícuota por valor FOB) en todos. Cambian la moneda en que se paga, el momento y el destino de las divisas. Cada corrida produce, mes a mes:

| Medida | Hipótesis | Qué responde |
|---|---|---|
| Ingresos del Tesoro en divisas y su dispersión | H1 | Cuánto entra, cuándo y con qué variabilidad |
| Cobertura de la necesidad firme en divisas (calendario de la fase 2, neto de pagos dentro del sector público) | H1, H4 | Qué parte de los pagos se cubre sin comprar divisas |
| Meses con faltante: depósitos del Tesoro en divisas menores que los pagos del mes | H1 | La previsibilidad vista desde la caja |
| Compras de divisas del Tesoro con pesos, y pesos emitidos o esterilizados por esas compras | H2 | El costo en pesos de conseguir los dólares |
| Reservas netas con la definición del FMI (D-001), Tesoro y BCRA por separado y consolidados | H2, H4 | Que ningún dólar se cuente dos veces |
| Brecha de refinanciación en divisas: pagos menos ingresos | H4 | Lo que queda por refinanciar, sin atribuir efectos sobre el riesgo país |

## 2. Cómo se arma

**Dos capas, en este orden.**

1. **Capa contable.** Un simulador mensual que respeta stocks y flujos: cada flujo tiene contrapartida y cada balance cierra. Sectores: Tesoro, BCRA, exportadores, resto del sector privado y resto del mundo. Instrumentos: base monetaria, depósitos del Tesoro en el BCRA (en pesos y en divisas), reservas, pasivos remunerados del BCRA, deuda del Tesoro en pesos y en divisas. Exportaciones, precios y tipo de cambio entran como trayectorias de escenario, sin reacción a la política. Esta capa alcanza para H1 y para buena parte de H2, con pocos supuestos.
2. **Capa de comportamiento.** Agrega respuestas: cuándo paga el exportador según la alícuota esperada (el adelantamiento de 2025 que describe ARCA, CLM-AD-012), cuánto liquida y cuándo, y cuánto compra el BCRA. Entra como sensibilidad sobre la capa contable, y cada parámetro lleva su fuente o queda rotulado como supuesto.

**El calendario de pagos viene de la fase 2.** No se proyectan emisiones como si fueran contratos (D-008). La refinanciación es una dimensión del escenario: los organismos renuevan o no, hay acceso al mercado o no.

## 3. Mecánica de cada régimen

Las tres fechas del lote AD ordenan el mes: la DJVE fija la alícuota, el embarque es el hecho imponible y abre el plazo de pago (15 días corridos en el caso general, RG 4852/2020), y la liquidación de divisas sigue los plazos del BCRA (lote B).

- **(a) Pesos, régimen actual.** El derecho se determina en dólares y se paga en pesos al tipo de cambio del día. El exportador liquida todas sus divisas. Si el BCRA las compra, emite pesos. Para pagar deuda en divisas, el Tesoro compra dólares con sus pesos (en 2026, USD 6.875 millones al BCRA hasta julio, CLM-AD-023).
- **(c) Dólares, la propuesta de Mosler.** El derecho se paga en dólares a una cuenta del Tesoro en el BCRA, y el exportador liquida solo el resto. La recaudación en dólares es la misma que en (a).
- **(d) Dólares con fondo de estabilización.** Como (c), y una parte entra a un fondo con reglas de acumulación y de uso, que todavía no están definidas.
- **(b) Brasil, contraste acotado.** El exportador no está obligado a liquidar y el derecho, cuando existe, se paga en moneda local. Entra como un parámetro: la fracción que el exportador retiene afuera.

**Lo que el modelo tiene que poder mostrar.** Si los exportadores liquidan todo y el BCRA compra todo, (a) y (c) dejan las mismas divisas en el sector público consolidado: lo que cambia es en qué bolsillo están, del BCRA o del Tesoro. Las diferencias aparecen en otro lado:
- los pesos que el Tesoro usa para comprar los dólares y su esterilización;
- el momento en que entran los dólares respecto de los vencimientos;
- qué pasa cuando el BCRA no compra, o no le vende al Tesoro.

Por eso el comportamiento del BCRA (compra todo, compra una parte, no compra) es una dimensión del escenario y no un supuesto fijo.

## 4. Datos y su estado

| Insumo | Estado | Fuente |
|---|---|---|
| Calendario de pagos en divisas, bruto y consolidado | Listo | Fases 2 y 3 |
| Depósitos del Tesoro en el BCRA, diarios | Listo | Lote R |
| Derechos de exportación mensuales, total | Listo (dos series oficiales que difieren) | Lote D |
| Derechos o exportaciones FOB por producto | Pedido | Lote AE |
| Alícuotas vigentes, cronograma 2027 y 2028, cambios desde 2018 | Listo; faltan 2021 a 2024 | Lotes F y AD |
| Plazos de pago y DJVE | Reglas listas; serie por producto pedida | Lotes AD y AE |
| Liquidación del agro (CIARA-CEC) | 2003 a 2017 y 2026; falta 2018 a 2025 | Lotes AD y AE |
| Compras de divisas del Tesoro | 2026 listo; 2024 y 2025 pedidos | Lotes AD y AE |
| Precios FOB oficiales y cosecha | Pedido | Lote AE |
| Trayectorias de tipo de cambio, CER, TAMAR, BADLAR y SOFR | Por armar como escenarios | Series observadas en `series/` y SOFR del lote Q |

## 5. Escenarios

- **Base:** exportaciones y precios del último año, alícuotas con el cronograma ya decretado (soja de 24% a 15% hacia fines de 2028).
- **Shocks:** caída de precios, sequía con un orden de magnitud como el de 2023, cambio de alícuotas, salto del tipo de cambio.
- **Refinanciación:** los multilaterales renuevan o no, hay acceso al mercado para Globales y Bonares o no.
- **BCRA:** compra todo, compra una parte, no compra.
- **Horizonte:** mensual hasta 36 meses y anual hasta 2036, que cubre la meseta de vencimientos de 2028 a 2034.

## 6. Configuraciones base

Alejandro delegó las tres decisiones en lo que mejor sirva al objetivo. Las configuraciones base y sus variantes están en `docs/DECISIONES.md`:

1. **El fondo del régimen (d), D-012.** Una regla de referencia que le da al Tesoro un flujo mensual fijo y deja en el fondo lo que exceda, con retiros por fórmula, un tope medido en meses de servicio de la deuda en divisas y gobierno por ley.
2. **El resto de las divisas, D-013.** Liquidación en el mercado de cambios a un tipo único, con el BCRA como creador de mercado de última instancia y sin programas transitorios.
3. **Los sectores sin alícuota, D-014.** Primero se relevan (lote AF). Mientras tanto quedan fuera, y cada salida informa qué parte de las exportaciones cubre.

Las tres son puntos de partida. La simulación las contrasta con sus variantes antes de fijarlas.

## 7. Código

Se va a escribir en `src/argfx/simulation/`, separado del motor contractual: lectura de insumos, escenarios, una función por régimen, la matriz de transacciones con su control de cierre y las medidas de la sección 1. La primera prueba es contable: en cada mes, cada fila y cada columna de la matriz suman cero.
