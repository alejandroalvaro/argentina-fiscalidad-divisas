# Esquemas

Los esquemas de los lotes de Grok están definidos en [`src/argfx/schemas.py`](../src/argfx/schemas.py). Los archivos `*.schema.json` de esta carpeta se generan desde ahí con `uv run python scripts/export_schemas.py`, de modo que no conviene editarlos a mano.

## Cómo validar

```bash
make validate-grok                     # valida todas las ramas grok/* y deja el informe en data/validacion/
uv run argfx validate <carpeta-inbox>  # valida una carpeta con subcarpetas lote-*/
```

La validación no corrige nada. Cada problema queda registrado con el archivo, la línea, la columna y un código, en dos niveles:

- **error**: rompe el contrato de entrega, y el lote no se incorpora a `main` hasta que se corrija;
- **advertencia**: está permitido, pero alguien tiene que mirarlo.

## Archivos por lote

| Archivo | Esquema | Obligatorio |
|---|---|---|
| `sources.csv` | `Source` | Sí |
| `claims.csv` | `Claim` | Sí |
| `documents_manifest.csv` | `ManifestRow` | Sí |
| `unresolved.md` | | Sí |
| `instruments.csv` | `Instrument` | Cuando el lote tiene instrumentos |
| `tablas/series_*.csv` | `SeriesObservation` | Cuando el lote tiene series |
| `tablas/*.csv` (otras) | Sólo se revisan las referencias de `source_id` | No |
| `contratos/terminos.csv` | `TermRow` | Cuando el lote trae términos contractuales |
| `contratos/tasas.csv` | `RateRow` | Junto con `terminos.csv` (puede tener sólo el encabezado) |
| `contratos/amortizaciones.csv` | `AmortizationRow` | Junto con `terminos.csv` (puede tener sólo el encabezado) |
| `contratos/fechas.csv` | `DateRow` | Optativa: fechas de fin de período listadas por la norma |

Los términos contractuales tienen controles propios: el `instrument_id` debe existir en algún `instruments.csv`, `saldo_corte` debe coincidir con su `outstanding_principal`, y el conjunto debe poder armarse como término (fracciones de amortización que suman 1, fechas dentro del calendario de pagos). El significado de cada columna está en `docs/FASE2_MOTOR.md`.

## Reglas principales

- Una celda vacía significa "desconocido" y se lee como nulo, nunca como cero.
- Identificadores: `SRC-0000`, `CLM-X-000`, `INS-X-0000`, únicos entre todos los lotes.
- Fechas en ISO 8601 completo (`AAAA-MM-DD`). Una serie mensual usa el primer día del mes, y una anual el 1 de enero.
- Monedas en ISO 4217 vigente: los pesos son `ARS`. El código de SIGADE (`ARP`) puede conservarse en una columna aparte, como `currency_code_sigade`.
- `indexation` admite `ninguna`, `ninguna informada` (la fuente no la informa, que no equivale a `ninguna`), `CER`, `UVA`, `dólar-linked (pagadero en ARS)`, `TAMAR` y `BADLAR`.
- En `documents_manifest.csv`, la columna `rol` distingue el documento descargado (`original`) de un archivo que produjo Grok (`derivado`). Un archivo derivado puede citar varias fuentes como `SRC-0001;SRC-0002`, sin texto libre.
- Se admiten columnas adicionales. El validador las informa y las conserva.

## Advertencias esperables

ISIN y residencia del tenedor vacíos en `instruments.csv`, porque SIGADE no los informa; series sin unidad, cuando la fuente no publica metadatos. Quedan como advertencia porque reflejan un faltante real de la fuente, no un error de entrega.
