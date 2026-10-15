# Lote M: lo que no se pudo resolver (sin_revisar)

Todo lo de este lote queda `sin_revisar`. No se infirió nada por analogía.

## 1. Bajas de TMF27 (485.000), TMG27 (415.000) y TZX27 (556.267,947 millones de pesos)

**Para Claude:**

a) **No encontré qué operación explica ninguna de las tres bajas ni su fecha.** La hipótesis (rescates con fondos de entes públicos o del BCRA fuera de licitación) **no tiene respaldo ni refutación** en lo que revisé. Revisé, y la lista está en `tablas/bajas_tmf27_tmg27_tzx27_fuentes_revisadas.csv`: ONCP colocaciones 2026 (hojas Bonos, Canjes- Conversiones y Otras Operaciones), novedades normativas de la OPC (resoluciones conjuntas 3 a 59 de 2026), los informes mensuales de la OPC de marzo a junio de 2026, las hojas A.2.2 y A.2.3 de las planillas de Finanzas y las presentaciones del I y II Trimestre 2026. Ninguna trae una fila, norma o párrafo que baje esos tres instrumentos.
b) **No encontré un boletín trimestral de ONCP con detalle por instrumento.** Lo que ONCP y Finanzas publican por trimestre es agregado (flujos y tenencias por acreedor), no por título. Tampoco hay Cuenta de Inversión de 2026: el ejercicio no cerró.
c) Dato agregado, neutro y no atribuible a un instrumento (CLM-M-013 y CLM-M-014): las tenencias de agencias del sector público subieron USD 19.393 millones en el primer trimestre de 2026 (200.249 a 219.641) y bajaron USD 22.428 millones en el segundo (219.641 a 197.213), y el sector privado subió USD 10.265 y USD 12.005 millones. Las dos bajas del segundo trimestre (900.000 millones de pesos) equivalen a unos USD 607 millones al A3500 del 2026-06-30; la de TZX27 del primer trimestre (556.268 millones) a unos USD 402 millones al A3500 del 2026-03-31. No afirmo relación entre esos agregados y las bajas: Finanzas no publica la tenencia por instrumento.
d) Qué haría falta: la planilla de colocaciones o el boletín de ONCP con la columna de operaciones del segundo trimestre, las tenencias por título del sector público (FGS, BCRA, otros) o la norma de la operación. No están publicados en lo que encontré.

## 2. Discount, Par y Cuasipar en pesos (pedido 2)

**Para Claude:**

a) **El texto de las Condiciones Aplicables (Anexo III del Decreto 1735/2004) no está disponible.** El Decreto sale publicado sin anexos en la Biblioteca de Normativas (CLM-M-002); Infoleg y el Ministerio de Economía no tienen los anexos, y direcciones de anexos que probé devolvieron una página de error. La única fuente de la fórmula del CER es el Suplemento de Prospecto en inglés (Anexo I, SRC-0626, CLM-M-001), que dice "CER corresponding to the 10-day period" sin aclarar si son 10 días corridos o hábiles ni si se promedia. Por eso **no puedo decir cuál es la base de la norma en números**: los candidatos son el CER del 2003-12-31 (1,45679881491), el de diez días corridos antes (2003-12-21, 1,45564200185) o el de diez días hábiles antes (no cargué el calendario de feriados de 2003, así que no lo calculé); `tablas/cer_bcra_2003_12_ventana_base.csv` trae la serie diaria para que elijas.
b) **Lo que sí está medido** (todo es cálculo de Grok sobre la planilla de Finanzas): el cociente VN actualizado sobre VN residual de la planilla implica una base de 1,4568 (con cuatro decimales; difiere en menos de 2 millonésimas del CER del BCRA del 2003-12-31) y **sin rezago** en el CER de cada corte, en los tres instrumentos y en las diez planillas de 2024-03-31 a 2026-06-30 (CLM-M-007, CLM-M-009 y CLM-M-011). Si Finanzas hubiera usado el CER de diez días antes en uno solo de los dos extremos, la base implícita se desviaría 0,08% (con base del 2003-12-21) o cerca de 1% (con rezago en el corte), y no es lo que sale. Eso describe **la valuación de Finanzas al corte**, no el cálculo de los pagos que haga ONCP según la norma.
c) **La relación con SIGADE** (CLM-M-012): saldo UCP de SIGADE por CER del corte da el VN actualizado de Finanzas por A3500; y saldo UCP por 1,4568 da el VN residual en pesos por el factor de capitalización (diferencias relativas de 2e-9 a 8e-7, tabla `sigade_ucp_vs_finanzas_2026-06-30.csv`). Los saldos UCP de SIGADE reúnen los decretos 1735/04 y 563/10, y para Discount y Cuasipar incluyen el interés capitalizado. El campo `saldo_corte` de `terminos.csv` de esos tres instrumentos son esos saldos UCP.
d) **Factores de capitalización** (CLM-M-008 a CLM-M-011): Discount 1,2699367 (3,04% semestral de 2004 a 2008 y 1,77% de 2009 a 2013, sobre 20 períodos; coincide con Finanzas en 1,269935 a 1,269938) y Cuasipar 1,3885928 (3,31%, 20 períodos). Par no capitaliza (el VN residual es igual al original hasta la amortización).
e) Pregunta abierta para tu motor: el prospecto aplica el CER sobre capital con capitalización en las fechas de pago; yo no calculé cupones ni amortizaciones de estos tres instrumentos (fuera del pedido).

## 3. RC 53 y 60/2026 y SIGADE al 2026-09-30 (pedido 3)

**Para Claude:** sigue sin publicación (`tablas/rc53_rc60_2026_publicacion_revision_lote_m.csv`): el informe de la OPC de septiembre de 2026 no existe (404; último listado: agosto), las direcciones de ONCP para colocaciones al 30-09-2026 devuelven 404, y Finanzas no lista un corte al 30-09-2026 (CLM-M-015 y CLM-M-016). La RC 53/2026 figura en el monitor de la OPC y la RC 60/2026 no. No leí en este lote la RC 54/2026 (BO 347105/20260908, ya anotada en lote L).

## 4. Aclaración sobre una contradicción previa (lote G, CLM-G-051 y CLM-G-052)

**Para Claude:** la diferencia entre la Ley 27.556 (4 de mayo y 4 de noviembre; 4 u 8 cuotas desde 2025) y SIGADE (9 de mayo y 9 de noviembre; 5 y 10 cuotas desde 2024) se explica por el art. 4 del Decreto 676/2020 (CLM-L, lote L), que adecua los Anexos II y III de la ley; coincide con las razones residual/original de Finanzas (0,2 y 0,5). Lo anoto como pista de lectura, no como cierre de esos claims.
