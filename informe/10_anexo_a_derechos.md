# Anexo A. Cobrar los derechos de exportación en dólares

Este anexo aplica el marco de los dos circuitos a una propuesta concreta. La idea de cobrar los derechos de exportación directamente en dólares es de Warren Mosler, que la presentó en Buenos Aires el 1 de mayo de 2022 ("A 3% export tax payable in $US", SRC-0212). El aporte de este trabajo es formalizarla, medir sus magnitudes con los datos del mandato y precisar qué cambia y qué no (D-006).

El anexo presenta la propuesta, sus magnitudes en el mandato y los resultados del modelo de la fase 4, que compara los regímenes con los datos del mandato y con una proyección hasta 2036 (`argfx simular`).

## A.1 La propuesta y los regímenes

Hoy el derecho se determina en dólares sobre el valor FOB y se paga en pesos. El exportador liquida las divisas en el mercado, cobra pesos y con ellos paga el derecho. La propuesta es que una fracción de las divisas, igual a la alícuota del derecho, vaya directo a una cuenta en dólares del Tesoro.

El modelo compara cuatro regímenes con la misma carga tributaria (D-007):

- **(a) Pesos**, el régimen actual.
- **(b) Brasil**: el exportador vende las divisas a tipo libre y puede mantenerlas en el exterior (anexo B).
- **(c) Dólares**, la propuesta de Mosler: la fracción igual a la alícuota se paga en dólares al Tesoro (D-005).
- **(d) Dólares con fondo de estabilización**: como (c), pero las divisas entran a un fondo que le transfiere al Tesoro una suma fija mensual, igual a la doceava parte del promedio de cinco años recalculado con las alícuotas vigentes; acumula los excedentes, cubre los faltantes por fórmula y destina a cancelar deuda lo que supere doce meses de servicio en divisas a terceros (D-012).

Para el resto de las divisas del exportador, la configuración base es liquidarlas a un tipo de cambio único, sin desdoblamiento, con plazos estables y alícuotas previsibles, porque la expectativa de un cambio es lo que demora la liquidación (D-013).

## A.2 Qué cambia y qué no

Si el exportador liquida todo y el BCRA compra todas las divisas, (a) y (c) terminan con las mismas reservas y la misma base monetaria en el sector público consolidado. En (a), el BCRA compra los dólares con pesos que emite, el exportador paga el derecho con esos pesos, y si el Tesoro usa esos mismos pesos para comprarle los dólares al BCRA, la base vuelve a su lugar. En (c), los dólares van directo al Tesoro y ningún peso se mueve. El efecto es el mismo; lo que cambia es el bolsillo en que quedan los dólares (BCRA o Tesoro) y la secuencia.

La diferencia aparece cuando la secuencia se corta, que es lo que muestran los capítulos 3 y 5. El Tesoro gasta los pesos del derecho; el BCRA, para que esos pesos no presionen sobre los precios o el tipo de cambio, los absorbe con pasivos que pagan interés; y cuando el Tesoro necesita dólares, consigue otros pesos, de superávit o de deuda, para comprarlos. Cobrar en dólares le ahorra al Tesoro ese recorrido para la parte del derecho, pero el Tesoro igual tiene que conseguir los pesos que deja de cobrar, porque el gasto es el mismo. Si los consigue con deuda, el interés que antes pagaba el BCRA lo paga él. El modelo mide cuánto pesa cada uno de estos efectos (secciones A.4 a A.6).

## A.3 Las magnitudes del mandato

**Los derechos recaudados.** Entre diciembre de 2023 y agosto de 2026 los derechos sumaron unos 17.079 millones de dólares ($28,6 billones de pesos de agosto de 2026).

| Año | Derechos cobrados | Compras de dólares del Tesoro |
|---|---:|---:|
| 2023 (diciembre) | 643 | 0 |
| 2024 | 6.565 | 15.641 |
| 2025 | 6.000 | 3.973 |
| 2026 (enero a agosto) | 3.871 | 6.409 |
| **Total** | **17.079** | **26.023** |

*Millones de USD. Derechos: recaudación (datos.gob.ar, lote D) pasada a dólares al A 3500 promedio del mes. Compras: lote AI.*

Cobrados en dólares, los derechos del mandato habrían equivalido al 66% de los dólares que el Tesoro compró con pesos, y al 40% de todo el cruce entre monedas (26.023 de compras más 16.703 de deuda con el BCRA cancelada con pesos). En 2025 habrían superado las compras del año.

**La brecha entre lo estimado y lo cobrado.** El informe estima los derechos posición por posición con los archivos de exportaciones de ARCA y las alícuotas vigentes en cada mes, incluida la fórmula móvil de hidrocarburos.

