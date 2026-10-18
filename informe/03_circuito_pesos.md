# 3. El circuito de los pesos

En el circuito de los pesos mandan el Tesoro y el BCRA. El BCRA crea pesos cuando compra divisas, le gira utilidades al Tesoro o paga intereses, y los absorbe cuando vende divisas o coloca pasivos que pagan interés. El Tesoro cobra impuestos, gasta, coloca deuda en pesos y la renueva. Este capítulo recorre los dos balances y muestra el cambio más importante del mandato: la absorción de pesos, y su costo, pasaron del BCRA al Tesoro.

Las cifras están en billones de pesos de agosto de 2026, deflactadas mes a mes por el índice de precios al consumidor (IPC) del Instituto Nacional de Estadística y Censos (INDEC, SRC-2028), salvo que se indique "pesos corrientes". Un peso de diciembre de 2023 equivale a 3,47 pesos de agosto de 2026.

::: {.destacado custom-style="Destacado"}
**El costo de absorber pesos pasó del BCRA al Tesoro, y buena parte se acumula fuera del resultado fiscal publicado.**

Hasta julio de 2024 el BCRA pagó $34,6 billones de pesos de agosto de 2026 de intereses por los pesos que absorbía. Desde entonces paga el Tesoro, sobre todo como interés que se suma al capital de sus letras y bonos: entre 5 y 11 billones de pesos corrientes por trimestre, unos 66 billones hasta junio de 2026. El resultado en base caja no lo registra hasta que se paga, y entonces lo registra como amortización.

*Alcance.* El interés capitalizado aumenta las obligaciones del Tesoro aunque no se pague en el período. La serie no incluye el ajuste de capital de los bonos CER ni el interés de las ampliaciones de bonos TAMAR y duales.
:::

## 3.1 Del BCRA al Tesoro: el traspaso de los pasivos remunerados

A fines de 2023, el BCRA debía en pases pasivos y Letras de Liquidez (LELIQ) $25,8 billones de pesos corrientes, 2,68 veces la base monetaria. Esa deuda pagaba la tasa de política monetaria, que desde el 18 de diciembre era del 100% nominal anual. Como los pases eran a un día y el interés de cada día se volvía a colocar al día siguiente, en un año el rendimiento compuesto llegaba al 171%: (1 + 1/365)^365 − 1 = 1,71. Es la tasa efectiva que publica el propio BCRA. Hasta el 15 de diciembre la tasa había sido del 133% nominal sobre LELIQ a 28 días, que compuesta mes a mes daba un 255% efectivo, y parte del stock de fin de año todavía cobraba esa tasa (BCRA, Series.xlsm, SRC-1625). En el informe de política monetaria de junio de 2026, el mismo BCRA recuerda que sus títulos y pases llegaron a 2,5 veces la base hacia fines de 2023.

En dos años y medio ese stock desapareció del balance del BCRA:

| Fin de mes | Base monetaria | Pases y LELIQ | LEFI en bancos | Total remunerado | Remunerado / base |
|---|---:|---:|---:|---:|---:|
| Dic 2023 | 9,6 | 25,8 | | 25,8 | 2,68 |
| Jun 2024 | 20,2 | 15,9 | | 15,9 | 0,79 |
| Jul 2024 | 21,8 | 0 | 9,6 | 9,6 | 0,44 |
| Dic 2024 | 29,7 | 0 | 10,7 | 10,7 | 0,36 |
| Jun 2025 | 37,2 | 0 | 11,0 | 11,0 | 0,30 |
| Dic 2025 | 43,0 | | | 0,8 | 0,02 |
| Jul 2026 | 46,2 | | | 1,6 | 0,04 |

*Billones de pesos corrientes. Fuente: BCRA, Series.xlsm, hoja de instrumentos del BCRA (SRC-1625), lote AJ. Desde julio de 2025 el remunerado son repos con bancos.*

El traspaso tuvo tres etapas.

