# Resumen ejecutivo al 16-10-2026

Estado del proyecto al cierre de la fase 3. Las cifras son preliminares. Las del calendario y la conciliación salen del código del repositorio y se pueden reproducir. Las del FMI, las de la prensa y las de los consultores provienen de los lotes de Grok, que en su mayoría siguen como `sin_revisar`. Montos en millones de USD salvo que se indique otra cosa. El corte de la deuda es el 30-06-2026 (SIGADE), con las operaciones posteriores sumadas hasta la última información oficial.

## 1. Qué buscamos

La pregunta es si cobrar los derechos de exportación directamente en dólares, como propuso Warren Mosler en 2022, hace más previsible la liquidez en divisas del Tesoro que cobrarlos en pesos con la misma carga tributaria. Interesa también si reduce la compra de dólares con pesos y la esterilización que la acompaña, y qué pasa con el riesgo de refinanciar la deuda. Brasil sirve de contraste acotado.

Para responder hace falta saber cuántos dólares tiene que pagar el Estado, cuándo y a quién. Esa es la mitad del trabajo que ya está hecha. La otra mitad es la comparación de regímenes, que corresponde a la fase 4.

## 2. Cómo lo hacemos

- **Fuentes primarias, guardadas y trazables.** Grok busca los documentos y los registra en lotes (de la A a la AC, 672 fuentes y 853 afirmaciones). Claude Code baja los originales, los guarda en R2 identificados por su sha256, coteja las cifras clave contra el original y fusiona cada lote solo si pasa el validador y las pruebas.
- **Motor contractual.** El calendario de pagos se arma instrumento por instrumento con las condiciones de emisión (81 instrumentos con términos propios, el resto con la proyección de SIGADE). Cada flujo guarda por separado la moneda de cuenta, la indexación, la moneda en que se paga y el tenedor. Por eso la deuda dólar-linked, que se paga en pesos, no cuenta como necesidad de divisas.
- **Conciliación con las cifras oficiales.** El inventario se contrasta con la planilla trimestral de la Secretaría de Finanzas. Luego se descuentan los pagos a organismos del propio sector público y se reconstruye el interés que se devenga y no se paga.
- **Reglas que no se negocian.** Un dato que falta queda vacío y nunca se completa con cero. Las reservas netas siguen la definición del acuerdo con el FMI (D-001), y los datos observados, los contratos, los escenarios y los supuestos van en tablas separadas.

## 3. Qué está hecho

| Fase | Estado |
|---|---|
| 0 y 1. Protocolo, inventario e infraestructura | Terminadas |
| 2. Motor contractual | Terminada. Reproduce SIGADE al centavo donde los contratos coinciden, y explica cada diferencia donde no |
| 3. Conciliación | Casi terminada. Faltan la consolidación de la deuda en pesos y dos movimientos sin explicar |
| 4. Simulación de regímenes | Preparación: datos pedidos a Grok (lote AD) |
| 5. Manuscrito | Sin empezar |

Los controles de la fase 3 cierran todos. El saldo de SIGADE (471.690) es igual al de la planilla oficial. Las identidades de flujos del trimestre cierran y el perfil de vencimientos oficial a doce meses se reproduce en los 24 meses y conceptos.

## 4. Resultados preliminares

### La deuda al 30-06-2026

| Composición por moneda de pago | Saldo |
|---|---|
| Bonos y letras en dólares | 136.974 |
| Organismos multilaterales (FMI incluido) | 96.425 |
| Bilaterales y otras monedas extranjeras | 8.178 |
| Letras en garantía del FODER (contingentes, D-011) | 3.774 |
| **Pagadera en divisas** | **cerca de 245.400 (52%)** |
| En pesos ajustados por CER | 112.637 |
| En pesos a tasa fija, variable y duales | 100.804 |
| Dólar-linked pagadera en pesos | 8.954 |

Quién la tiene: el propio sector público tiene el 41,6% (197.213), los privados el 37,5% y los organismos internacionales el 20,9%. Es decir que cuatro de cada diez dólares de deuda bruta son una deuda del Estado consigo mismo, sobre todo letras intransferibles del BCRA y tenencias del FGS y el Banco Nación.

### Lo que hay que pagar en divisas en los próximos doce meses (julio de 2026 a junio de 2027)

| Acreedor | Pagos firmes |
|---|---|
| FMI | 6.254 |
| Otros multilaterales | 4.181 |
| Globales (ley extranjera) | 4.744 |
| Bonares (ley local) | 4.195 |
| Letra intra sector público en dólares | 1.228 |
| Bilaterales y otras monedas | 1.396 |
| Resto | 147 |
| **Necesidad bruta** | **22.145** |
| Menos pagos a tenedores del sector público | −3.370 |
| **Necesidad consolidada** | **18.775** (20.618 sin la capa estimada por proporción) |

