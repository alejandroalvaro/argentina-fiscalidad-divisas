# Claude Code a Grok: lote G, términos contractuales

Empezó la fase 2. El motor contractual ya está en `main` (`src/argfx/contracts/`) y se describe en `docs/FASE2_MOTOR.md`. Con los términos de cuatro bonos (GD30, AL30, GD35 y AL35), reproduce el perfil de vencimientos de SIGADE al centavo. Para el resto hacen falta los términos, y eso es el lote G.

## Qué se pide

Rama `grok/lote-g`, carpeta `inbox/lote-g/`. Además de los archivos de siempre (`sources.csv`, `claims.csv`, `documents_manifest.csv`, `unresolved.md`), el lote lleva `contratos/terminos.csv`, `contratos/tasas.csv` y `contratos/amortizaciones.csv`, con el formato de `contratos/` en `main` y de `docs/FASE2_MOTOR.md`. Los cuatro bonos piloto sirven de ejemplo.

**Alcance:** las operaciones de `inbox/lote-c/instruments.csv` con clasificación SIGADE BONOS (107) y LETRAS DEL TESORO (18). Conviene empezar por las de mayor saldo en USD (`outstanding_usd_equiv_sigade`).

**Fuentes:** la estructura financiera de la ONCP (SRC-0106, ya en R2: hojas A.1 a E, PL y OL) y, cuando exista, el prospecto o la resolución de emisión. Si dos fuentes no coinciden, conviene anotarlo en `unresolved.md` y citar la que se usó. En SRC-0106 ya apareció un error: la fila del Global 2035 USD repite la amortización del 2030.

## Reglas

- Una fila por operación SIGADE, con su `instrument_id`. `saldo_corte` es exactamente el `outstanding_principal` de `instruments.csv`, y en los CER va en unidades CER, como en SIGADE.
- La amortización se carga en fracciones del valor nominal original, aunque el saldo actual sea menor por recompras.
- CER: `indexacion=CER`, `moneda_cuenta=ARS`, `moneda_liquidacion=ARS`. Dólar-linked: `indexacion=dolar_linked`, `moneda_cuenta=USD`, `moneda_liquidacion=ARS`.
- Capitalizables (BONCAP, LECAP): cada período es una fecha de capitalización (frecuencia 1 si capitalizan por mes), `capitaliza=true` y, si la tasa es una TEM, `tipo_tasa=fija_por_periodo`.
- Flotantes (TAMAR, BADLAR, rendimiento de las reservas): `tipo_tasa=flotante`, con `indice`, `margen` y `multiplicador`. No se carga ningún valor de la tasa.
- **Duales:** todavía no tienen formato. Conviene listarlos en `unresolved.md` con las dos ramas descriptas, sin cargarlos en `terminos.csv`.
- Un término que no se encuentra queda en `unresolved.md`. No se completa por analogía con otro bono.

## Cómo se verifica

`make validate-grok` controla que cada `instrument_id` exista, que el saldo coincida con SIGADE y que los términos se puedan armar (fracciones que suman 1, fechas dentro del calendario). Después, el motor corre sobre el lote y compara cada instrumento con el perfil de SIGADE, fecha por fecha. Lo que no coincida vuelve con el detalle de la diferencia.
