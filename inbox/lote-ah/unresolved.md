# Huecos del lote AH

## 1. Oro, plata y minería

1. **2020 sin norma propia hallada.** Para 2020 (antes de que el 785/2020 y el 1060/2020 listen las posiciones) usé la regla general del Decreto 793/2018: 12% a todas las posiciones NCM hasta el 2020-12-31. Es inferencia producto por producto. No busqué si otra norma tocó 7106, 2603 o 2836.91 en 2020.
2. **El 12% del oro en el anexo del 1060/2020 choca con el tope de la ley.** El art. 52 de la Ley 27.541 dice que para minería no se puede superar el 8%, y el anexo del 1060/2020 deja 7108.11, 7108.13 y 7108.20 en 12%. No encontré explicación. Dejé la alícuota del anexo, tal como está en `alicuotas/eventos.csv`.
3. **Oro en bruto desde 2024-01-01.** No aparece en ningún anexo que procesé después del 908/2021. La prensa (La Nación y Bloomberg Línea, SRC-1623 y SRC-1624) dice que quedó sin retención al vencer el 8%. Lo cargué como 0% inferido, sin norma.
4. **Oro semilabrado y monetario (7108.13, 7108.20).** Sigue en 12% según los anexos revisados (305/2025, 38/2025, 697/2024, 423/2026, 566/2026 y 563/2025). No busqué normas fuera de esos.
5. **Plata y litio.** Siguen en 4,5% según el anexo del 1060/2020, el comunicado del 563/2025 y la ausencia de 7106 y 2836.91.00 en los Anexos I y II del 566/2026. La ausencia sale de buscar sobre texto extraído de PDF.
6. **No hay alícuota general para lo no listado después de 2020.** El art. 52 de la Ley 27.541 no fija alícuotas, solo topes (33%, 15%, 5% y 8%). El Decreto 793/2018 caducó el 2020-12-31. No encontré una norma que fije un piso o una alícuota residual desde 2021; si una posición no figura en un anexo, la tomé como 0%.
7. **Cobre, Decreto 308/2022.** Registro optativo con alícuota variable (0% hasta USD 7.700 por tonelada y 8% desde USD 11.500, según la prensa). No leí el texto del decreto ni sé si alguien se inscribió; el 563/2025 dice que no tuvo beneficiarios.
8. **Decreto 423/2026 Anexo III** (SRC-1588): lo bajé y busqué los códigos de este lote, sin coincidencias. No lo leí completo.

## 2. Gas y combustibles

1. 2711 (todas las aperturas) sigue la fórmula móvil del Decreto 488/2020, desde el 2020-05-19. No encontré una norma que lo cambie. El PI sale del XLSX de Energía (SRC-1566).
2. Las aperturas que figuran en el anexo del 488/2020 las tomé de las descripciones del PDF. Hay filas de 2710.12 y 2710.19 con códigos de seis o siete cifras en el anexo (2710.12.2, 2710.12.4, 2710.12.5, 2710.19.1, 2710.19.2, 2710.19.3, 2710.19.9). En la tabla puse las aperturas de ocho cifras; revisá que coincidan con la nomenclatura de los zips de ARCA.
3. 2710.20, 2710.91 y 2710.99 tienen alícuota propia de 12% (anexo del 1060/2020), no la fórmula.
4. Desde el 2026-07-01 el 8% de la fórmula se reemplaza por un cronograma mensual para 2707.30.00, 2707.99.90, 2710.12.10, 2710.12.30, 2710.12.90 y 2710.19.19 (Decreto 566/2026 art. 3 y Anexo III). Vale tanto cuando el PI llega al valor de referencia (quinto párrafo del art. 7 del 488/2020) como en la fórmula intermedia (sexto párrafo). En la tabla la alícuota queda vacía porque depende del PI de cada mes.

## 3. Crudo convencional, Decreto 59/2026

1. **Inicio de efectos ambiguo.** El decreto rige desde 2026-01-30, pero surte efectos desde el dictado de las normas de la SE (la Resolución 42/2026 está fechada 2026-02-18 y se publicó el 2026-02-20) o a los 60 días de publicado (2026-03-30), lo que ocurra antes. Puse 2026-02-18; si preferís la fecha de publicación, es 2026-02-20.
2. **No hay serie oficial de exportaciones que separe convencional de no convencional** que yo haya podido verificar. Lo más cercano: la producción por pozo de Capítulo IV tiene `tipo_de_recurso` (SRC-1595, ficha; el CSV, SRC-1596, no responde desde la box ni desde la Mac). La Resolución 42/2026 fija el porcentaje de convencional por área de concesión, no por exportación. Los Tableros del Sistema de Mediciones (SRC-1594) tienen exportaciones diarias; no verifiqué si abren por tipo de recurso.
3. El PDF del decreto en ARCA (`decreto59.pdf`) tiene 7 KB y no se pudo leer; usé el texto de Presidencia (SRC-1525, de lotes anteriores).