| Año | Exportaciones con alícuota / total | Estimado | Cobrado | Cobrado / estimado |
|---|---:|---:|---:|---:|
| 2021 | 92,8% | 10.372 | 10.131 | 0,98 |
| 2022 | 94,3% | 12.113 | 12.511 | 1,03 |
| 2023 | 93,4% | 7.651 | 4.902 | 0,64 |
| 2024 | 93,6% | 9.144 | 6.565 | 0,72 |
| 2025 | 95,1% | 8.267 | 6.000 | 0,73 |
| 2026 (enero a septiembre) | 95,2% | 5.753 | 4.612 | 0,80 |

*Millones de USD. Fuente: `argfx derechos`.*

En 2021 y 2022 el método reproduce la recaudación. Desde 2023 se cobra entre un 20% y un 36% menos de lo estimado. Hay cinco explicaciones candidatas, ninguna cuantificada todavía:

1. **La fecha de la alícuota.** El derecho se fija al registrar la declaración jurada de venta (DJVE) y no al embarcar. Las ventanas de alícuota reducida, como el 0% del Decreto 682/2025 en septiembre de 2025, adelantaron registros y pagos. Octubre y noviembre de 2025 cobran el 25% y el 22% de lo estimado.
2. **El dólar soja.** Los programas de 2022 y 2023 adelantaron pagos: septiembre de 2022 cobró tres veces lo estimado, y los meses siguientes, mucho menos.
3. **El blend 80/20** de diciembre de 2023 a abril de 2025, que en principio no cambia el derecho en dólares.
4. **Rebajas y exenciones que faltan en la tabla de alícuotas**, sobre todo en la soja entre 2021 y 2024.
5. **Diferencias de calendario** entre el embarque y el pago.

**La estacionalidad.** Los derechos tienen su pico entre mayo y julio, con la cosecha gruesa, y su variación mensual llega a la mitad del promedio (coeficiente de variación de 0,28 en 2024 y 0,52 en 2025). Los pagos de deuda en divisas se concentran en enero y julio. El fondo del régimen (d) existe para acomodar esa diferencia.

## A.4 Lo que el modelo muestra primero: una identidad

El modelo es contable: un libro de doble entrada mensual con cinco sectores (Tesoro, BCRA, exportadores, resto del sector privado y resto del mundo), en el que cada transacción suma cero y cada instrumento cierra entre sectores en todos los meses. Las pruebas del código verifican ese cierre en los cuatro regímenes.

El primer resultado es una identidad, y conviene decirlo antes que cualquier cifra. **Si el BCRA compra todos los dólares que se liquidan, cobrar el derecho en pesos o en dólares deja al sector público consolidado con los mismos dólares y con la misma deuda en pesos.** En el régimen actual, el BCRA emite pesos para comprar los dólares del derecho, el exportador paga el derecho con esos pesos y el Tesoro los usa para comprarle los dólares al BCRA. Con el cobro en dólares, los dólares van directo al Tesoro y el Tesoro deja de cobrar esos pesos. La proyección lo confirma: en los dos regímenes, la deuda en pesos que el Tesoro tiene que tomar para comprar los dólares que le faltan es exactamente la misma (cuadro A.3). Lo que cambia es en qué bolsillo quedan los dólares, del BCRA o del Tesoro, y en qué momento llegan.

Las diferencias aparecen en tres lugares: cuando el BCRA no compra los dólares, en la moneda en que el Tesoro termina endeudado y en la regularidad con que le llegan los dólares.

## A.5 El mandato con el derecho cobrado en dólares

El ejercicio toma lo que pasó entre diciembre de 2023 y agosto de 2026 como el régimen (a) y cambia una sola cosa: el derecho cobrado cada mes, pasado a dólares al A 3500 del mes, entra a la cuenta del Tesoro en el BCRA en lugar de pagarse en pesos. Las exportaciones, el gasto, la deuda pagada y la parte del mercado que compró el BCRA quedan como fueron. Como las fuentes no dicen qué habría hecho el Tesoro con esos dólares, se miden dos usos por separado.

**Primer uso: los dólares del derecho reemplazan compras con pesos.**

| Año | Derechos en dólares | Compras del Tesoro evitadas | Compras del BCRA que no se hacen | Dólares que quedan en el sector público |
|---|---:|---:|---:|---:|
| 2023 (diciembre) | 643 | 0 | 492 | 151 |
| 2024 | 6.565 | 7.208 | 1.869 | 4.696 |
| 2025 | 6.000 | 3.495 | 303 | 4.315 |
| 2026 (enero a agosto) | 3.871 | 5.662 | 785 | 2.731 |
| **Total** | **17.079** | **16.366** | **3.450** | **11.892** |

