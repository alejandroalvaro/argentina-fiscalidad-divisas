# Lote D: síntesis breve (series externas)

Fuentes: API del BCRA, API de Series de Tiempo (datos.gob.ar, con datos de BCRA, INDEC y Secretaría de Hacienda) e informe del FMI de mayo de 2026. Las series de datos.gob.ar se toman de los archivos estáticos de cada distribución. Acceso el 14/10/2026. Los datos están en `tablas/series_lote_d.csv` (formato largo, 8.344 observaciones) y `tablas/definiciones_reservas.csv`.

**Reservas.** El BCRA publica reservas brutas diarias desde 2003 (último dato: 08/10/2026) y mensuales desde 1940. El balance de pagos de INDEC registra la transacción de activos de reserva, que es un flujo. El programa con el FMI define reservas netas como brutas menos pasivos de corto plazo, swaps, encajes en divisas y otros conceptos, y no descuenta los depósitos en divisas del Tesoro en el BCRA. Hay cinco definiciones en uso y ninguna serie oficial de reservas netas.

**Exportaciones y derechos.** Las exportaciones FOB del balance de pagos (devengado) y los cobros del balance cambiario (caja) miden cosas distintas. Las dos series oficiales de derechos de exportación difieren entre sí (mediana -2,7% en 127 meses).

**Pagos de renta.** La serie de intereses pagados del balance de pagos en MBP5 termina en 2016 y la MBP6 empieza en 2006, lo que implica una ruptura metodológica.

**Tesoro en el BCRA.** La única serie localizada agrupa depósitos del Gobierno Nacional y otros, en pesos, hasta octubre de 2025.

Las contradicciones entre fuentes están listadas en unresolved.md sin resolver.