## 4. Licitación del 14-10-2026

1. El comunicado oficial (SRC-1597 y SRC-1598) da los montos por instrumento pero **no los vencimientos cubiertos ni la tasa de rollover**. El 136,14% está en la prensa (Infobae SRC-1621, Economis y Reuters). Vencimientos de unos $ 4,86 billones según Punto Federal (SRC-1622) y de unos $ 4,9 billones según Reuters. El cálculo 6.610.275 / 1,3614 da 4.855.498 millones: es un cálculo mío.
2. Los vencimientos del día no aparecen en el llamado (SRC-1599). No busqué el cronograma de vencimientos en la página de Finanzas ni en el Boletín Oficial.
3. Los USD 727 millones de VNO de TMVE8 se expresan en pesos al A3500 del 2026-10-13 (USD 1.515,8543). El rollover de la prensa mezcla pesos y ese equivalente.

## 5. Corte del tercer trimestre de 2026

**No está publicado** al 2026-10-16 (11:30 hora de Bahía). La página de datos trimestrales (SRC-1601) llega hasta `deuda_publica_30-06-2026_0.xlsx`; las URL `deuda_publica_30-09-2026.xlsx` y `deuda_publica_30-09-2026_0.xlsx` dan 404. Tampoco hay presentación gráfica del tercer trimestre; la última es la del segundo (SRC-1602, `presentacion_grafica_2do_trim_26.pdf`). Volvé a mirar la página en unos días.

## 6. Balance cambiario del BCRA

1. **Septiembre de 2026 no está.** El XLSX llega a agosto de 2026 y el informe de septiembre da 404. Para enero de 2024 a agosto de 2026 hay 32 meses.
2. **No hay una línea con el nombre exacto "formación de activos externos del sector privado no financiero".** En la hoja `Balance Cambiario` aparecen "Compra-venta de billetes y divisas sin fines específicos del sector privado no financiero", "Formación de activos externos del sector financiero (PGC)" y "Formación de activos externos del sector público". La compra de billetes de personas humanas está en `Datos Mercado de Cambios` (sector Personas Humanas). La estimación de lo que se quedó en activos externos (por ejemplo USD 700 millones en agosto) aparece solo en el texto del informe PDF, no en el XLSX. No busqué todas las columnas de las 254 de la hoja.
3. El XLSX pesa 18 MB; la hoja larga tiene 269.748 filas. Las cifras son "provisorias, sujetas a revisión" según la nota 1 de la hoja `Observaciones`.
4. Los desembolsos del FMI y las operaciones de organismos internacionales no entran todas en el mercado de cambios (notas 2 y 6 de la hoja `Observaciones`).

## 7. FMI, acuerdo de 2025

1. **Los comunicados del FMI (SRC-1612 a SRC-1614) dan 403 con curl.** Los leí con una herramienta de lectura web. Las tablas salen de los informes del personal, copiados por el BCRA (SRC-1609 a SRC-1611), que sí bajan.
2. **Monto inicial.** El comunicado de la primera revisión dice 10.729 millones de DEG girados en total; la tabla 13 da 9.160 + 1.529 = 10.689. El total de 11.452 al 2026-06-30 solo cierra con 9.160 + 1.529 + 763. El comunicado de la segunda revisión dice "SDR 0,8 mil millones" para 763.
3. **Fechas de ingreso.** Son las que informa la prensa (SRC-1618 a SRC-1620): 2025-04-15, 2025-08-04 y 2026-05-26. No encontré la fecha de valor del FMI en una fuente oficial. Para la primera, un resultado de búsqueda atribuye al informe monetario del BCRA un ingreso de USD 12.396,4 millones (no lo bajé ni lo verifiqué).
4. **Tercera revisión** (636 millones de DEG, disponible desde 2026-07-31): sin aprobación al 2026-09-30 (el monto girado sigue en 11.452). La prensa del 15 de octubre dice que sigue abierta y que Argentina pide un waiver. No lo verifiqué en fuente oficial.
5. **DEG por dólar.** Hay valor para cada fin de mes de abril de 2025 a septiembre de 2026, con el último día publicado en la página mensual. En noviembre de 2025 la página termina el día 26. La tabla tiene también marzo de 2025 (cierre previo al desembolso).
6. Los pagos del FMI a Argentina (principal y cargos de ambos acuerdos) están en SRC-1615 por año, no por fecha.
