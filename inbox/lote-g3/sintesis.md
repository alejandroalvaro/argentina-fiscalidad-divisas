# Lote G3: BONAR USD 6%, Par, bases de cálculo, márgenes TAMAR oficiales y duales (sin_revisar)

## Qué hay
- `contratos/terminos.csv`: 18 filas (7 nuevas y 11 con referencias o notas actualizadas).
  - Nuevas: INS-C-0358 (Consenso Fiscal, con el anexo de la Res. 66/2018), INS-C-0359 y INS-C-0360 (BONAR USD 6%, con `fechas.csv`), INS-C-0448 a 0451 (Par, con `periodo_final_corto=true`).
  - Actualizadas: INS-C-0386, 0387, 0413, 0425, 0426 y 0427 (base de cálculo) e INS-C-0367 a 0371 (margen del resultado oficial de la licitación). Los valores de los cinco TAMAR no cambian.
- `contratos/fechas.csv` (51 fechas: 20 de INS-C-0359 y 31 de INS-C-0360), `contratos/tasas.csv` (25 filas) y `contratos/amortizaciones.csv` (280 filas: 125 de INS-C-0358, 80 de los Par y 75 de las seis filas de base, repetidas sin cambios para que el lote valide solo).
- `sources.csv` (SRC-0618 a 0625, 0627 y 0628), `claims.csv` (CLM-G-043 a 054 y 058 a 060), `documents_manifest.csv`, `tablas/` (márgenes oficiales y estado de la base de los seis instrumentos).

## Hallazgos
- **Márgenes TAMAR.** Los cinco resultados oficiales de la Secretaría de Finanzas dan 6,50% (TMF27), 6,00% (TMG27), 6,50% (TMF28), 6,90% (TMG28) y 5,40% (TML27). Coinciden con los del nombre. La reapertura del TMF28 del 28-04-2026 se hizo por precio ($ 1.007,00), sin margen nuevo.
- **BONAR USD 6%.** Las 51 fechas de la norma coinciden con las del perfil SIGADE y el interés mensual coincide en todos los pagos salvo uno: el del 31-03-2028 de INS-C-0360 (SIGADE cuenta 30 días desde el 29-02-2028, la base 30/360 del motor cuenta 32).
- **Par.** Las cuatro filas reproducen el perfil SIGADE (26 pagos cada una, interés y capital) con `periodo_final_corto=true`, incluido el último período corto del 30-09-2038 al 31-12-2038.
- **Consenso Fiscal (INS-C-0358).** El anexo de la Res. 66/2018 se obtuvo de la edición web del Boletín Oficial (125 porcentajes que suman 100%). Las 30 cuotas posteriores al corte equivalen al perfil SIGADE con un valor nominal base constante de 36.523.285.518 (derivado).
- **Base de cálculo.** Confirmada en norma para INS-C-0386 y 0387 (Ley 27.556, Anexo III) y para INS-C-0413 (RC 18-E/2016). Para INS-C-0425 y 0426 se confirma en el prospecto de 2005 aprobado por la Res. 20/2005, cuyos anexos no se publicaron. Sin confirmar: INS-C-0427 e INS-C-0450 (yenes).
- **Contradicción nueva.** La Ley 27.556 fija fechas de pago del BONCER 2026 y 2028 el 4 de mayo y el 4 de noviembre, con menos cuotas que SRC-0106 y SIGADE (9 de mayo y 9 de noviembre).
- **Duales.** El DNU 164/2023, Anexo III, define las condiciones del BONAR Dual 2036 pero no las fechas. La resolución que las fija no apareció.

## Qué no se hizo
Ver `unresolved.md`.
