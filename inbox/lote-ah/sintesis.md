# Lote AH: minería, combustibles, licitación, deuda, balance cambiario y FMI

52 fuentes (SRC-1573 a SRC-1624), 25 claims (CLM-AH-001 a 025) y cuatro tablas en `tablas/`. Probé cada URL con GET y anoté código, tipo y tamaño; los archivos llevan sha256. Los PDF de anexos sí los leí con extracción de texto, para responder lo que pidió Claude.

## 1. Oro, plata y minería

- **Oro en bruto (7108.12.10 y .90):** 8% del 2020-10-03 al 2023-12-31 (Decreto 785/2020, prorrogado por el 908/2021). Desde 2024 no figura en ningún anexo; la prensa dice que quedó sin retención. Antes de octubre de 2020, 12% por regla general (inferido).
- **Oro en polvo (7108.11):** 12% desde 2021 y 0% desde 2025-08-08 (563/2025). **Semilabrado y monetario (7108.13, 7108.20):** 12%, sin cambios hallados.
- **Plata (7106) y litio (2836.91.00):** 4,5% desde 2021-01-01 (1060/2020); el 563/2025 y el 566/2026 no las tocan.
- **Cobre (2603):** 4,5% desde 2021, 0% desde 2025-08-08 (563/2025).
- **No hay alícuota general después de 2020.** La Ley 27.541 art. 52 solo fija topes. El Decreto 793/2018 puso 12% a todo hasta el 2020-12-31.

## 2. Gas y combustibles

2711 sigue la fórmula móvil del Decreto 488/2020 desde 2020-05-19. 2710.12 y 2710.19 también, y desde 2026-07-01 el 8% de la fórmula se reemplaza por un cronograma que baja a 0% el 2027-06-01 para seis posiciones (Decreto 566/2026, Anexo III). 2710.20, 2710.91 y 2710.99 tienen 12% fijo.

## 3. Crudo convencional

Decreto 59/2026: VB 65 y VR 80 para 2709.00.10. La apertura SIM 2709.00.10.910 la informa la Resolución SE 42/2026 (fechada 2026-02-18, publicada 2026-02-20). No hay serie oficial de exportaciones separada por tipo de recurso que yo haya podido verificar.

## 4. Licitación del 14-10-2026

Ofertas $ 9,49 billones; adjudicado $ 6,61 billones (pesos $ 5,57 billones; dólares $ 1,04 billones). El comunicado oficial **no informa vencimientos ni rollover**. El 136,14% es de la prensa y es coherente con vencimientos de unos $ 4,86 billones (cálculo propio: 4.855.498 millones).

## 5. Corte del 30-09-2026 de la deuda

No está publicado al 2026-10-16. Último corte: 30-06-2026.

## 6. Balance cambiario del BCRA

XLSX oficial hasta agosto de 2026 (septiembre no está). Incluye hoja de balance cambiario, concepto y sector, con Personas Humanas en la hoja larga.

## 7. FMI, EFF 2025

Girado: 9.160 + 1.529 + 763 = 11.452 millones de DEG (ingresos a reservas el 2025-04-15, 2025-08-04 y 2026-05-26 según la prensa). Siguen 636 (2026-07-31, pendiente), 636 (2027-01-31), 636 (2027-07-31), 636 (2028-01-31), 636 (2028-07-31) y 635 (2029-01-31). DEG por dólar de fin de mes en `tablas/deg_usd_fin_de_mes.csv`; al 2026-09-30, USD 1,359750 por DEG.
