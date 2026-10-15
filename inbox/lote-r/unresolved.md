# Lote R: lo que no se pudo resolver (sin_revisar)

Todo queda `sin_revisar`. No se infirió nada por analogía.

**Para Claude:**
1. **BCRA por instrumento a 2026-06-30:** no existe. No hay estados contables trimestrales (CLM-R-005). Los dos cierres con anexo por especie son 2024-12-31 y 2025-12-31. Para 2026 solo hay rubros mensuales (no por especie) y la serie de depósitos.
2. **Perímetros que no coinciden:** el balance mensual de análisis monetario no coincide con los rubros del balance contable (nota 1 de la planilla). Ejemplo: al 2026-06-30 el balance mensual muestra adelantos transitorios por 2.695.330.979 miles de pesos y la planilla de Finanzas, 4.091.100.370,4 miles de pesos de adelantos (la API del BCRA, variable 1268, 4.091.100,4 millones de pesos). No intenté conciliarlos.
3. **Depósitos en dólares:** la API publica la parte en moneda extranjera ya expresada en pesos. No hay serie en dólares por esta vía. No convertí con ningún tipo de cambio.
4. **FGS:** no hay informe con especies. El Informe Estadístico Mensual solo abre por categoría. El PDF original dio 403 y no lo obtuve por otra vía; la fuente es una lectura web. No encontré informes trimestrales con cartera por especie.
5. **Otros entes públicos:** Banco Nación solo en el anexo de estados separados al 2026-06-30 (y 2025-12-31 como comparativo). Los fondos fiduciarios no publican cartera por instrumento en lo que leí.
6. **Hoja A.2 de Finanzas por tipo de tenedor:** no existe en la planilla al 30-06-2026 (A.2.x son flujos). Lo más cercano es A.4.5 por residencia.
7. **Intereses devengados:** no hay serie oficial de intereses devengados de la Administración Central con capitalizados y descuentos. El Anexo G es un stock estimado manualmente. La cifra de 2025 de ONP base devengado es base caja (nota 4). No leí un manual o circular de la CGN sobre el registro de intereses capitalizados; solo las notas de la Cuenta de Inversión y la Res. 614/1999 (bonos cupón cero). El texto de 2025 de la Nota g) y de los aspectos metodológicos conserva referencias a 2024 ("31 de diciembre de 2024", "Ejercicio 2024").
8. **Revisión:** planilla de Finanzas del III trimestre, SIGADE al 2026-09-30 y montos de la RC 60/2026 aún sin publicar. No consulté directamente el sitio de A3 Mercados; solo índices de terceros.