*Cuadro A.1. Millones de USD. La última columna es el derecho, menos lo que el BCRA habría dejado de comprar en el mercado, menos las compras evitadas que el Tesoro hacía en el mercado y no al BCRA. Fuente: `argfx simular`, `data/simulacion/mandato_contrafactico_compras.csv`.*

Con el derecho en dólares, el Tesoro se habría ahorrado 16.366 de los 26.023 millones que compró con pesos. En pesos, el resultado casi no cambia: los pesos que el Tesoro no habría cobrado son casi los mismos que no habría tenido que gastar en dólares. La diferencia al cierre, con intereses a la tasa BADLAR, es de 1,2 billones de pesos, y se explica por el desfase: en 2025 los dólares del derecho habrían llegado antes de que el Tesoro los necesitara.

El efecto grande está en los dólares. En el mandato el BCRA compró, en promedio, una parte chica de lo que liquidaron los exportadores: el 27% entre diciembre de 2023 y marzo de 2025 y el 9% desde abril de 2025, con la banda cambiaria. El resto lo compraron privados. Con el derecho en dólares, esa parte del derecho habría quedado en el Tesoro en lugar de ir a manos privadas: 11.892 millones de dólares más en el sector público consolidado, una cuarta parte del atesoramiento neto del mandato. El modelo no dice qué habría pasado del otro lado. Los privados habrían tenido menos dólares para comprar, y eso pudo resolverse con menos atesoramiento, con menos importaciones o con un tipo de cambio más alto; el modelo no tiene esas respuestas.

**Segundo uso: los dólares del derecho reemplazan deuda nueva en divisas.** El Tesoro habría tomado 16.575 millones menos de deuda en divisas y habría tenido que conseguir con deuda en pesos los pesos del derecho que dejaba de cobrar. Las dos deudas, llevadas con sus intereses hasta agosto de 2026, quedan así:

| | Pesos de agosto de 2026 |
|---|---:|
| Deuda en pesos que se habría tomado, con intereses a la tasa BADLAR | 29,3 billones |
| Deuda en divisas que se habría evitado, con intereses al 7% anual, al tipo de cambio de agosto de 2026 | 27,3 billones |
| **Costo adicional de la deuda en pesos** | **2,1 billones** |

*Cuadro A.2. Fuente: `argfx simular`. La tasa de la deuda en divisas es un supuesto: con 5% el costo adicional es de 2,7 billones, y con 9%, de 1,4.*

Cambiar deuda en dólares por deuda en pesos habría costado, visto después, entre un 5% y un 10% más. La razón es que en el mandato el tipo de cambio subió menos que la tasa en pesos: la deuda en dólares resultó barata medida en pesos. Ese resultado depende del período. Con una devaluación grande en el medio, la cuenta puede dar al revés. Lo que no depende del período es la moneda: con el derecho en dólares, el Tesoro habría terminado el mandato con unos 16.600 millones de dólares menos de deuda en divisas y con su equivalente en pesos, una deuda que el Estado emite y puede renovar en su propia moneda.

**El costo de la esterilización atribuible a las compras de dólares.** Entre diciembre de 2023 y agosto de 2026 el BCRA pagó 13,4 billones de pesos corrientes de intereses, primas y remuneración de cuentas, casi todo hasta julio de 2024. Si cada peso absorbido se reparte según lo que lo creó, la parte que corresponde a las compras netas de dólares (compras al sector privado menos ventas al Tesoro) es de 2,6 billones, el 19%. El reparto en proporción es un supuesto: las fuentes no atan cada peso absorbido a su origen. Desde julio de 2024 el costo de absorber pesos lo paga el Tesoro como interés capitalizado (capítulo 3), y ahí el modelo no puede separar qué parte nace de las compras de dólares, porque la deuda en pesos del Tesoro financia a la vez el gasto, los vencimientos y la compra de divisas.

## A.6 Hacia adelante

La proyección va de octubre de 2026 a diciembre de 2036. Toma las exportaciones de los últimos doce meses con datos (octubre de 2025 a septiembre de 2026) mes por mes, les aplica las alícuotas ya decretadas en cada mes futuro (Decreto 423/2026, que baja la soja del 24% al 15% hacia fines de 2028) y multiplica por la proporción entre lo cobrado y lo estimado de enero a septiembre de 2026 (0,80). Del otro lado pone los vencimientos firmes en divisas con acreedores fuera del sector público, del calendario de la fase 2 y las tenencias de la fase 3. El tipo de cambio queda fijo en el último observado: la proyección mide dólares.

