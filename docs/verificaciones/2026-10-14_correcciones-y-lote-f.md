# Verificación de las correcciones (lotes A a E), del lote F y de los aportes

Fecha: 2026-10-14. Verificó: Claude Code. Las descargas quedan en `manifests/downloads.csv` y los objetos en `manifests/objects.csv`.

## Validación de esquemas

`make validate-grok` sobre las seis ramas `grok/*`: 26 archivos, 19.709 filas, 0 errores y 2.235 advertencias. Las advertencias son las esperables: faltantes reales de SIGADE (ISIN, residencia, indexación no informada), columnas adicionales y las 23 filas de `mapeo_indexador_dpf.csv` sin regla documentada.

## Descargas nuevas

| Lote | Fuentes nuevas | En R2 | Hash igual al de Grok | Observaciones |
|---|---|---|---|---|
| A | SRC-0212 a 0225 (14) | 14 | 12 | SRC-0213 (prensa) y SRC-0220 (Boletín Oficial) son páginas HTML que cambian en cada consulta. SRC-0224 (WIDER) rechaza el User-Agent del proyecto y se bajó con uno de navegador; el hash coincide. |
| D | SRC-0314, 0315 | 2 | 2 | |
| E | SRC-0424 | 1 | 1 | Copia de Grok en `documentos/`. La de planalto.gov.br difiere sólo en un token del balanceador F5 incrustado en un `<script>`; el texto del decreto es idéntico byte a byte. |
| F | SRC-0501 a 0514 (13) | 12 | 4 | Ver abajo. |

Lote F, en detalle:

- SRC-0501 a 0503 (Anexos del Decreto 423/2026): el Boletín Oficial los entrega por POST como JSON con el PDF en base64. Decodificados, los tres coinciden con el hash de Grok.
- SRC-0507 coincide.
- SRC-0504, 0511, 0513 y 0514 son páginas HTML dinámicas; los hashes difieren y las citas aparecen en nuestras copias.
- SRC-0505, 0506, 0509 y 0510 (planalto.gov.br) difieren por el mismo token F5 del SRC-0424. Se guardaron nuestras copias.
- **SRC-0508 queda sin verificar.** La `url` es sólo el dominio `https://www.bcb.gov.br`, y lo que se descarga ahí es la portada, no el cuadro comparativo de 2005. CLM-F-011 depende de ese documento.

## Contenido

**Lote C.** Entre `b81dff9` y la versión actual, `instruments.csv` cambió sólo en `currency_of_payment` (`ARP` a `ARS`, 90 filas). Las cinco tablas SIGADE no cambiaron y siguen idénticas a la base original.

**Lote D.** `series_lote_d.csv` se comparó valor por valor con los archivos estáticos de R2: 12 series, 2.568 observaciones, 0 diferencias y 0 vacíos. Las dos series nuevas (SRC-0314, 10 valores; SRC-0315, 42 valores) también coinciden. CLM-D-009 se recalculó con el mismo resultado: 127 meses, mediana -2,69%, extremos -39,5% y +72,9%. Queda un detalle menor: el archivo estático del IMIG mensual (SRC-0306) trae 2026-08, que la tabla no incluye porque conserva el rango de fechas anterior.

**Lote E.**

- Las 9.470 filas de `series_lote_e.csv` tienen los mismos valores que antes; sólo cambió el formato de fecha.
- Contra los archivos originales, las 19 series SGS y las 2 del WEO coinciden en todas las fechas.
- Las unidades nuevas coinciden con el catálogo CKAN del BCB en las 14 series que respondieron a la consulta. El catálogo indica "Milhões de reais" para la deuda externa (SGS 28192 a 28202) y la tabla lo respeta.
- `dpf_por_indexador_derivado.csv` se recalculó desde `estoquedpf.csv` (SRC-0422) aplicando `mapeo_indexador_dpf.csv` con el prefijo alfabético del título. Hasta 2022-12 coinciden las 642 celdas. Desde 2023-01 aparece una diferencia que crece hasta varios miles de millones de reales y corresponde a **NTN-B1** (Tesouro RendA+ y Educa+). En la tabla derivada, ese título está en `sin_clasificar`, pero la fila no figura en el mapeo, de modo que la tabla no se puede reconstruir a partir de él.

