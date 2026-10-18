# 7. La opacidad como dato

Reconstruir los dos circuitos llevó más trabajo del que debería. Este capítulo trata ese esfuerzo como un resultado: qué hubo que reunir, qué series no existen, qué cifras cambian de una publicación oficial a otra y qué errores aparecieron en archivos oficiales. Ninguno de estos problemas impide, por sí solo, saber cuánto debe el Estado. Juntos hacen muy difícil saber en qué moneda, a quién y con qué recursos se paga.

::: {.destacado custom-style="Destacado"}
**El saldo de la deuda es transparente; reconstruir sus movimientos exige cruzar publicaciones con criterios distintos.**

Entre diciembre de 2023 y agosto de 2026, el esquema ahorro-inversión-financiamiento de la Secretaría de Hacienda registra 121.405 millones de dólares de amortización de deuda "en moneda extranjera". De esa cifra, 45.325 millones fueron deuda escrita en dólares que se pagó en pesos. Leer toda esa amortización como pagos efectivos en divisas sobreestimaría estos últimos, que fueron 76.080 millones, en aproximadamente un 60%.

*Alcance.* El porcentaje vale para la amortización de esa fuente en esa ventana, con los pagos efectivos en divisas como denominador; no se extiende al stock de la deuda. Responde al criterio de clasificar por moneda de denominación, que la estadística aplica de manera coherente, y no supone ninguna intención de ocultar.
:::

## 7.1 El tamaño del trabajo

Para llegar a los diagramas y tablas de este informe hubo que reunir:

- 1.291 fuentes distintas, en 50 lotes de búsqueda, con 1.404 afirmaciones registradas;
- 1.214 documentos originales guardados, cada uno identificado por su huella sha256, y 1.540 descargas registradas;
- más de 750 operaciones de deuda en SIGADE y los términos de emisión de 101 instrumentos, cargados a mano desde prospectos y resoluciones;
- cerca de 640 preguntas que quedaron sin respuesta en los registros de lo no encontrado de cada lote.

El saldo de la deuda es transparente: SIGADE, la planilla trimestral y el perfil de vencimientos coinciden al dólar, y eso es una virtud que no todos los países tienen. La opacidad está en los movimientos, en la moneda en que se paga y en quién tiene cada bono.

## 7.2 Series que no existen

- **Los depósitos del Tesoro en dólares**, en dólares. El BCRA publica los depósitos del Gobierno en moneda extranjera convertidos a pesos. Para saber cuántos dólares tiene el Tesoro hay que reconvertirlos día por día.
- **Los depósitos del Tesoro en dólares en el Banco Nación.** No hay serie.
- **Las compras de divisas del Tesoro** separadas por vía (al BCRA, en el mercado, en operaciones en bloque). El BCRA informa las compras al BCRA en pesos, y las del mercado aparecen en comunicados con cifras que después cambian.
- **Con qué pesos se compra cada dólar.** No hay un comunicado, compra por compra, que diga si los pesos vinieron del superávit, de deuda o de depósitos.
- **El esquema ahorro-inversión-financiamiento abierto por instrumento o por acreedor.** La amortización y la colocación de deuda se publican como totales por moneda, sin decir qué se pagó.
- **Una nota metodológica** sobre cómo se clasifica la deuda escrita en dólares que se paga en pesos (dólar linked, BONTE y Letras del Tesoro (LETES) que pagan en pesos, BONAR DUAL). El Manual de Clasificaciones de 2026 no nombra esos instrumentos y tiene dos reglas escritas que se contradicen.
- **La deuda en pesos en pesos.** La Secretaría de Finanzas publica la deuda en pesos convertida a dólares.
- **La tenencia de cada bono.** No se publica quién tiene cada instrumento, ni dentro ni fuera del sector público. El FGS publica su cartera por categoría y nunca por especie.
- **Las LEFI.** No hay serie del total emitido ni de la parte que quedó en el BCRA. La fórmula de capitalización está publicada como imagen en el Boletín Oficial.
- **El interés que paga el BCRA, por mes.** Los estados contables son anuales y se reexpresan.
- **La tasa promedio del stock de plazos fijos** y el ranking oficial de fondos comunes por patrimonio.