1. **Las LELIQ pasaron a pases** en diciembre de 2023, y los pases fueron bajando en el primer semestre de 2024 a medida que los bancos los cambiaban por LECAP del Tesoro.
2. **Los pases pasaron a LEFI** en julio de 2024. Las Letras Fiscales de Liquidez eran letras del Tesoro (RC 40/2024), colocadas por canje con el BCRA, que solo se negociaban entre el BCRA y los bancos y pagaban la tasa de política con capitalización diaria. Llegaron a $16,6 billones en bancos en noviembre de 2024. El BCRA describió la operación como el "traspaso de todos los pasivos remunerados al Tesoro".
3. **Las LEFI se rescataron** el 10 de julio de 2025 y su lugar lo ocuparon LECAP, BONCAP y duales del Tesoro, colocados en licitación.

El resultado fue que el interés que antes pagaba el BCRA pasó a pagarlo el Tesoro. Las LEFI devengaron unos $3,4 billones corrientes de interés que cobraron los bancos. El resto del costo de absorber pesos quedó en la deuda del Tesoro en pesos, que en su mayor parte capitaliza intereses (sección 3.4).

## 3.2 El BCRA en pesos

El diagrama 3.1 muestra por dónde entraron y salieron los pesos del BCRA en el mandato, con los factores de explicación de la base monetaria que publica el propio BCRA. A la izquierda están los pesos que volvieron al BCRA (absorción); a la derecha, los que salieron hacia la economía (emisión). La emisión neta, el aumento de la base, cierra el diagrama.

<iframe class="sankey" src="flujos_ars_bcra_2023-12_2026-08.html" title="Diagrama 3.1"></iframe>

*Diagrama 3.1. BCRA en pesos, diciembre de 2023 a agosto de 2026, en millones de pesos de agosto de 2026. Fuente: BCRA, Series.xlsm, hoja de base monetaria, bloque mensual (SRC-1625). `argfx flujos`.*

| Absorbieron pesos | Billones | Crearon pesos | Billones |
|---|---:|---|---:|
| Venta de divisas al Tesoro | 43,5 | Compra de divisas al sector privado | 64,7 |
| Otras operaciones con el Tesoro | 63,1 | Utilidades transferidas al Tesoro | 42,9 |
| Otros | 3,2 | Intereses, primas y remuneración de cuentas | 34,6 |
| Operaciones con LEFI | 0,1 | Desarme de LELIQ y Notas de Liquidez (NOTALIQ) | 22,9 |
| | | Desarme de pases | 8,4 |
| **Aumento de la base monetaria** | **63,5** | | |

Del diagrama salen varias lecturas.

**El BCRA pagó intereses hasta julio de 2024 y después casi nada.** El factor de intereses suma 34,6 billones: 8,3 en diciembre de 2023 y 26,4 entre enero y julio de 2024. Desde agosto de 2024 es casi cero. Los estados contables del BCRA dan el mismo perfil: intereses perdidos por 28,0 billones de pesos corrientes en 2023, 17,1 en 2024 y 1,7 en 2025.

**El Tesoro le devolvió al BCRA, por la venta de divisas, casi todo lo que recibió de utilidades.** Las utilidades transferidas suman 42,9 billones (11,98 billones corrientes en 2025, por el ejercicio 2024, y 24,4 en mayo de 2026, por el ejercicio 2025). En el mismo período, el Tesoro le compró al BCRA divisas por 43,5 billones. En mayo de 2026 el giro de utilidades volvió casi entero al BCRA el mismo mes: 24,4 billones salieron como utilidades y 22,8 volvieron como otras operaciones con el Tesoro, en línea con la recompra de Letras Intransferibles por $18,4 billones (capítulo 5).

