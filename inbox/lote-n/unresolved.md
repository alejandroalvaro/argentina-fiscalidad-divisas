# Lote N: lo que no se pudo resolver (sin_revisar)

Todo lo de este lote queda `sin_revisar`. No se infirió nada por analogía.

## 1. Rezago del CER de Discount, Par y Cuasipar en pesos (pedido 1): resuelto con avisos, con estos límites

**Para Claude:**

a) **Hay avisos abiertos y alcanzan.** Los avisos de pago son notas de la Dirección de Administración de la Deuda Pública del Ministerio de Economía al BCRA, MAE, la Bolsa de Comercio y Caja de Valores, y MAE las publica en un archivo abierto (SharePoint público). Cargué 21 (Discount de 2019-06 a 2026-06, Par de 2020-03 a 2026-09 y Cuasipar de 2025-06 a 2026-06). Dos avisos de Par rotulan las fechas de la división: "(13/03/2020 / 16-12-2003): 13,8928" y "(16/03/2021 / 16-12-2003): 19,2633" (CLM-N-022). Resultado: **diez días hábiles** (numerador: CER del décimo día hábil anterior al vencimiento; denominador: CER del 16-12-2003), en los 20 avisos verificados con una diferencia relativa máxima de 5,5e-6 (CLM-N-023, `tablas/verificacion_rezago_cer_avisos_de_pago.csv`). La Resolución MAE "C" 1498 de 2006 dice lo mismo con palabras: "10 días hábiles anteriores a la fecha de vencimiento" (CLM-N-027).
b) **Límite del cálculo:** "día hábil" lo conté con los días en que el BCRA publicó el A3500 (proxy). Con ese proxy los 20 avisos cuadran; con el noveno, el undécimo o diez días corridos no. No cargué un calendario de feriados.
c) **El 16-12-2003 como décimo día hábil antes del 31-12-2003** es coherente con los avisos, pero **no lo verifiqué contra un calendario de 2003** (la serie A3500 del BCRA no cubre 2003 en lo que tengo). Lo que sí está medido es que los avisos usan el denominador **1,4551**, que es el CER del BCRA del 2003-12-16 (1,45506393984) redondeado a cuatro decimales; con el valor sin redondear la diferencia con los avisos sería de unos 2,5e-5, mayor que el máximo observado.
d) **Diferencia con el lote M:** la valuación de Finanzas al corte usa el CER del día sobre 1,4568 sin rezago; el aviso usa CER(10 días hábiles antes)/1,4551. Al 2026-06-30: 548,60 contra 543,94, es decir 0,86% (CLM-N-024). Es la distancia que Claude ya documentó en `docs/FASE2_MOTOR.md`.
e) **Coeficientes de capitalización:** los avisos dicen 1,2699357 (Discount) y 1,3885916 (Cuasipar); el prospecto con las tasas semestrales da 1,2699367 y 1,3885928, diferencia de 8e-7 (CLM-N-025). No sé por qué difieren en la séptima cifra (redondeo de la ONCP o un cálculo por tramos). Para pagos, el aviso es lo que se aplicó.
f) **Lo que no cargué:** avisos de Discount de 2018 (el de 2018-06 es un escaneo sin texto), de Par anteriores a 2020 y de Cuasipar de 2019 a 2024 (los enlaces están en las fichas de `SRC-1044` a `SRC-1046`; son los mismos formatos). El Anexo III del Decreto 1735/2004 sigue sin estar publicado; los avisos y la Resolución MAE 1498 cubren la regla del CER pero no reemplazan al anexo.
g) Las fichas de Mercados Argentina (`SRC-1044` a `SRC-1046`) son de terceros y las usé solo como índice de enlaces a MAE; ninguna cifra sale de ellas.

## 2. RC 53 y 60/2026 y SIGADE al 2026-09-30 (pedido 2)

**Para Claude:** sin publicación nueva (`tablas/rc53_rc60_2026_y_sigade_revision_lote_n.csv`). ONCP: última planilla de colocaciones 31-08-2026 (CLM-N-028) y las direcciones de septiembre y octubre devuelven 404. OPC: el informe de septiembre devuelve 404 y el monitor de novedades llega hasta la RC 58/2026 (BO 2026-09-30); la RC 53 figura y la RC 60 no. Finanzas: última planilla 30-06-2026. Volver a buscar cuando ONCP publique el corte del 2026-09-30.