Los pagos se concentran en dos meses: julio de 2026 (5.079) y enero de 2027 (5.067) suman el 46% del año. De octubre a diciembre de 2026 vencen 2.374.

### A más largo plazo

Por año calendario, la necesidad bruta en divisas es de 26.500 en 2027 y luego sube a una meseta de 27.000 a 35.000 por año entre 2028 y 2034. El pico es 2032 y 2033 (34.500 y 35.000), cuando amortizan juntos los bonos del canje de 2020 y los préstamos del FMI. Desde 2036 baja a menos de 7.000 por año. Estas cifras suponen que no se refinancia nada, incluidos los organismos multilaterales, que en la práctica suelen renovar.

### Reservas y depósitos del Tesoro

- **Reservas brutas del BCRA:** 49.323 al 08-10-2026.
- **Reservas netas según el FMI** (informes del personal técnico, lotes X e Y):
  - fin de 2025: −12.100, con una meta de −1.000 que no se cumplió;
  - marzo de 2026: −10.500, contra una meta de −1.500;
  - la meta de junio de 2026 se bajó de 3.200 a −8.600, y la de fin de 2026 es −4.100.
- **Depósitos en divisas del Tesoro en el BCRA:** unos 1.230 al 13-10-2026, contra 3.920 al 30-06-2026. En octubre de 2025 llegaron a 92, el mínimo de la serie.

### Interés que se devenga y no se paga

Las LECAP y BONCAP capitalizan el interés y lo pagan al vencimiento, así que no aparece en el resultado fiscal en base caja. Reconstruido trimestre por trimestre, el interés capitalizado neto va de 5 a 11 billones de pesos por trimestre desde mediados de 2024. Si se suma al resultado, el resultado financiero del sector público nacional da déficit en todos los trimestres desde el tercero de 2024, también después de descontar lo que tiene el FGS. En el segundo trimestre de 2026, el resultado financiero en base caja es un déficit de 278 miles de millones de pesos, y con lo devengado pasa a un déficit de entre 7.856 y 8.371.

## 5. Diferencias con lo que dicen las autoridades y la prensa

- **Depósitos del Tesoro.** Las cifras de la prensa coinciden con el cálculo propio: 2.760 el 10-09 y 1.177 el 05-10, según la consultora 1816. Aquí no hay diferencia.
- **Reservas.** La prensa y el discurso público hablan de reservas brutas, que rondan los 49.000. Con la definición del FMI, las netas siguen siendo negativas, y el país no cumplió ninguna de las metas de 2025 ni la de marzo de 2026. Las metas se fueron rebajando en cada revisión. Las dos cifras pueden ser ciertas a la vez; lo que cambia es la pregunta que responde cada una.
- **Cobertura de los pagos.** Un titular de septiembre habla de un plan financiero para cubrir 4.000 hasta diciembre. El calendario propio da 2.374 de octubre a diciembre y 5.067 solo en enero de 2027, contra depósitos del Tesoro de 1.230. No encontramos una cifra oficial de necesidad de divisas a doce meses con la cual compararlo, ni una declaración de las autoridades sobre la meseta de 2028 a 2034.
- **Resultado fiscal.** El Ministerio de Economía sostiene, en el Informe 144 de la Jefatura de Gabinete, que el interés capitalizado no afecta el resultado y que la contabilidad no cambió. Con lo devengado, el superávit financiero publicado se vuelve déficit. CEPA y la OPC llegan a la misma dirección con métodos que no se pudieron replicar.
- **Cifras que no cierran entre fuentes oficiales:**
  - la recompra de letras intransferibles de mayo de 2026 figura por 21.700 (Ministerio), 20.434 o 22.284 (resoluciones), 21.000 (BCRA) y 13.225 efectivos (prensa);
  - el pago de 1.040 de la RC 30/2026 no aparece en los depósitos del Tesoro;
  - las reservas netas de 2025 son −12.100 en el informe del FMI y −9.600 en la carta de intención;
  - las compras de divisas del Tesoro en 2025 dan 2.727 o 1.216 según la serie.
- **Deuda en moneda extranjera.** La OPC informa 247.504 a agosto de 2026, en línea con nuestros 245.400 a junio, aunque con métodos distintos.

## 6. La arquitectura de la deuda

**Es transparente en el saldo.** SIGADE, la planilla trimestral y el perfil de vencimientos coinciden al dólar, y eso es una virtud que no todos los países tienen.

**Es opaca en el movimiento y en los tenedores.** El corte se publica con casi tres meses de demora, y en ese lapso las licitaciones quincenales mueven 36.000 de capital a doce meses. No se publica quién tiene cada bono. Hay bajas de saldo sin una operación que las explique (TMF27, TMG27, TZX27), montos de una resolución que nunca se publicaron (RC 60/2026) y un pago que no aparece en las cuentas (RC 30/2026). En la estructura financiera oficial encontramos además un error de carga: el Global 2035 repite la amortización del 2030.