**Lote F.**

- `alicuotas_de_vigentes_2026-10-14.csv` se cotejó con el texto de los tres anexos. Los 21 renglones del Anexo I, los 22 del Anexo II (alícuota 2026 y los 24 meses de 2027 y 2028) y los 2 del Anexo III coinciden.
- CLM-F-002 cita el art. 2 del Decreto 423/2026, cuyo texto está en SRC-0006, pero `source_id` dice SRC-0502 (el Anexo II).

**Citas.** Se buscó el `exact_evidence` de cada afirmación de los seis lotes en el texto del documento citado. Las afirmaciones nuevas de los lotes A y F aparecen en su fuente, con dos salvedades de forma: CLM-A-017 (las notas al margen del Statutes at Large se intercalan con el texto) y CLM-A-024 (ligaduras tipográficas). Las afirmaciones de cálculo de los lotes D y E no son citas textuales y se verificaron sobre los datos.

## Aportes propuestos (`docs/APORTES_PROPUESTOS.md`)

El documento cumple D-003: separa lo que existe en la literatura de lo que propone el proyecto, no agrega nada a `claims.csv` y deja todo como propuesta. Hay dos puntos a tener en cuenta:

- Cita CLM-E y CLM-F, de modo que conviene incorporarlo junto con los lotes E y F.
- Registra como decisiones de Alejandro los tres regímenes del modelo, la fracción en divisas igual a las alícuotas vigentes y la atribución del aporte 1 a Mosler. Esas decisiones no están en `docs/DECISIONES.md` y se anotan ahí cuando Alejandro las confirme.

## Resultado

| Rama | Estado |
|---|---|
| `grok/lotes-b-c` | Se incorpora a `main` |
| `grok/lote-a` | Se incorpora a `main` |
| `grok/lote-d` | Se incorpora a `main` |
| `grok/lote-e` | Espera la fila NTN-B1 en el mapeo |
| `grok/lote-f-regimenes` | Espera CLM-F-002 y SRC-0508 |
| `grok/aportes` | Se incorpora junto con los lotes E y F |

## Segunda ronda (2026-10-14, noche)

`make validate-grok`: 26 archivos, 19.712 filas, 3 errores, todos en el lote E por la misma causa (SRC-0426 citado pero ausente de `sources.csv`).

- **`grok/lote-d-2026-08`.** La fila nueva (IMIG, 2026-08, 960.155,5 millones de ARS) coincide con el archivo estático. CLM-D-009 se recalculó: 128 meses, mediana -2,71%, extremos -39,5% y +72,9%, y 2026-08 en -5,45%. El hash de la tabla coincide con el manifiesto. **Se incorpora.**
- **`grok/lote-f-regimenes`.** CLM-F-002 cita ahora SRC-0006. SRC-0508 tiene la URL directa del PDF, el hash coincide con el de Grok y la cita de CLM-F-011 está en la p. 1. El PDF quedó en R2. **Se incorpora.**
- **`grok/lote-e`.**
  - Con la fila NTN-B1 en el mapeo y la regla de prefijo documentada en `unresolved.md`, `dpf_por_indexador_derivado.csv` se reconstruye exactamente: 642 de 642 celdas, en stock y en participación.
  - La clasificación de NTN-B1 en `ipca_precos` se apoya en el Decreto 12.814/2026, art. 8, inc. V. La copia de Grok es idéntica a la de planalto.gov.br salvo el token F5, y quedó en R2.
  - Falta registrar SRC-0426 en `sources.csv` y su fila `original` en `documents_manifest.csv`. **Espera esa corrección.**
- **`grok/aportes`.** Se incorpora junto con el lote E.
