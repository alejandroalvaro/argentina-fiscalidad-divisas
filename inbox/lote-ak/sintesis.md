# Síntesis, lote AK: lo que falta para saber quién cobra

Todo `sin_revisar`. Fuentes SRC-1716 a SRC-1770; reutiliza SRC-1166 (FGS, junio 2026) y la nota del programa financiero del lote AJ. Los cálculos propios están marcados.

## 1. FCI: lo que sí hay y lo que no

**Fuente:** el Resumen Mensual de la industria que publica la CAFCI (44 PDF, enero 2023 a agosto 2026, todos bajados, con sha256). La CNV no publica un informe mensual equivalente: lo suyo es la cartera semanal fondo por fondo (más de mil fondos), que no bajé.

**Lo que abre el informe:** por clase de fondo (mercado de dinero, renta fija, mixta, variable, retorno total, infraestructura, títulos del Tesoro), la cartera en operaciones a plazo, títulos de deuda, títulos públicos y, dentro de estos, **deuda nacional** (pesos y dólares juntos), provincial, extranjera y municipal. Cauciones, plazo fijo y pases aparecen separados **solo desde marzo de 2026**.

**Lo que no abre:** LECAP, BONCAP, CER, duales ni ningún instrumento. No hay forma, con CAFCI, de separar la deuda nacional por especie. Tampoco hay una clase "T+1" separada: esos fondos están dentro de mercado de dinero o renta fija.

Tablas:
- `tablas/cafci_cartera_fci_por_clase_mensual_2023_2026.csv`: 257 filas mensuales por clase donde el PDF trae la tabla en texto (faltan meses, ver `unresolved.md`).
- `tablas/cafci_tenencias_por_clase_de_fondo_cierres_2023_a_ago2026.csv`: cierres de diciembre 2023, 2024, 2025 y agosto 2026 por clase de fondo y de activo (completos, del PDF de agosto de 2026).

Deuda nacional en cartera de los FCI abiertos (millones de pesos, cierres):

| Clase de fondo | dic-23 | dic-24 | dic-25 | ago-26 |
|---|---|---|---|---|
| Industria total | 5.374.804 | 12.638.418 | 12.149.082 | 21.354.614 |
| Renta fija | 4.216.602 | 9.478.972 | 8.849.657 | 16.412.258 |
| Renta mixta | 699.594 | 1.984.114 | 1.987.850 | 2.476.369 |
| Retorno total | 98.620 | 410.360 | 520.328 | 949.625 |
| Mercado de dinero | 202 | 207.512 | 331.222 | 743.481 |
| Títulos del Tesoro | 134.752 | 282.716 | 175.228 | 41.519 |

Lecturas (cálculo propio sobre esas cifras):
- En agosto de 2026 la renta fija concentra el 77% de la deuda nacional en cartera de los FCI; el mercado de dinero apenas el 3%.
- Los fondos de mercado de dinero ($63 billones de patrimonio en agosto de 2026) tienen su plata en plazo fijo (57,1%), cauciones (11,9%) y disponibilidades (25,3%); en deuda nacional solo $743.481 millones (1,2%). Para esos fondos el vínculo con los instrumentos del Tesoro y el BCRA pasa por los bancos (plazos fijos, cuentas a la vista) y por las cauciones, no por tenencia directa de LECAP. Esta es una lectura, no un dato de la fuente.
- Cauciones en mercado de dinero (millones de pesos): mar-26 9.351.036; abr-26 6.862.243; may-26 7.379.879; jun-26 7.255.599; jul-26 7.266.182; ago-26 7.624.233.
- Unidades: el pie de la sección de industria dice "miles de millones", pero las cifras coinciden con millones de pesos (el total $111.686.701 equivale a los $111,10 billones del texto); en mercado de dinero el pie dice "millones". Usé millones.
- Fecha de cartera: el patrimonio es al cierre del mes y la cartera a la última fecha de información (agosto de 2026: 28/08).

## 2. FGS

Los informes mensuales del FGS no abren la cartera por especie. Lo que abren: categorías (bonos CER, TAMAR, tasa fija, dólar linked, letras en pesos, letras en USD, etc.). Con el lote AB (cierres 2024 a 2026) y este lote queda una serie de cierres trimestrales por categoría desde septiembre de 2023, con la excepción de diciembre de 2024.

Nuevo en este lote (`tablas/fgs_titulos_publicos_por_categoria_sep_y_dic_2023.csv`), millones de pesos:

| Categoría | sep-23 | dic-23 |
|---|---|---|
| Bonos $ CER | 5.460.928 | 11.199.448 |
| Bonos $ dólar linked | 4.498.507 | 11.992.320 |
| Letras $ | 1.526 | 21.098 |
| Total títulos públicos nacionales | 13.410.207 | 28.468.004 |