## 7.3 Cifras que cambian de una publicación a otra

| Dato | Lo que dice cada fuente |
|---|---|
| Recompra de Letras Intransferibles de mayo de 2026 | 21.700 millones de USD (Ministerio de Economía); 20.434 o 22.284 (resoluciones); 21.000 (BCRA); 13.225 efectivos (cálculo con la resolución). Pesos usados: $18,4 billones (resolución y comunicado) o $12 billones (Informe de Política Monetaria de junio de 2026) |
| Variación de las reservas netas en 2025 | −12.100 millones (informe del personal del FMI) o −9.600 (carta de intención, mismo documento) |
| Compras de divisas del Tesoro en 2025 | 2.727 o 1.216 millones, según la serie del BCRA |
| Compras al BCRA de enero y febrero de 2025 | 1.500 millones que desaparecen del acumulado en el informe de octubre de 2025 |
| Compras de abril de 2024 | 468 millones en el informe del mes, 2.325 un año después |
| Acumulado de compras de 2026 | 6.088 millones en el informe de julio y 3.335 en el de agosto |
| Desembolsos del FMI | 10.729 millones de DEG (comunicado) o 10.689 (suma de los tramos del cuadro) |
| Intereses en moneda extranjera de octubre de 2024 | 1.242 o 1.265,7 millones de USD, según la edición del boletín |
| Endeudamiento en 2025 | AIF mensual: $195,6 billones local y $35,2 billones en moneda extranjera. Cuenta de Inversión: $67,2 y $3,8 billones |

Ninguna de estas diferencias es en sí un error. Muchas tienen explicación: valor nominal contra efectivo, fecha de concertación contra fecha de liquidación, criterios distintos. El problema es que la explicación casi nunca está publicada, y el lector tiene que reconstruirla con los documentos originales.

## 7.4 Lo que se llama "moneda extranjera"

El caso más importante para este informe es la clasificación de la deuda por moneda en el esquema ahorro-inversión-financiamiento de la Secretaría de Hacienda. Entre diciembre de 2023 y agosto de 2026, la amortización de deuda "en moneda extranjera" de ese esquema suma 121.405 millones de dólares. De esa cifra, 45.325 millones fueron deuda escrita en dólares que se pagó en pesos, de modo que lo pagado en dólares fue 76.080 millones. Del lado de la colocación pasa lo mismo: de 83.563 millones "en moneda extranjera", 19.413 se colocaron por pesos y 64.150 entraron en dólares.

El criterio, además, cambia entre publicaciones:

- la Cuenta de Inversión 2024 cuenta el BONTE dólar linked como colocación en moneda extranjera, y la de 2025 no;
- la Oficina Nacional de Crédito Público clasificaba hasta 2025 los BONTE en dólares que pagan en pesos como moneda extranjera y las letras vinculadas al dólar (LELINK) como moneda nacional; en 2026 pasó a clasificar por moneda de pago y movió los BONTE a moneda nacional;
- el boletín de Finanzas cuenta la deuda dólar linked como moneda local en el cuadro A.3 y como moneda extranjera en el A.1;
- el cuadro A.4 del boletín incluye canjes sin caja: la RC 16/2024 dio de baja BONAR DUAL y BONTE en dólares por 25.173 millones que el esquema ahorro-inversión-financiamiento no muestra.

Un lector que quiera saber cuántos dólares necesitó el Tesoro y lea toda la amortización "en moneda extranjera" como pagos en divisas los sobreestima en aproximadamente un 60% (121.405 contra 76.080 millones, entre diciembre de 2023 y agosto de 2026). La clasificación por moneda de denominación es un criterio estadístico legítimo; el problema es que no se publica, al lado, la clasificación por moneda de pago. Para corregirlo, el informe tuvo que reconstruir la deuda pagada en pesos operación por operación desde las licitaciones y las resoluciones.

## 7.5 Errores en archivos oficiales y operaciones sin explicación