**Las utilidades son, en su mayor parte, contables.** La Carta Orgánica del BCRA (artículo 38, SRC-0012) manda transferir al Tesoro las utilidades del ejercicio que no se capitalizan ni van a reservas, y lo que mide es el resultado contable, no el efectivo cobrado. En 2024 el BCRA ganó 19,4 billones de pesos de diciembre de 2024, pero las partidas de valuación y de interés devengado sin cobrar sumaron 43,6: el ajuste por CER de los bonos del Tesoro que tenía en cartera (27,2), la revaluación de sus activos en dólares por la suba del tipo de cambio (8,7) y el devengamiento de las Letras Intransferibles y de los adelantos al Tesoro (7,6). Sin ellas, el BCRA habría perdido unos 17 billones, sobre todo por los intereses de los pases. En 2025 ganó 34,3 billones de pesos de diciembre de 2025, y las mismas partidas sumaron 32,0, el 93% del resultado. La mayor ganancia efectiva de ese año fue de 6,3 billones, por la recompra de Letras Intransferibles que el Tesoro pagó con los dólares del FMI (estados contables 2024 y 2025, SRC-1157 y SRC-1156, nota 4.22; la separación entre lo cobrado y lo contable es propia).

Buena parte de esa ganancia contable es un crédito contra el propio Tesoro que se revalúa: el CER de sus bonos y el tipo de cambio de sus Letras. Consolidando el sector público, la ganancia del BCRA es una pérdida igual del Tesoro. Aun así, el giro de utilidades le entrega al Tesoro pesos que pueden gastarse, y en el mandato el Tesoro los usó, en buena medida, para comprarle dólares al mismo BCRA.

**Las pérdidas no las cubre el Tesoro.** El mismo artículo 38 dice que las pérdidas de un ejercicio se imputan a las reservas y, si no alcanzan, al capital del BCRA, y que el directorio puede usar las utilidades de los años siguientes para recomponerlos. Así se hizo con la pérdida de 2023: se imputó a reservas y capital en 2024, y en 2025 el BCRA retuvo 7,7 billones de las utilidades de 2024 para recomponerlos antes de girar el resto. La Carta Orgánica no obliga al Tesoro a capitalizar al BCRA cuando pierde.

**La compra de divisas al sector privado fue el principal origen de pesos.** Sumó 64,7 billones, concentrados en el primer semestre de 2024 y en 2026. En 2025, con la banda cambiaria, el BCRA casi no compró.

**La base monetaria creció 63,5 billones.** Es lo que quedó en la economía después de todas las operaciones.

Una aclaración sobre la fuente: una tabla de factores que recibimos en un lote intermedio estaba mal en 27 de los 45 meses, porque mezclaba la suma anual con el mes de enero. El código lee la planilla original del BCRA y verifica que los factores sumen la variación de la base en cada mes (capítulo 7).

## 3.3 El sector público nacional en pesos

El diagrama 3.2 muestra el sector público nacional (SPN), en base caja, solo en pesos. La deuda en divisas, sus intereses y los depósitos del Tesoro en dólares salen del diagrama, y el cruce hacia los dólares queda como una salida propia.

<iframe class="sankey" src="flujos_ars_2023-12_2026-08.html" title="Diagrama 3.2"></iframe>

*Diagrama 3.2. Sector público nacional en pesos, diciembre de 2023 a agosto de 2026, en millones de pesos de agosto de 2026. Fuentes: esquema ahorro-inversión-financiamiento (AIF) en base caja (lotes AM y AN), boletín de la Secretaría de Finanzas, cuadro A.5 (SRC-9002), lotes AI, AR y AS. `argfx flujos`. Cada línea está neta en la ventana. El diagrama cierra con una diferencia de $214.000 millones de redondeo.*

| Entradas | Billones | Salidas | Billones |
|---|---:|---|---:|
| Impuestos y aportes (sin derechos) | 440,2 | Prestaciones sociales | 301,0 |
| Derechos de exportación | 28,6 | Funcionamiento y otros gastos corrientes | 88,6 |
| Utilidades del BCRA | 42,9 | Subsidios económicos | 38,5 |
| Rentas de la propiedad | 19,6 | Universidades, provincias y capital | 37,0 |
| Otros ingresos | 22,8 | Intereses de la deuda en pesos (netos) | 2,2 |
| Deuda en pesos colocada | 610,5 | Deuda en pesos amortizada | 507,8 |
| Deuda escrita en dólares, colocada por pesos | 31,9 | Deuda escrita en dólares, pagada en pesos | 79,3 |
| Uso de activos financieros | 279,1 | Aumento de activos financieros | 354,7 |
| Otros pasivos (aumento) | 33,7 | Otros pasivos (disminución) | 35,4 |
| Diferencia entre monedas | 7,7 | Compra de dólares | 45,7 |
| | | Deuda en dólares con el BCRA cancelada con pesos | 27,0 |

