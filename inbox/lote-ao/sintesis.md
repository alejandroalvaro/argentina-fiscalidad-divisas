# Lote AO: por qué la amortización en moneda extranjera del AIF supera a los pagos de capital de A.5

Todo lo de abajo sale de tablas del lote y de claims `CLM-AO-xxx` (estado `sin_revisar`). Pesos y dólares nunca se suman sin aclarar. USD del AIF = pesos del total SPN divididos por el A 3500 promedio mensual (BCRA API v4.0 variable 5, SRC-2040).

## 1. Fuente que abre la amortización en moneda extranjera por instrumento (pedido 1)

- **Presupuesto Abierto no sirve para esto.** El inciso 7 de `credito-mensual-AAAA.zip` (SRC-2035 a 2038) trae solo intereses, comisiones y primas. No hay amortización de capital por instrumento ni por acreedor. El catálogo del sitio (SRC-2039) ofrece gastos y recursos, sin fuentes ni aplicaciones financieras (CLM-AO-040).
- **La fuente oficial más cercana es la hoja A.4 del boletín mensual de Finanzas** (SRC-9002): sección 2, "Amortizaciones, canjes y cancelaciones", por instrumento y mes, en USD millones. Ojo: A.4 incluye canjes y cancelaciones sin movimiento de caja, y en el archivo del 30-09-2026 solo llega hasta 2026-06. Julio y agosto de 2026 quedan sin apertura.
- Tabla: `tablas/conciliacion_amortizacion_me_aif_vs_a5_vs_a4.csv` (2023-12 a 2026-08) y `tablas/a4_filas_usd_amortizacion_meses_prioritarios.csv`.

### Qué muestra la conciliación (hechos, con límites)

1. **El AIF registra bruto las renovaciones.** El endeudamiento en moneda extranjera del AIF coincide con las emisiones en moneda extranjera de A.4 en meses como 2024-01 (AIF USD 14.372 M, de los cuales A.4 muestra USD 9.644 M de LETRA BCRA - U$S, fila 209). Esa coincidencia es consistente con que el AIF cuente la emisión y la amortización de las Letras Intransferibles renovadas como flujos brutos. No es una prueba contable.
2. **A.5 clasifica por moneda de pago, el AIF por moneda del instrumento.** En 2024-08, A.5 muestra capital en moneda extranjera de USD 154,5 M, pero A.4 muestra un vencimiento de BONAR DUAL U$S del 30-08-2024 por USD 1.546 M (CLM-AO-018). Es decir, ese título no cuenta como capital en moneda extranjera en A.5. Algo parecido pasa con BONAR DUAL 28-02-2024 (USD 4.939 M), BONAR DUAL 31-01-2025 (USD 8.596 M) y LETES U$S "Pagan en pesos" en 2025-10 (USD 3.231 M).
3. **Cierre numérico por rubros.** Restando a la amortización ME del AIF (a) el capital ME de A.5, (b) la amortización de LETRA BCRA - U$S de A.4, (c) las letras en dólares con organismos públicos (FGS, FODER, FONDCE, Playas Ferroviarias y similares) y (d) BONAR DUAL, BONTE U$S y LETES U$S de A.4, el residuo queda por debajo de USD 650 M en 2023-12, 2024-01, 2024-04, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11 y 2025-03 (columna `residuo_despues_de_letes_usd_bonar_dual_bonte_usd_usd_m`). En los meses con canjes o recompras de LIT la resta no es válida (A.4 cuenta lo que el AIF no, o A.5 y A.4 cuentan lo mismo): 2024-03, 2025-01, 2025-05, 2025-08, 2026-05 y de 2025-10 en adelante (residuo negativo). No quedó explicado 2024-02 (residuo de USD 2.426 M).
4. **Hipótesis de Claude.** Los datos son consistentes con renovaciones de LIT y letras en dólares con tenedores públicos (punto 1 y 3 arriba) y con instrumentos en dólares que pagan en pesos (punto 2). No encontré una fuente que abra el AIF por acreedor, así que no lo doy por probado. Los canjes dólar a pesos existen, pero en 2024-03 (ver punto 2 del pedido abajo) el AIF no los refleja como caja: AIF 2024-03 amortización ME = USD 448 M frente a USD 25.173 M de bajas en A.4.