- Referencia de junio de 2026 (SRC-1166): CER $54.679.488 millones (44,3% del FGS), TAMAR $9.102.296, letras en pesos $5.314.279, total $95.851.048.
- Tenencia del FGS en FCI por clase (`tablas/fgs_tenencia_en_fci_por_clase_2021_a_jun2026.csv`): money market $47.688 millones en dic-23, $79.673 en dic-25 y $239.018 en jun-26, sobre un total en FCI de $1.440.302 millones en jun-26. Es poco frente a los $95 billones en títulos.
- Ni los informes anteriores a septiembre de 2023 que probé ni diciembre de 2024 se pudieron leer (ver `unresolved.md`). No hay LECAP, BONCAP ni duales por separado: "Letras, $" es lo más cercano a LECAP, y lo que el lote AB observó sobre dólar linked sigue sin aclarar.
- El texto de los PDF se leyó con el lector web: ANSES bloquea la descarga directa. Por eso esas fuentes no tienen sha256.

## 3. LEFI

**Reglas** (Resolución Conjunta 40/2024, Boletín Oficial 18-07-2024): emisión 17-07-2024, vencimiento 17-07-2025, hasta VNO $20 billones, interés a la tasa nominal anual de política monetaria del BCRA con capitalización diaria, pagadero al vencimiento; en cada cambio de tasa se capitaliza; el BCRA calcula; solo se negocia entre el BCRA y las entidades; se colocó por canje con el BCRA. La fórmula exacta es una imagen en el Boletín Oficial, no está en el texto.

**Tasa** (API del BCRA, variable 160 TNA y 161 TEA, diarias): 40% TNA (49,15% TEA) hasta el 31-10-2024; 35% (41,88%) desde el 01-11-2024; 32% (37,69%) desde el 06-12-2024; 29% (33,63%) desde el 31-01-2025; la serie termina el 10-07-2025. Las TEA coinciden con capitalización diaria sobre 365 días ((1+TNA/365)^365-1), lo que respalda esa base de cálculo (es una verificación mía, no un texto oficial).

**Saldos** (variable 196, LEFI en cartera de entidades, valor técnico): arrancan el 22-07-2024 con $10.852.365 millones (la nota del BCRA habla de $10,85 billones suscriptos el primer día), máximo $16.590.358 millones el 28-11-2024, $15.494.780 millones el 08-07-2025 y cero desde el 10-07-2025. Flujo diario (variable 58, efecto monetario de las operaciones con LEFI): -$10.852.365 millones el 22-07-2024 y +$15.519.412 millones el 10-07-2025.

**Tablas:**
- `tablas/lefi_diaria_tasa_saldo_y_flujo_2024-07_a_2025-07.csv`: serie diaria oficial (tasa TNA, TEA, saldo, flujo).
- `tablas/lefi_mensual_calculo_interes_devengado_sobre_cartera_de_entidades.csv`: **cálculo propio**, interés devengado mensual estimado sobre la cartera de entidades (saldo del día previo por TNA/365, por día calendario). Suma julio 2024 a julio 2025: unos $3,41 billones. Control cruzado: la suma del flujo diario de la variable 58 en el período es $3.413.024 millones, casi igual, lo que sugiere que equivale a los intereses capitalizados pagados a las entidades al cerrar sus posiciones.

**Qué cubre y qué no:** la serie 196 es solo la cartera de las entidades. Las LEFI que quedaron en el BCRA (parte de los $20 billones del canje) no figuran; el interés sobre esas es una cuenta entre el BCRA y el Tesoro, no un pago al sector privado. El monto emitido total tampoco figura en una serie oficial que haya encontrado. Para saber quién cobró, la cifra relevante es la de entidades (bancos): unos $3,4 billones en el año, devengados por el Tesoro y cobrados por los bancos (la letra era del Tesoro). Esta frase es una lectura de la letra y del flujo, no un dato de una fuente.

## 4. Programa financiero 2026 y 2027

La presentación de julio de 2026 (5 páginas) bajó esta vez sin problema (SRC-1770). Cuadro `tablas/programa_financiero_2026_2027_dolares_del_tesoro.csv`, USD miles de millones:

| Concepto | 2026 | 2027 |
|---|---|---|
| Necesidades | 19,2 | 24,9 |
| Vencimientos de capital | 9,3 | 15,7 |
| Vencimientos de intereses | 8,9 | 9,2 |
| Capitalización del BCRA | 1,0 | sin dato |
| Fuentes | 22,9 | 24,9 |
| Compra de USD al BCRA | 6,7 | 4,9 |
| Emisiones locales | 6,0 | 5,0 |
| Fuentes menos necesidades | 3,7 | 0,0 |

- Cita relevante: "La nueva deuda se emite exclusivamente para refinanciar el capital de la deuda heredada; los intereses se pagan con superávit fiscal".
- El programa cuenta la compra de dólares al BCRA como fuente de los dólares del Tesoro, con pesos del Tesoro: USD 6,7 mil millones en 2026 y USD 4,9 mil millones en 2027. Eso es la compra al BCRA, no la compra en el mercado, y no indica con qué pesos se pagan.
- La nota al pie sobre emisiones locales dice "USD 4 billones", casi seguro un error de tipeo por USD 4 mil millones (el total de emisiones locales es 6,0). Lo dejo tal cual en la cita y lo señalo.
