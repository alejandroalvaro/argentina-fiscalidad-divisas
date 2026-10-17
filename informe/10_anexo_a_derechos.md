# Anexo A. Cobrar los derechos de exportación en dólares

Este anexo aplica el marco de los dos circuitos a una propuesta concreta. La idea de cobrar los derechos de exportación directamente en dólares es de Warren Mosler, que la presentó en Buenos Aires el 1 de mayo de 2022 ("A 3% export tax payable in $US", SRC-0212). El aporte de este trabajo es formalizarla, medir sus magnitudes con los datos del mandato y precisar qué cambia y qué no (D-006).

El anexo es un avance. La comparación de regímenes con el modelo de la fase 4 todavía no se corrió con datos, y lo que sigue presenta las magnitudes y el diseño, sin resultados de simulación.

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

La diferencia aparece cuando la secuencia se corta, que es lo que muestran los capítulos 3 y 5. El Tesoro gasta los pesos del derecho; el BCRA, para que esos pesos no presionen sobre los precios o el tipo de cambio, los absorbe con pasivos que pagan interés; y cuando el Tesoro necesita dólares, consigue otros pesos, de superávit o de deuda, para comprarlos. Ese recorrido tiene un costo en intereses, en pesos, que paga el Tesoro o el BCRA y cobra el sistema financiero (D-015). Cobrar en dólares evita el recorrido para la parte del derecho, sin crear un solo dólar nuevo.

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

## A.4 El costo de la esterilización: lo que hay y lo que falta

Lo medido:

- el BCRA pagó $34,6 billones de pesos de agosto de 2026 en intereses entre diciembre de 2023 y julio de 2024, y casi nada después (capítulo 3);
- desde entonces el costo lo paga el Tesoro, como interés capitalizado de entre 5 y 11 billones de pesos corrientes por trimestre (capítulo 3);
- el Tesoro aplicó $71,4 billones de pesos de agosto de 2026 a obligaciones en dólares (capítulo 5).

Lo que falta es la medida central de D-015: cuánto de los pasivos remunerados, y de sus intereses, nace de comprar dólares con pesos, y en manos de quién quedó. Para atribuirlo hace falta el modelo de la fase 4.

## A.5 Estado del modelo

Está escrito y probado el libro contable de doble entrada del modelo, en el que cada transacción suma cero, y la secuencia mensual de los cuatro regímenes con sus medidas. Las pruebas fijan que, si el BCRA compra todas las divisas, (a) y (c) terminan con las mismas reservas y difieren en cuántos dólares compra el Tesoro con pesos, y que si el BCRA compra solo una parte, (c) deja más reservas. Está escrita también la estimación de derechos por posición.

No se corrió todavía el modelo con trayectorias de datos, ni los escenarios de precios, sequía, compras del BCRA y refinanciación, ni las variantes del fondo. No hay, por lo tanto, resultados de la comparación de regímenes. Eso queda para la versión siguiente del informe.