**El resultado.** El superávit primario del período fue de 46,1 billones. Los intereses en efectivo, en todas las monedas, fueron 44,6, de modo que el resultado financiero en base caja quedó en +1,5 billones. En pesos corrientes, el primario pasó de −2,0 billones en diciembre de 2023 a +10,4 en 2024, +11,8 en 2025 y +12,3 entre enero y agosto de 2026.

**El interés en efectivo es casi todo en dólares.** De los 44,6 billones de intereses pagados en efectivo, solo 2,2 corresponden a la deuda en pesos. El resto, unos 42,4 billones, es interés de la deuda en moneda extranjera (cuadro A.5 del boletín de Finanzas, por moneda de pago, convertido al tipo de cambio de cada mes). La deuda en pesos casi no paga interés en efectivo porque capitaliza: LECAP, BONCAP y LEFI acumulan el interés en el capital y lo pagan al vencimiento, cuando el pago se registra como amortización. El programa financiero oficial dice que "los intereses se pagan con superávit fiscal" (SRC-1770). En los hechos, el superávit primario en pesos alcanzó para pagar intereses que en su mayoría eran en dólares, y que por lo tanto exigieron conseguir dólares.

**Qué son los activos financieros.** En el esquema de Hacienda, el "aumento de activos financieros" es todo lo que el sector público hace con pesos que no es gastar ni pagar deuda: depositarlos en el BCRA o en el Banco Nación, comprar títulos (el Fondo de Garantía de Sustentabilidad de la ANSES, o FGS, compra bonos del Tesoro), prestarles a provincias o a empresas. El "uso de activos financieros" es lo contrario: retirar depósitos, vender títulos, cobrar préstamos. Las dos líneas son brutas y se mueven mucho mes a mes. En neto, en el mandato el sector público acumuló 75,6 billones en activos financieros, en su mayor parte depósitos en el BCRA.

**La deuda en pesos creció.** Se colocaron 610,5 billones y se amortizaron 507,8: una colocación neta de 102,8 billones. Descontados los 75,6 billones que el sector público acumuló en activos, el financiamiento neto en pesos fue de unos 27 billones. Una parte de la deuda colocada por encima de los vencimientos quedó depositada, como dijo el BCRA en abril de 2026. Esos 27 billones son deuda neta de depósitos con quienes están fuera del sector público nacional: bancos, fondos, personas, pero también el BCRA y el Banco Nación, que no forman parte de él. Las fuentes en base caja no permiten separar cuánto es con privados.

**El cruce hacia los dólares.** El Tesoro aplicó 72,7 billones a obligaciones en dólares: 45,7 a comprar dólares y 27,0 a cancelar deuda en dólares con el BCRA, que no le dio ningún dólar disponible (capítulo 5). Aparte, pagó en pesos 79,3 billones de deuda escrita en dólares y cobró 31,9 por colocarla. Las fuentes en pesos del período fueron el superávit primario (46,1), las utilidades del BCRA (42,9) y la colocación neta de deuda en pesos (102,8), mientras se acumulaban depósitos. Con las fuentes publicadas no se puede saber qué peso financió qué. No hay un comunicado, compra por compra, que diga con qué pesos se compraron los dólares.

## 3.4 El interés que no se ve

Las LECAP y BONCAP capitalizan el interés y lo pagan todo al vencimiento. En base caja, ese interés no figura como gasto mientras se acumula, y al vencer se paga como amortización de capital. El resultado financiero publicado no lo registra nunca. La Jefatura de Gabinete lo confirmó en el Informe 144 (pregunta 58): el interés capitalizado no se registra como interés en base caja.