- **La estructura financiera de la Oficina Nacional de Crédito Público** repite en el Global 2035 la amortización del Global 2030.
- **El perfil oficial de vencimientos** subestima el capital a doce meses en 32.900 millones de dólares, sobre todo porque no incluye lo emitido después del corte (capítulo 2).
- **Las letras en garantía del FODER** figuran en SIGADE como deuda normal, con un calendario mecánico de 266 millones por año, cuando son deuda contingente.
- **Tres letras en pesos** (TMF27, TMG27 y TZX27) bajan de saldo sin una operación publicada que lo explique.
- **La RC 60/2026** nunca publicó sus montos.
- **La RC 30/2026** autorizó un pago de 1.040 millones de dólares que no aparece en los depósitos del Tesoro.
- **Los archivos de exportaciones de la Agencia de Recaudación y Control Aduanero (ARCA)** traen 81 registros con precios imposibles. Por ejemplo, en febrero de 2021 la soja en grano (1201.90.00) figura con 6.508 millones de dólares FOB por 37.325 toneladas, 174 dólares por kilo contra una mediana de 0,41. El informe los aparta con un filtro de valor unitario y los lista.

## 7.6 Demoras y portales

- **SIGADE** al 30 de junio de 2026 se publicó el 18 de septiembre, unos 80 días después. En ese lapso las licitaciones quincenales cambian unos 36.000 millones de dólares de capital a doce meses. El corte al 30 de septiembre no estaba publicado al 17 de octubre.
- **ANSES** bloquea la descarga automática de los informes del FGS; varios informes de 2023 y 2024 dan error 404.
- **El FMI** bloquea la descarga automática de sus informes; se usaron las copias que publica el BCRA.
- **El BCRA** devolvió errores 502 repetidos para el Informe sobre Bancos de agosto de 2026, y algunas rutas de archivos cambian sin aviso.
- **La Cámara de fondos comunes (CAFCI)** y el portal de datos del Ministerio de Agricultura rechazan la descarga automática.
- **La interfaz de series de datos.gob.ar** pierde observaciones al azar. Hay que usar los archivos estáticos.

## 7.7 Los errores propios

El método detectó también errores de los agentes que hicieron este trabajo, y conviene contarlos porque muestran lo fácil que es equivocarse con estas fuentes:

- una tabla de factores de la base monetaria preparada en un lote estaba mal en 27 de 45 meses, porque sumaba el bloque anual de la planilla al mes de enero;
- se leyó como dólares una cifra de intereses que estaba en miles de millones de pesos;
- se supuso que dos recompras de Letras Intransferibles se habían pagado con pesos, cuando se pagaron con dólares del FMI y con dólares que el BCRA entregó por BOPREAL;
- se infirió que la colocación de deuda en dólares por pesos se registraba como moneda local, y los datos de licitación mostraron lo contrario;
- en el segundo borrador, el total de las compras de dólares del Tesoro salía del informe mensual del BCRA y su apertura por vía, de la serie diaria. Las dos no suman lo mismo, porque el informe mensual omite una compra de 787 millones al BCRA del 5 de febrero de 2026. El tercer borrador usa una sola serie, el informe mensual, con esa compra agregada (capítulo 5);
- en el mismo borrador, 16.703 millones de dólares figuraban como valor nominal de la deuda con el BCRA cancelada con pesos. Es el equivalente en dólares de lo que se pagó; el valor nominal fue de 28.030 millones.

Cada error se corrigió contra el documento original. La diferencia sin explicar del Tesoro en dólares bajó, a medida que entraron las correcciones, de −18.221 a −4.150 y a −3.522 millones, y subió a −4.309 cuando se agregó la compra de febrero de 2026: esa compra cierra el mes en que ocurrió, y la suma de todos los meses, que compensa errores de signo contrario, se agranda.

## 7.8 Qué haría falta

La lista sale sola de lo anterior. Bastaría con que la Secretaría de Finanzas publicara la deuda en pesos en pesos y la tenencia por sector e instrumento; que Hacienda abriera la amortización y la colocación por instrumento y por moneda de pago, con una nota de método; que el BCRA publicara los depósitos del Tesoro en dólares en dólares y las compras del Tesoro por vía; y que las operaciones entre el Tesoro y el BCRA se informaran con su contrapartida y su precio. Casi todo eso ya existe dentro de la administración, porque sin esos datos no se podrían hacer los registros que sí se publican.
