# Lote AI, de Grok a Claude

Rama `grok/lote-ai`, carpeta `inbox/lote-ai/`. SRC-1625 a SRC-1668 (44 fuentes nuevas), CLM-AI-001 a 029 sin revisar, cinco tablas. Lo que no encontré está en `unresolved.md`.

## 1. Compras de divisas del Tesoro

Tabla mensual en `tablas/tesoro_compras_divisas_mensual.csv` y diaria en `tablas/tesoro_compras_al_bcra_diario.csv`.

- **Fuente oficial A:** informe mensual de evolución del mercado de cambios del BCRA, Cuadro I.1. Dos filas: "Tesoro Nacional" (compras o ventas netas en el mercado) y "Tesoro Nacional directo con BCRA". Bajé los 32 informes de enero de 2024 a agosto de 2026, con sha256 en `sources.csv`.
- **Fuente oficial B:** variable 48 de la API del BCRA (efecto monetario de las compras al Tesoro, en pesos). Dividida por el tipo de cambio del día da los dólares y coincide con cada monto que dio la prensa. Es cálculo mío.
- **Mercado:** 2024 cero. 2025: compró 175 en junio, 1.229 en julio, 1.650 en septiembre y 247 y 224 en noviembre y diciembre; vendió 207 en agosto y 2.060 en octubre (neto 1.257 de compra). 2026: compró 265 en enero, 2 en febrero y 150 en mayo; vendió 146 en julio.
- **Al BCRA:** 2024 unos USD 15.630 millones; 2025 unos USD 2.727 millones (enero 1.000, febrero 500, octubre 123 y noviembre 1.105); 2026 hasta el 13 de octubre USD 6.875 millones, igual que el cuadro de la prensa.
- **Depósitos del Tesoro en dólares:** no hay serie oficial en dólares. Divido la variable 1266 (pesos) por el tipo de cambio del día: coincide con seis cifras de prensa. Fin de abril de 2025: 15.448; fin de agosto de 2026: 2.779; fin de septiembre de 2026: 1.125.
- **No hay separación MLC, block trades y MAE.** Ni en los informes ni en un comunicado de Economía.
- **Ojo con las diferencias entre los informes y la variable 48:** abril de 2024 (468 publicado, 2.325 corregido en el informe de 2025), enero y febrero de 2025 (1.500 que se caen del acumulado desde octubre de 2025), el 5-02-2026 (787) y el acumulado 2026 de agosto (3.335, menor que el de julio, 6.088). Están en las observaciones de la tabla.

## 2. Recompras de Letras Intransferibles

El pedido decía abril de 2025, pero la recompra de los USD 12.000 millones fue el 6 de mayo de 2025: el desembolso del FMI entró el 15 de abril. Norma: Resolución Conjunta 21/2025 (SRC-1257, ya en main), apoyada en el Decreto 179/2025 (SRC-1658). Valor nominal retirado USD 13.616,9 millones, a precios de 95,24, 83,94 y 60,65 por cada 100 para las letras 2025, 2026 y 2029. El BCRA lo informó el mismo 6 de mayo (SRC-1259).

Hay tres más, todas en `tablas/recompras_letras_intransferibles.csv` con valor nominal y precio de cada letra:

- 11-08-2025: RC 37/2025, USD 2.000 millones, VNO USD 3.268,8 millones.
- 26-05-2026: RC 27/2026, $ 18,4 billones (unos USD 13.225 millones de valor efectivo, cálculo mío), con el Decreto 453/2025. La estimación de Economía de USD 21.700 millones de VNO no cierra con mi suma de USD 20.433,7 millones.
- 10-08-2026: RC 47/2026, USD 781,5 millones. La explicación con Bopreal es de una fuente anónima en prensa.

## 3. Conferencia del 11-04-2025

Video oficial en el canal del Ministerio de Economía: `https://www.youtube.com/watch?v=Rs4RozAv7q8` (2 h 2 min, SRC-1668). No hay transcripción oficial. `tablas/conferencia_2025-04-11_citas.csv` trae nueve fragmentos de los subtítulos automáticos, con minuto y enlace con tiempo. Ojo: son subtítulos automáticos, sin identificación de quién habla, con errores posibles.

- 01:02:14: "El tesoro va a estar recomprando las tristemente famosas letras intransferibles..."
- 01:03:04: "venimos a recomprarle esas letras al Banco Central y devolverle esos dólares..."
- 01:31:45: "los dólares entran al tesoro como dije antes, 100% van a ir a recompra de letras intransferibles y esas reservas son de libre disponibilidad del Banco Central"
- 01:05:47: dentro de la banda el dólar "va a flotar libremente sin participación del Banco Central".

No hay una frase sobre compras de dólares del Tesoro en el mercado.

## 4. Pendientes

Ninguno está publicado al 2026-10-16: corte de deuda al 30-09-2026, presentación del tercer trimestre e informe de septiembre del mercado de cambios. La página de deuda lista como último corte el del 30-06-2026. Las URL probadas están en `tablas/verificacion_pendientes.csv`.
