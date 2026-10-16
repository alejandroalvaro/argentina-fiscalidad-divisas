# Lote AI: lo que no encontré o quedó a medias

## 1. Compras de divisas del Tesoro

1. **No hay serie oficial que separe MLC, block trades y MAE.** Los informes mensuales del BCRA dan una sola cifra del Tesoro "en el mercado de cambios" (compras o ventas netas con entidades) y otra de "compras directas al BCRA". No encontré comunicado del Ministerio de Economía con cifras mensuales ni el detalle de los bloques. La prensa cita dos bloques de USD 100 millones el 23-06-2025 y otra compra el 03-07-2025 (SRC-1661, no oficial); el informe del BCRA registra 175 en junio y 1.229 en julio de 2025 y no dice cuánto fue en bloque.
2. **Depósitos del Tesoro en moneda extranjera.** El BCRA no publica una serie en dólares: la variable 1266 de la API está en millones de pesos. Los dólares de la tabla mensual son mi cálculo (pesos del día dividido por el tipo de cambio mayorista de referencia del mismo día, variable 5). Coincide con seis cifras que difundió la prensa (3.157, 3.605, 4.387, 3.866, 5.285 y 485 millones de USD, con diferencia de hasta 1), pero no es una cifra oficial en dólares.
3. **Compras al BCRA en dólares.** La variable 48 está en pesos; los dólares de la tabla diaria son pesos del día divididos por el tipo de cambio del día. Cada operación grande coincide con el monto que dio la prensa (por ejemplo 2.319, 158, 279, 787, 115, 1.700, 597 y 919 millones en 2026).
4. **Diferencias entre el informe del BCRA y la variable 48.** Quedan sin explicar: abril de 2024 (el informe de ese mes publicó 468 y el de abril de 2025 corrige a 2.325); enero y febrero de 2025 (1.500 en total, que figuran en los informes hasta septiembre de 2025 y no están en el acumulado de octubre de 2025 en adelante); febrero de 2026 (787 el 5 de febrero según la variable 48, que la tabla de febrero no cuenta como "directo con BCRA"); y el acumulado 2026 del informe de agosto (3.335) menor que el de julio (6.088).
5. **Tablas de 2026 leídas a ojo.** En los informes de febrero a agosto de 2026 el Cuadro I.1 es una imagen sin texto. Cargué sus cifras mirando la imagen, con confianza media. Las frases del resumen ejecutivo, que sí son texto, confirman las cifras del Tesoro en el mercado.
6. **Septiembre de 2026.** El informe de evolución del mercado de cambios de septiembre no está publicado al 2026-10-16 (cuatro URL probadas, todas con 404). En la tabla mensual las columnas del informe quedan como n/d; la variable 48 no registra compras en septiembre. Octubre es parcial (hasta el 14).
7. **Datos que no usé.** No revisé el balance del BCRA ni el informe de política monetaria por compras del Tesoro; el informe de mercado de cambios cubre lo pedido.

## 2. Recompra de Letras Intransferibles

1. **El pedido decía abril de 2025.** El desembolso del FMI de USD 12.000 millones ingresó el 15 de abril de 2025 y la recompra se hizo el 6 de mayo de 2025 (Resolución Conjunta 21/2025, SRC-1257). En abril no hubo norma de recompra: el 10 de marzo de 2025 el Decreto 179/2025 ya la había habilitado.
2. **Hubo cuatro operaciones, no una:** 6-05-2025 (USD 12.000 millones), 11-08-2025 (USD 2.000 millones), 26-05-2026 ($ 18,4 billones, unos USD 13.225 millones de valor efectivo según mi cálculo) y 10-08-2026 (USD 781,5 millones). Las tres últimas son de otras fuentes de fondos (desembolso del FMI de la primera revisión, dividendos del BCRA y un arreglo con Bopreal), no de la de abril.
3. **Estimación oficial frente a mi suma.** Economía estimó USD 21.700 millones de valor nominal original para la operación de mayo de 2026 (SRC-1660); la suma de los ocho valores nominales de la Resolución Conjunta 27/2026 da USD 20.433,7 millones. No sé a qué se debe la diferencia de 1.266 millones.
4. **La operación de agosto de 2026 con Bopreal.** La explicación de que el Tesoro le dio Bopreales al BCRA, con los pesos le compró dólares y con esos dólares recompró letras viene de una fuente anónima citada por Bloomberg Línea (SRC-1664). No encontré documento oficial que la describa.

## 3. Conferencia del 11-04-2025

1. **No hay transcripción oficial.** El Ministerio de Economía publicó el video completo (SRC-1668, canal oficial de YouTube, 2 h 2 min) y no encontré versión taquigráfica en argentina.gob.ar ni en casarosada.gob.ar. Lo que hay en la tabla son los subtítulos automáticos de YouTube, con errores posibles (por ejemplo "100" en lugar de "1.400" en la banda superior, y "2025" donde seguramente se dijo 2024).
2. **Oradores sin identificar.** Los subtítulos no marcan quién habla. Por el contexto el tramo de la recompra es de Caputo; el de las bandas puede ser de Bausili, pero eso es inferencia mía. Revisar con el video antes de atribuir las frases.
3. **Tesoro y mercado de cambios.** En la conferencia no aparece una frase sobre compras de dólares del Tesoro en el mercado. Lo más cercano son las frases sobre el destino de los dólares (100% a recomprar letras) y sobre el BCRA dentro y en los extremos de la banda.

## 4. Pendientes

1. **Corte de deuda al 30-09-2026 y presentación del tercer trimestre.** No están publicados al 2026-10-16. La página oficial de datos trimestrales de la deuda (SRC-1601) lista como último corte el del 30-06-2026. Las URL con el patrón de nombre habitual dan 404.
2. **Balance cambiario de septiembre de 2026.** No está publicado (ver punto 1.6). El anexo estadístico (SRC-1604) llega hasta agosto de 2026.