<iframe class="grafico" src="grafico_derechos_vs_servicio.html" title="Gráfico A.1"></iframe>

*Gráfico A.1. Derechos de exportación cobrados en dólares, proyección base, y vencimientos en divisas con acreedores fuera del sector público, con y sin refinanciación del capital de los organismos. Millones de USD por año. Fuente: `argfx simular`, `argfx graficos`.*

| Escenario | Derechos, oct. 2026 a 2036 | Vencimientos con terceros | Cobertura | Meses en que el Tesoro tiene que comprar dólares, (a) / (c) |
|---|---:|---:|---:|---:|
| Base, sin refinanciación | 44.640 | 206.858 | 21,6% | 122 / 97 |
| Base, los organismos renuevan el capital | 44.640 | 122.902 | 36,3% | 122 / 37 |
| Cobro igual a lo estimado (sin la brecha de A.3) | 55.680 | 206.858 | 26,9% | 122 / 94 |
| Sequía como la de 2023, desde abril de 2027 | 43.270 | 206.858 | 20,9% | 122 / 97 |
| Precios de exportación 20% más bajos | 35.720 | 206.858 | 17,3% | 122 / 108 |

*Cuadro A.3. Millones de USD, 123 meses. Fuente: `argfx simular`, `data/simulacion/proyeccion_resumen.json`. En todos los escenarios, la deuda en pesos que el Tesoro toma para comprar los dólares que le faltan es la misma en (a) y en (c).*

Los derechos cobrados en dólares cubrirían algo más de una quinta parte de los vencimientos con terceros si nadie refinancia, y algo más de un tercio si los organismos renuevan el capital, como hicieron en el mandato. Con la refinanciación de los organismos, el Tesoro dejaría de tener que comprar dólares en 86 de los 123 meses. Las alícuotas ya decretadas bajan la recaudación de unos 5.400 millones en 2027 a unos 4.150 por año desde 2029.

**El fondo de estabilización, régimen (d).** Con la regla de D-012, el fondo le transfiere al Tesoro cada mes la doceava parte del promedio anual de los primeros cinco años proyectados, unos 381 millones, y guarda los excedentes de la cosecha. La variación mensual de lo que recibe el Tesoro (coeficiente de variación) baja de 0,21 a 0,12 en el escenario base, y de 0,20 a 0,06 en el de sequía. El fondo llega a un máximo de 1.242 millones, y no se dispara la regla de cancelar deuda con lo que supere doce meses de servicio, salvo en la sequía, donde se cancelan 147 millones. Con estos montos, el fondo ordena los meses; no cambia cuántos dólares llegan.

<iframe class="grafico" src="grafico_fondo_mensual.html" title="Gráfico A.2"></iframe>

*Gráfico A.2. Dólares que recibe el Tesoro cada mes en 2027 y 2028, con el cobro directo en dólares (c) y con el fondo de estabilización (d). Millones de USD. Fuente: `argfx simular`, `argfx graficos`.*

## A.7 Qué dice y qué no dice el modelo

Lo que sostiene el modelo:

- Cobrar en dólares no crea dólares ni ahorra pesos al sector público consolidado mientras el BCRA compre todo lo que se liquida. Cambia el bolsillo y el momento.
- Cuando el BCRA no compra, el cobro en dólares retiene en el sector público dólares que de otro modo van a manos privadas. En el mandato habrían sido unos 11.900 millones.
- El Tesoro deja de depender de que el BCRA le venda o de comprar en el mercado para una quinta parte, o un tercio, de sus vencimientos con terceros.
- Si esos dólares reemplazan deuda en divisas, la deuda del Tesoro se corre hacia los pesos. En el mandato eso habría costado algo más, por cómo se movió el tipo de cambio, pero deja una deuda que el Estado maneja en su propia moneda.
- El fondo de estabilización reduce a la mitad la variación mensual de los dólares que recibe el Tesoro.

Lo que el modelo no tiene todavía: la respuesta de los exportadores (cuándo liquidan y cuándo pagan según la alícuota esperada), la de los privados que dejan de comprar los dólares del derecho, el efecto sobre el tipo de cambio y una proyección de importaciones, sin la cual las reservas brutas proyectadas no significan nada y no se informan. Tampoco explica la brecha entre los derechos estimados y los cobrados (A.3), que en la proyección se toma como dada. Esas son las extensiones de la capa de comportamiento que prevé el diseño (`docs/FASE4_DISENO.md`).
