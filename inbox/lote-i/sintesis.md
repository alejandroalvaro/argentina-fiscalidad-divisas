# Síntesis del lote I (actualización post corte SIGADE del 30-06-2026)

Todo `sin_revisar`. Corte de información: 15-10-2026. Sin recomendaciones.

## Operaciones (contratos/operaciones.csv, 46 filas; detalle de las 78 en tablas/operaciones_detalle.csv)
- Precio, TEM de corte y TIREA de cada licitación en `tablas/licitaciones.csv`.
- Licitaciones con liquidación el 17-07, 31-07, 14-08, 31-08, 15-09 y 30-09, más la adjudicada el 14-10 (liquida el 16-10, RC no publicada).
- Valor efectivo total adjudicado: 15-07 ARS 5.438.241 millones; 29-07 ARS 12.205.528 millones; 14-10 ARS 6,61 billones (comunicado de Finanzas).
- Emisiones de bonos en dólares: BONAR USD 6% 2029 (AO29) y TMVE8; sus resoluciones conjuntas (RC 44, 46, 48 y siguientes) están en `contratos/` y `tablas/resoluciones_conjuntas_post_corte.csv`.
- Conversiones públicas de LELINK: D31L6 USD 1.851 millones (45,17%), D31G6 USD 1.344 millones (34,12%), D30S6 USD 3.299 millones (75%).
- Recompra de letras intransferibles al BCRA: RC 47, USD 781.466.440,76 (VNO USD 76.248.473 de la letra a 30-06-2031 y USD 1.226.343.706 de la letra a 20-04-2032), liquidada el 10-08-2026. Base: art. 55 Ley 11.672 y art. 2 Decreto 453/2025.
- Canjes con el BCRA por conversión de LECAP S30O6 y otras especies (RC 39, 49, 51, 53, 60): montos efectivos no publicados.
- RC 59: tope de ARS 221.119.509.519.
- Préstamos garantizados (RC 40 y 41; Decretos 478, 549 y 550/2026): topes de USD 2.000 millones y USD 1.200 millones, sin desembolso verificado.

## Stock oficial (tablas/stock_oficial_a1_2026.csv y flujos_oficiales_a4_2026.csv)
- Deuda bruta en USD millones: 474.198,0 (30-06), 484.722,4 (31-07, provisorio), 484.917,0 (31-08, provisorio). En situación de pago normal al 31-08: 482.391,6.
- Hoja A.4: financiamiento, canjes y emisiones USD 20.536,7 millones en julio y 12.607,3 en agosto; amortizaciones, canjes y cancelaciones 14.472,4 y 15.643,7.
- Coinciden con las licitaciones: AO29 USD 1.125,9 millones en julio y 100 en agosto; TMVE8 USD 3.467 millones en julio.
- OPC agosto de 2026: letras intransferibles canceladas por USD 1.303 millones sin nueva emisión.
- No hay SIGADE ni stock oficial al 30-09 publicados.

## Resultado de caja del SPN (tablas/series_spn_base_caja.csv, 96 filas: 3 series por 32 meses, 2024-01 a 2026-08)
- Método: la respuesta de la JGM en el Informe 144 (Pregunta 58) describe el tratamiento de los intereses capitalizados, citada literal en claims.csv. El Boletín Fiscal 2T26 define base caja como movimiento de fondos.
- Se verifica la identidad resultado primario menos intereses igual a resultado financiero, y la coincidencia con el BF2T26 de enero a junio de 2026.
- Sumas (millones de ARS corrientes): 2024 primario 10.405.810, intereses 8.641.024, financiero 1.764.786; 2025 primario 11.769.219, intereses 10.315.400, financiero 1.453.819; enero a agosto 2026 primario 12.277.684, intereses 9.941.064, financiero 2.336.620.
- Estimaciones secundarias de intereses capitalizados no registrados: CEPA enero a mayo 2026 ARS 11,37 billones frente a un superávit informado de 2,48 billones; desde enero 2024 ARS 50,26 billones frente a 5,70 billones; OPC/Cachanosky 2025 ARS 75,8 billones y enero a abril 2026 ARS 17,3 billones; FMI 1,2% del PIB (no verificado en origen). Metodologías no replicadas.

## Validación
`argfx validate` real sobre main más el lote: 1 error (`term_sheet_invalid`, lote aislado, ver unresolved.md punto B) y advertencias de ISIN, residencia, indexación y columnas extra. Fusionado con `contratos/` de main, `load_term_sheets` y el motor corren sin error (82 términos, 1.282 flujos).