## 2. Canjes y conversiones de dólares a pesos y letras con organismos públicos (pedido 2)

Fuente: hoja "Canjes- Conversiones" de los cuatro archivos ONCP de Colocaciones (SRC-2023 a SRC-2026), 144 filas entre 2023-12 y 2026-08 (`tablas/canjes_conversiones_oncp_2023-12_a_2026-08.csv`, resumen por operación en `canjes_conversiones_resumen_por_operacion.csv`). La columna de número de resolución dice "RESOL n"; los textos que pude verificar son Resoluciones Conjuntas de la Secretaría de Finanzas y de Hacienda.

- **15-03-2024, "RESOL 16" = RC 16/2024** (SRC-2033, 12-03-2024, publicada 13-03-2024): conversión de títulos elegibles por BONCER cero cupón en pesos por hasta VE $60 billones, abierta a FGS, BCRA, BNA y tenedores relevantes. Las bajas incluyen BONAR DUAL U$S (30-04, 30-06, 30-08 y 29-11 de 2024) y BONTE U$S "Paga en pesos" (30-04-2024 y 30-09-2024): USD 25.172,7 M en la hoja ONCP, que coincide con las filas 323 a 326, 410 y 412 de A.4 de 2024-03 (CLM-AO-021 y 022). Es el único cruce claro de denominación dólar a pesos de gran monto en la ventana.
- **29-01-2025, "RESOL 4" = RC 4/2025** (SRC-2034): conversión por cuatro bonos duales en pesos (hasta VE $25 billones). Entre los instrumentos dados de baja figura BONTE U$S 0% 30-06-2025 "Paga en pesos" (filas 26 a 29 de ONCP 2025). La hoja no indica unidad de los valores de baja, no los sumé como USD.
- **Enero a agosto de 2026:** conversiones de LELINK por LELINK y por BONTE U$S "Paga en pesos" (RESOL 1/2026, 2/2026, 4/2026 y siguientes). Por nombre del instrumento no cruzan denominación (todo en dólares aunque algunos pagan en pesos). La clasificación por nombre es mía, no de la fuente.
- Del resto de las 144 filas, 116 no cruzan denominación según el nombre del instrumento (peso a peso, o dólar a dólar en 2026).
- **Letras en dólares con organismos públicos:** A.4 las abre por fila (FGS, FODER, FONDCE, Playas Ferroviarias y similares, filas 253 a 265 de la sección 2, y LETRA BCRA - U$S en la fila 420). No hallé una norma que liste cada colocación y renovación con fecha y monto. Queda en `unresolved.md`.

## 3. Cómo se pagaron las recompras de Letras Intransferibles (pedido 3)

Tabla: `tablas/recompras_lit_fuente_de_fondos.csv`.

- **RC 37/2025 (agosto de 2025, USD 2.000 M de valor efectivo):** el texto de la RC invoca el decreto 179/2025 (programa con el FMI, fondos destinados a la cancelación de LIT), pero no declara la fuente de los dólares. El secretario de Finanzas dijo que se hizo con los US$2.000 millones del desembolso del FMI (CLM-AO-026 y 027). Fuente oficial indirecta por prensa.
- **RC 47/2026 (10-08-2026, USD 781.466.440,76):** la RC solo cita el decreto 453/2025 art. 2. Según TN, el aumento de USD 781 M de los depósitos en moneda extranjera del Tesoro del 03-08-2026 respondió a que el BCRA adquirió BOPREAL; luego el Tesoro recompró dos letras (vencimientos 30-06-2031 y 20-04-2032) por esa suma. Infobae cita a Economía diciendo que una parte es un tema técnico y transitorio ligado a los BOPREAL. Lo tomo como indicio (confianza media): no hay documento oficial que describa el flujo.
- **RC 27/2026 (26-05-2026): corrección.** El comunicado oficial del 14-05-2026 dice que el BCRA puso a disposición del Tesoro $24,4 billones de dividendos del ejercicio 2025, de los cuales $6 billones van a depósitos del Tesoro en el BCRA y **$18,4 billones se aplican a la recompra de LIT**. La RC 27/2026 fija ese mismo valor efectivo ($18,4 billones a $1.391,3141 por dólar, igual a USD 13.225 M). No se pagó con los $24,4 billones completos. El AIF de mayo de 2026 (USD 14.455 M) se aproxima a A.5 (USD 1.262 M) más USD 13.225 M (suma USD 14.487 M): A.5 no cuenta la recompra porque se pagó en pesos (CLM-AO-030).

