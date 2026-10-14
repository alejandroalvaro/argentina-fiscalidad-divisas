# Lote D: cuestiones abiertas, rupturas y contradicciones

Fecha de acceso: 2026-10-14. Todas las afirmaciones están marcadas sin_revisar. Los valores vacíos de `tablas/series_lote_d.csv` vienen vacíos en origen y no se rellenaron con cero. En esa tabla, las observaciones diarias del BCRA llevan SRC-0301 aunque las de la segunda página provienen de SRC-0313.

## Rupturas metodológicas

1. **Balanza de pagos MBP5 y MBP6.** La serie de intereses pagados (SRC-0311) es MBP5 y cubre 1994 a 2016. Las series MBP6 (SRC-0303, SRC-0308, SRC-0310) empiezan en 2006. No deben empalmarse sin una tabla de correspondencia.
2. **Derechos de exportación con dos fuentes.** IMIG (SRC-0306, desde 2016, con 44 meses vacíos) y Recursos tributarios base 2001 (SRC-0307, desde 1997). Difieren mes a mes (ver contradicciones). No se documentó si la diferencia responde a base caja frente a base de recaudación, a coparticipación o a devoluciones.
3. **Reservas: saldo frente a flujo.** El BCRA publica saldos brutos (SRC-0301, SRC-0302). INDEC publica la transacción de activos de reserva en la cuenta financiera (SRC-0303), que es un flujo. No son comparables sin conciliar efectos de valuación.

## Contradicciones (no resueltas)

- **Saldo mensual de reservas frente al último dato diario de la API.** Hay diferencias en 6 de 280 meses: 2007-12 (+10), 2014-12 (+36), 2016-12 (-536), 2024-12 (-28), 2025-12 (+72) y 2026-03 (+1.329 millones de USD). Las de fin de año podrían deberse a la fecha de cierre, pero no se verificó.
- **Derechos de exportación, IMIG frente a Recursos tributarios.** Mediana -3,4%, extremos -39% y +73% en la superposición de 83 meses.
- **Descripción de la serie 144.2_PCIONFMI_0_T_20.** El texto dice "Anual" y la frecuencia es trimestral.

## Reservas: definiciones (ver `tablas/definiciones_reservas.csv`)

- Brutas BCRA (diaria y mensual), activos de reserva MBP6 (flujo), y brutas y netas según el TMU del FMI.
- Según el TMU, los depósitos en divisas del Tesoro en el BCRA no se restan para calcular las reservas netas del programa. Otras definiciones de "reservas netas" (de analistas privados o del propio BCRA) no fueron relevadas y pueden diferir en ese punto.

## Brechas y bloqueos

- **FMI:** la URL oficial del Country Report 26/105 devolvió HTTP 403, también con encabezados de navegador. Se usó una copia secundaria (SRC-0312). Claude Code debe reemplazarla por la oficial. El PDF secundario no se sube a `documentos/` porque la fuente oficial existe y el bloqueo probablemente es del entorno.
- **Sin serie de reservas netas** publicada por el BCRA.
- **Depósitos del Tesoro en el BCRA:** la serie de datos.gob.ar termina en 2025-10 y mezcla moneda nacional y extranjera ("Gobierno Nacional y otros", en miles de ARS). No se encontró serie separada de depósitos en USD del Tesoro.
- **Series vacías:** IMIG intereses netos anual (452.2_INTERESES_TOS_0_T_15_45) y pasivos del gobierno general de la PII (144.4_PVOSGOLES_0_T_32) devolvieron archivos sin datos. No se incluyeron.
- **Amortizaciones pagadas y deuda por moneda y acreedor:** se remite al Lote C (SRC-0103, perfil de vencimientos y cuadros A.1.4). No se descargó una serie histórica de pagos efectivos.
- **No se descargaron** las series de balanza de pagos y deuda externa directamente de INDEC (indec.gob.ar). Se usó la redistribución oficial de datos.gob.ar, que cita a INDEC como fuente.