Conviene nombrar con precisión tres medidas distintas del resultado:

- el **resultado financiero en base caja** es el que publica la Secretaría de Hacienda: registra el interés cuando se paga en efectivo;
- el **resultado financiero con intereses capitalizados devengados** le suma el interés que las LECAP, BONCAP y LEFI acumulan en el capital en cada trimestre, aunque todavía no se haya pagado. Es el que reconstruye este capítulo;
- un **resultado ajustado por inflación** trataría además el ajuste de capital de los bonos CER, y la parte del interés nominal que solo compensa la inflación, de manera homogénea en toda la deuda en pesos. El informe no lo calcula.

El informe reconstruye la segunda medida trimestre a trimestre con las planillas trimestrales de la Secretaría de Finanzas, netas de lo que traen las ampliaciones, los descuentos y las primas de colocación (`argfx devengados`, D-009).

| Trimestre | Interés capitalizado neto, Administración Central | Resultado financiero en base caja | Resultado financiero con intereses capitalizados devengados (SPN) |
|---|---:|---:|---|
| 2024 T1 | 6 | +1.133 | +1.128 |
| 2024 T2 | 858 | +1.439 | +581 a +613 |
| 2024 T3 | 5.304 | −131 | −5.435 a −5.060 |
| 2024 T4 | 6.177 | −677 | −6.670 a −6.433 |
| 2025 T1 | 5.892 | +1.309 | −3.781 a −3.714 |
| 2025 T2 | 8.164 | +1.786 | −4.871 a −4.645 |
| 2025 T3 | 10.830 | +531 | −9.045 a −8.842 |
| 2025 T4 | 9.610 | −2.173 | −10.467 a −10.009 |
| 2026 T1 | 9.808 | +1.734 | −7.045 a −6.363 |
| 2026 T2 | 9.054 | −278 | −8.371 a −7.856 |

*Miles de millones de pesos corrientes. El rango del sector público nacional depende de cuánto de la deuda capitalizable tiene el FGS, que se descuenta porque es interés dentro del sector público (entre el 10,6% y el 16,3% al 30-06-2026). Fuente: `argfx devengados`, planillas trimestrales de Finanzas, línea A.2.2.*

<iframe class="grafico" src="grafico_resultado_devengado.html" title="Gráfico 3.1"></iframe>

*Gráfico 3.1. Resultado financiero del sector público nacional por trimestre: en base caja, el publicado (verde), y con intereses capitalizados devengados (rojo, punto medio del rango del FGS). Billones de pesos corrientes. Fuente: `argfx devengados`, `argfx graficos`.*

El interés capitalizado neto va de 5 a 11 billones de pesos corrientes por trimestre desde mediados de 2024 y suma unos 66 billones corrientes hasta junio de 2026. Con intereses capitalizados devengados, el resultado financiero del sector público nacional es deficitario en todos los trimestres desde el tercero de 2024. Ese interés es, en buena medida, el costo de la absorción de pesos que el BCRA dejó de pagar en julio de 2024: cambió de pagador y de forma de registro.

La medida tiene un faltante conocido, que va en contra del resultado. Deja afuera el ajuste del capital de los bonos CER por la inflación, que la planilla registra aparte y que va de 7 a 41 billones de pesos corrientes por trimestre, y el interés de las ampliaciones de bonos TAMAR y duales y de los canjes. Si se sumara el ajuste CER, el resultado financiero devengado en términos nominales quedaría por debajo de la barra roja. En una medida ajustada por inflación, en cambio, ese ajuste y la parte inflacionaria del interés de toda la deuda en pesos se tratarían como compensación por la pérdida de valor del capital, y el déficit sería menor que el nominal. Las dos lecturas responden preguntas distintas, y el informe presenta la barra roja con su nombre: el resultado nominal con el interés capitalizado, sin el ajuste CER.

## 3.5 Escala fiscal: universidades e intereses