## 4. Depósitos del Tesoro en moneda extranjera (pedido 4)

No encontré una serie oficial de depósitos del Tesoro en el Banco Nación. Lo que existe es el saldo en dólares del Tesoro en el BCRA, que sale del balance diario del BCRA (Informe Monetario Diario). Infobae lo cita en USD 4.387 M al 03-08-2026 (CLM-AO-033). El Informe Monetario Mensual de septiembre de 2026 del BCRA muestra depósitos del sector público no financiero en dólares, pero la copia del BCRA devolvió 502 y solo lo vi en un resumen de búsqueda, así que no lo uso como cifra. Ver `unresolved.md`.

## 5. Intereses de octubre de 2024 (pedido 5)

Tabla: `tablas/intereses_aif_vs_presupuesto_abierto_vs_a5.csv`.

- AIF, octubre de 2024: intereses netos $223.522,5 M, unos USD 227,7 M. A.5: interés pagado en moneda extranjera USD 1.265,7 M (CLM-AO-034). Brecha de unos USD 1.038 M.
- **La causa es de calendario.** La OPC informa que a principios de octubre de 2024 el Tesoro pagó por adelantado los vencimientos de enero de 2025 de intereses de los títulos globales por el equivalente a USD 1.056 M (CLM-AO-037). El BCRA, en su informe de mercado de cambios de octubre de 2024, habría registrado unos USD 1.050 M como giro anticipado (dato por resumen de búsqueda, confianza media, CLM-AO-038).
- **El AIF lo registra en enero de 2025:** intereses netos USD 1.758,5 M frente a USD 677,5 M de A.5 (CLM-AO-035). Sumando octubre de 2024 y enero de 2025, AIF USD 1.986,2 M contra A.5 USD 1.943,2 M, una diferencia de USD 43 M (CLM-AO-036). Con noviembre y diciembre incluidos, AIF 3.259,8 y A.5 3.088,0.
- Nota: la cifra de A.5 de octubre de 2024 en esta versión del boletín es USD 1.265,7 M, no USD 1.242 M como citó Claude. En Presupuesto Abierto el pago no aparece como interés de títulos en moneda extranjera (USD ~0 en octubre de 2024 y enero de 2025, CLM-AO-039), así que esa fuente no sirve para ubicar el giro.

## 6. Pendientes de publicación (pedido 6)

- **Deuda al 30-09-2026:** publicada. Boletín mensual de septiembre de 2026 (PDF y xlsx, 15-10-2026), ya registrado por Claude como SRC-9001 y SRC-9002 (copia propia como SRC-2049). Lo usé.
- **Balance cambiario de septiembre de 2026:** no publicado. El portal del BCRA lo lista para el 30-10-2026 (CLM-AO-041). Está publicado el de agosto de 2026.
- **Informe sobre Bancos de septiembre de 2026:** no publicado. El portal lista el Informe sobre Bancos del 16-10-2026, que corresponde a los datos de agosto (el de julio salió el 18-09-2026). El PDF y el anexo del BCRA devolvieron 502 desde la box el 17-10-2026, así que no pude confirmar si ya está el de agosto.
