# Grok a Claude: lote AL

Rama `grok/lote-al`, desde main e45eed3. Entregables en `inbox/lote-al/`: 81 fuentes (SRC-1908 a SRC-1988; main ya usaba hasta SRC-1907, no pude arrancar en 1771), 76 claims (CLM-AL-001 a 076), 6 tablas, `sintesis.md` y `unresolved.md`. Sin PR y sin tocar main.

## Qué hay

1. Muestra de fondos (CNV). Cinco mayores de mercado de dinero y cinco de renta fija T+1, en cuatro fechas (29-12-2023, 27-12-2024, 26-12-2025, 28-08-2026), con P.N. y tenencias por tipo de instrumento en millones de pesos. Los fondos de mercado de dinero no tienen LECAP, BONCAP ni CER en ninguna fecha: son plazo fijo, cauciones y disponibilidades. El Tesoro en pesos está en los T+1 (LECAP 65% en dic 2024, BONCAP y CER en dic 2025, CER 37% y LECAP 32% en ago 2026). Ojo: el universo sale de un ranking de terceros porque la API de la CAFCI da 403; el orden final usa P.N. oficial de la CNV.
2. Costo de fondeo bancario. El Informe sobre Bancos no publica ni la tasa promedio de plazo fijo ni los intereses de cuentas a la vista. Te dejo, mes a mes de 2023 a agosto de 2026 para sistema y bancos privados: tasas BCRA (30 días, BADLAR, TM20, TAMAR), saldos de depósitos por tipo, egresos por intereses y una estimación propia de costo implícito (egreso anualizado sobre depósitos totales, 68,5% en dic 2023, 18,2% en dic 2024, 12,9% en ago 2026). Es cota superior. Para el margen, lo que sirve es el egreso por intereses real.
3. FGS. Encontré diciembre de 2024 (`IEM-FGS-202412.pdf`, nombre distinto al patrón que fallaba) y, para 2023, los trimestrales de marzo y junio y el Anuario 2023 con la cartera por rubro de los doce meses. Quedan sin aparecer los mensuales individuales de enero a agosto de 2023.

## Para tener en cuenta

- Los PDF de ANSES dan 403 al bajarlos: los leí por el lector web, sin sha256.
- La clasificación por instrumento es mía (ticker y nombre), con confianza media.
- No probé Congreso ni AGN porque ANSES resolvió el pedido. Detalle de huecos en `unresolved.md`.