En la discusión fiscal del mandato, el financiamiento de las universidades nacionales ocupó un lugar central. Conviene ver su peso en las cuentas al lado de otros flujos del presupuesto, con la misma fuente, el mismo período y la misma unidad.

| Año 2025, gasto devengado de la Administración Nacional | Billones de pesos de agosto de 2026 |
|---|---:|
| Transferencias a universidades nacionales | 6,0 |
| Intereses de la deuda, según el presupuesto | 13,9 |
| Transferencias corrientes en energía y transporte | 9,9 |
| Prestaciones de la seguridad social | 77,1 |
| *Fuera del presupuesto: interés capitalizado neto de la deuda en pesos (sección 3.4)* | *39,6 a 46,9* |

*Fuentes: Presupuesto Abierto, crédito anual 2025, devengado (Secretaría de Hacienda, repositorio de la DGSIAF, actualizado al 5-07-2026); universidades: programa 26 "Desarrollo de la Educación Superior", inciso 5, partida 6; intereses: inciso 7, solo intereses, sin comisiones ni primas; energía y transporte: transferencias corrientes de esas funciones, una aproximación propia a los subsidios económicos. Interés capitalizado: `argfx devengados`, trimestres de 2025, entre el sector público nacional sin el FGS (39,6) y la Administración Central (46,9). Deflactado mes a mes con el IPC del INDEC. Originales: SRC-9009 a SRC-9012 (`inbox/claude-revision-2026-10-18/`); tabla en `series/presupuesto_abierto_devengado.csv`.*

En 2025 los intereses que registra el presupuesto fueron 2,3 veces las transferencias a las universidades nacionales; entre enero y septiembre de 2026, 2,9 veces (13,1 contra 4,5 billones de pesos de agosto de 2026). Si se suma el interés que la deuda en pesos capitalizó en 2025 y que el presupuesto no registra como interés, la relación pasa a ser de nueve a diez veces. La comparación sirve para medir el tamaño relativo del ajuste universitario frente a otros flujos. No dice que el gasto universitario sea eficiente, ni que no tenga costo fiscal, ni que un peso de intereses se pueda reasignar sin más a otro destino, porque los intereses son obligaciones contractuales.

Dos cuidados más. Las dos columnas de intereses son devengadas y no incluyen amortizaciones ni colocaciones brutas, que son movimientos de deuda y no gasto. Y en 2026 hay crédito asignado a universidades sin devengar (1,5 billones corrientes en "universidades sin discriminar"), en un año en que la aplicación de la Ley de Financiamiento Universitario (27.795) está en discusión judicial, según la prensa.

## 3.6 La deuda del Tesoro en pesos

La Secretaría de Finanzas publica la deuda del Tesoro en pesos convertida a dólares (cuadro A.1.7), sin una serie oficial en pesos. Por instrumento, el cambio de composición es claro:

| Corte | LECAP | BONCAP | Duales TAMAR | LEFI | Dólar linked | Total títulos en pesos |
|---|---:|---:|---:|---:|---:|---:|
| Dic 2023 | 0 | 0 | 0 | 0 | 6.402 | 51.688 |
| Dic 2024 | 28.498 | 5.180 | 0 | 23.021 | 3.067 | 70.716 |
| Dic 2025 | 42.661 | 19.171 | 19.071 | 0 | 9.325 | 92.446 |
| Jun 2026 | 30.467 | 46.391 | 7.512 | 0 | 8.954 | 95.428 |

*Millones de USD a valor actualizado, como lo publica la fuente. Finanzas, cuadro A.1.7, lote AJ. La columna de bonos CER de esa tabla parece incompleta y se revisa antes de la versión final.*

En la conciliación al 30-06-2026 (capítulo 2), la deuda en pesos suma 225.154 millones de dólares a valor de SIGADE, de los cuales unos 112.600 están ajustados por CER y 100.800 son a tasa fija, variable o dual. El 60% de la deuda en pesos está en manos del propio sector público, según la planilla oficial.
