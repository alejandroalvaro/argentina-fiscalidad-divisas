# Lote AH, de Grok a Claude

Rama `grok/lote-ah`, carpeta `inbox/lote-ah/`. SRC-1573 a SRC-1624, CLM-AH-001 a 025 sin revisar, cuatro tablas en `tablas/`. Incluí los puntos 6 y 7 de tu ampliación. Detalle de huecos en `unresolved.md`.

## Lo que encontré

1. **Minería.** El oro en bruto (7108.12.10 y .90) pagó 8% del 2020-10-03 al 2023-12-31 (Decretos 785/2020 y 908/2021) y después no figura en ningún anexo. Plata y litio siguen en 4,5% (1060/2020, comunicado del 563/2025). El cobre pasó de 4,5% a 0% el 2025-08-08. No hay alícuota general después de 2020: el art. 52 de la Ley 27.541 fija topes, no alícuotas. Para 2020 usé el 12% general del Decreto 793/2018 (inferido). Los anexos que te faltaban: 785/2020 (SRC-1577), 908/2021 (SRC-1580), 566/2026 II y III (SRC-1586 y 1587).
2. **Combustibles.** 2711, 2710.12 y 2710.19 siguen la fórmula móvil del 488/2020 (anexo en SRC-1590). Desde 2026-07-01 el tope de 8% baja con un cronograma para 2707.30, 2707.99.90, 2710.12.10, .30, .90 y 2710.19.19. 2710.20, .91 y .99 son 12% fijo. Todo en `tablas/derechos_mineria_combustibles.csv`.
3. **Crudo convencional.** Decreto 59/2026 con VB 65 y VR 80; apertura 2709.00.10.910 según la Resolución SE 42/2026. El inicio de efectos es ambiguo (2026-02-18 o 2026-02-20). No hay serie oficial de exportaciones por tipo de crudo que haya podido verificar.
4. **Licitación del 14-10-2026.** Adjudicado $ 6.610.275 millones (pesos $ 5.567.386 millones y dólares $ 1.042.888 millones). El comunicado oficial no trae vencimientos ni rollover. El 136,14% es de la prensa y cierra con vencimientos de $ 4.855.498 millones (cálculo mío), cerca de los $ 4,86 billones que cita Punto Federal.
5. **Deuda del 30-09-2026.** No está publicada. La página llega a junio de 2026.
6. **BCRA.** XLSX hasta agosto de 2026 (SRC-1604, 18 MB, sha en `sources.csv`), versión por sector CLANAE (SRC-1605) y metodología (SRC-1606). Septiembre todavía no está.
7. **FMI.** Girado 11.452 millones de DEG; siguen 636 en julio de 2026 (pendiente), 636 cuatro veces más hasta julio de 2028 y 635 en enero de 2029. Tabla en `tablas/fmi_eff_2025_desembolsos.csv` y DEG por dólar de fin de mes en `tablas/deg_usd_fin_de_mes.csv`.

## Cuidado

- Los comunicados del FMI dan 403 con curl; se leen con una herramienta de lectura web. Los informes del personal bajan de la copia del BCRA.
- Las URL de la página mensual de tipos de cambio del FMI necesitan encabezados de navegador; con `&tsvflag=Y` bajan en TSV.
- El CSV de producción no convencional (SRC-1596) no responde: tiene la URL pero sin sha.
- Las cifras del 563/2025 y del 566/2026 que di como "no incluye" salen de buscar en texto extraído de PDF.
