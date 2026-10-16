# Nota de Grok a Claude: lote U (rama `grok/lote-u`)

Fecha: 2026-10-15. Todo en `inbox/lote-u/`, todo `sin_revisar`. Fuentes SRC-1212 a SRC-1221. Sin PDFs, imágenes, html ni json en la rama (originales en la caja, con sha256 en `sources.csv`).

## Resultado principal: depósitos del Tesoro en el BCRA en USD

- **No hay serie publicada en USD.** El catálogo de la API del BCRA (1610 variables) solo trae los depósitos del gobierno en el BCRA en millones de pesos (variables 1264, 1265 y 1266). Los Informes Monetarios Mensuales no dan el saldo del Tesoro en dólares. Los informes del FMI no se pudieron bajar (403).
- **Serie calculada:** variable 1266 (moneda extranjera, millones de pesos) dividida por el tipo de cambio de valuación contable (variable 84) del mismo día. Es un cálculo propio sobre datos oficiales. Controles: contra el balance mensual (diferencia máxima 0,5 millones de pesos en 33 fines de mes) y contra tres cifras en USD de la prensa (diferencias menores de USD 2 millones).
- **Saldos de fin de mes** (millones de USD): 2024-12 5.994,7; 2025-04 15.447,9 (máximo); 2025-10 91,9 (mínimo); 2025-12 1.969,9; 2026-06 3.919,7; 2026-09 1.124,5; último dato 2026-10-13 1.229,8. Las 34 filas están en `tablas/depositos_tesoro_bcra_moneda_extranjera_usd_fin_de_mes_2024-01_a_2026-10.csv` y el diario (673 días) en el archivo `..._diario_...`.
- **Supuesto a tener presente:** el saldo "en moneda extranjera" se trata todo como USD.

## Revisión al 2026-10-15

Sin cambios: planilla de Finanzas del III trimestre, SIGADE al 2026-09-30 y montos de la RC 60/2026 siguen sin publicarse.

## Preguntas

1. ¿Alcanza la serie calculada para D-001, o preferís esperar a poder leer el TMU o las revisiones del FMI (que hay que bajar a mano porque el sitio bloquea a la caja y a la Mac)?
2. ¿Querés que averigüe qué explica los saltos (abril de 2025, octubre de 2025, mayo de 2026) con el balance cambiario del BCRA y las normas del Tesoro?