**Es difícil de comprender sin reconstruirla.** Conviven más de 750 operaciones y una variedad de diseños poco común:
- ajustes por CER con diez días hábiles de rezago y dos bases distintas para el mismo bono;
- tasas TAMAR promediadas y duales que pagan la mayor de dos ramas (fija o TAMAR, CER o TAMAR, dólar-linked o TAMAR);
- deuda en dólares que se paga en pesos;
- letras que capitalizan un interés que no aparece como gasto;
- letras en garantía que SIGADE registra como deuda en situación normal cuando en realidad son contingentes.

Para leer el calendario fue necesario escribir un motor contractual. Sin él, el perfil oficial subestima el capital a doce meses en 32.900, que el motor atribuye a causas contractuales sin dejar residuo.

**Sobre su lógica.** El diseño responde a una lógica reconocible. La deuda en pesos es corta (las letras tienen 0,55 años de vida promedio) e indexada, y se refinancia cada dos semanas. La deuda en divisas viene del canje de 2020 y del FMI, con pagos concentrados en enero y julio y una meseta entre 2028 y 2034. El costo de esa lógica queda en parte fuera de la vista: en la capitalización que no pasa por el resultado y en las tenencias dentro del sector público, que inflan la deuda bruta y a la vez la vuelven más fácil de refinanciar. La valoración de esa elección queda para el lector del informe.

## 7. ¿Qué tan robusta parece la hipótesis?

Por ahora hay indicios, no pruebas. La comparación de regímenes es la fase 4 y todavía no corrió. Lo que ya se ve:

- **H3 (la matriz por moneda, indexación, pago y tenedor revela riesgos):** es la mejor sostenida. La matriz mostró el interés capitalizado oculto, la deuda dólar-linked que no requiere divisas, los 3.370 de pagos que quedan dentro del sector público y la meseta 2028 a 2034. Nada de eso se ve en los agregados.
- **H1 (previsibilidad):** hay datos para las dos puntas.
  - A favor: el volumen pesa. Los derechos de exportación sumaron unos 5.200 en los últimos doce meses (6.600 en 2024 y 6.000 en 2025). Eso es entre el 23% y el 28% de la necesidad firme a doce meses, y cerca del 60% de lo que se paga a tenedores de Globales y Bonares.
  - En contra: son volátiles (la variación mensual va del 28% al 52% de la media) y estacionales, con el pico entre abril y septiembre por la cosecha, mientras que los pagos se concentran en enero y julio. La baja de alícuotas ya decretada (soja de 24% a 15% hacia fines de 2028) achica la recaudación justo cuando empieza la meseta de vencimientos.
- **H2 (menos compras de dólares con pesos y menos esterilización):** el problema es real. El Tesoro llegó a tener 92 en depósitos en octubre de 2025 y hoy tiene unos 1.230, frente a 2.374 por pagar antes de fin de año. Pero hay que mirar el efecto con cuidado. Con la definición del FMI y consolidando Tesoro y BCRA, cobrar en dólares no crea divisas nuevas si los exportadores las iban a liquidar igual: las cambia de bolsillo, del BCRA al Tesoro. La ventaja, si existe, está en ahorrar la emisión de pesos para comprarlas, en la esterilización asociada y en la previsibilidad de la caja del Tesoro. Eso es lo que la fase 4 tiene que medir.
- **H4 y H5 (refinanciación e inversión):** sin datos todavía para sostenerlas ni para debilitarlas.

## 8. Qué falta para concluir

**Fase 3:**
1. Consolidar la deuda en pesos con las tenencias del BCRA, el Banco Nación y el FGS. No cambia la necesidad de divisas, pero sí la lectura de la deuda bruta.
2. Explicar o dejar documentados la RC 30/2026 y las bajas de TMF27, TMG27 y TZX27.
3. Actualizar todo con SIGADE al 30-09-2026 y la planilla del tercer trimestre cuando se publiquen.

**Fase 4:**
1. Los datos pedidos a Grok (lote AD): derechos por producto, plazos de pago, liquidación del agro, precios y cantidades, cambios de alícuota, compras de divisas del Tesoro y Brasil.
2. Las decisiones de Alejandro que siguen abiertas: las reglas del fondo de estabilización del régimen (d) y qué hacer con el resto de las divisas de exportación (menú de `docs/APORTES_PROPUESTOS.md`, sección 8).
3. Escenarios de tasas, índices y tipo de cambio. Sin ellos, unos 8.000 de capital en pesos quedan sin monto, y los préstamos a tasa SOFR siguen con la tasa congelada.
4. El modelo stock-flujo consistente con los cuatro regímenes (D-007) y el análisis de sensibilidad a exportaciones, tipo de cambio, refinanciación y shocks productivos.

**Fase 5:** el informe final de deuda y la respuesta a la pregunta, con cada cifra vinculada a su fuente, su corte y su método.
