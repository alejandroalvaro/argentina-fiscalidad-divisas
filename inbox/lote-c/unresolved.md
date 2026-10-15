# Lote C: cuestiones abiertas y contradicciones

Fecha de acceso: 2026-10-14. Cortes: base SIGADE y planilla trimestral al 30/06/2026; estructura financiera de títulos al 31/08/2026. No se encontró inventario oficial con corte posterior al 30/06/2026.

## Alcance de instruments.csv

- Una fila por operación de la tabla "Saldo de Deuda en Situación de Pago Normal" de SIGADE (753 filas). `outstanding_principal` copia el campo "Saldo en Moneda de Origen", que es un saldo y no una emisión. **Resuelto (verificación de Claude Code, docs/verificaciones/2026-10-14_sigade_lote-c.md):** el saldo de cada operación coincide con la suma del principal futuro de la tabla de vencimientos (diferencia total de 25 USD), por lo que al corte el saldo es capital pendiente.
- Quedan fuera la deuda elegible pendiente de reestructuración (tabla aparte, 1.036 filas de servicios) y la "Deuda a Reestructurar" (110 filas). Ambas están en `data/` sin convertir a instrumentos.
- Cubre la Administración Central. Quedan fuera la deuda del BCRA (por ejemplo, BOPREAL y pasivos remunerados), provincias y empresas públicas.
- `isin` está vacío en todas las filas: ninguna fuente oficial descargada asocia ISIN a las operaciones vigentes. Las ISIN del prospecto de 2020 (SRC-0108) son de bonos elegibles canjeados, y por eso no se asignaron.
- `holder_residency` está vacío. Solo existe el agregado por residencia (cuadro A.4.5).
- `instrument_family` es una clasificación mecánica derivada de los códigos SIGADE (moneda, clasificación, nombre). Requiere revisión.

## Inconsistencias dentro de la base SIGADE (no corregidas)

1. Código de moneda frente a descripción: AED figura como "DOLARES ESTADOUNIDENSES"; KWD figura como "EURO" (con moneda de pago EUR); una fila XDR figura como "DOLARES ESTADOUNIDENSES" con pago USD, y otras dos como "SPECIAL DRAWING RIGHTS".
2. Préstamos garantizados con "T.VARIABLE" en el nombre figuran con tipo de tasa "TASA FIJA". El BONTE DUAL CER/TAMAR figura como "TASA CERO", y los BONCAP TAMAR figuran como "DIVERSAS".
3. **Resuelto (verificación de Claude Code, docs/verificaciones/2026-10-14_sigade_lote-c.md):** el tipo de cambio UCP es igual a ARP / CER (1.483,0198 / 799,2033 = 1,8556). El saldo UCP está en unidades de capital ajustable; multiplicado por el CER al corte da pesos corrientes.
4. **Resuelto (verificación de Claude Code, docs/verificaciones/2026-10-14_sigade_lote-c.md):** el tipo de cambio DLK es 1 y la relación saldo en origen / saldo en dólares es exactamente 1 en las 8 operaciones. El saldo DLK está en USD, pagadero en pesos.

## Diferencias entre cuadros (conciliables, no contradicciones)

- A.1.1 "Deuda en situación de pago normal" = 471.689.788 miles de USD (cuadro), igual a la suma de SIGADE (471.689.788.348 USD; SIGADE está en dólares, no en miles). A.1.4 "excluida la elegible" = 471.795.067; la diferencia (105.278) coincide con la deuda en situación de pago diferido de A.1.2.
- En A.1.4 no queda claro si la deuda dólar-linked se clasifica como "moneda local" o "moneda extranjera". Pendiente.

## Brechas

- **ISIN y CUSIP vigentes.** Fuentes candidatas no descargadas: anexos del 18-K y los 424B posteriores en EDGAR, resoluciones conjuntas de emisión en el Boletín Oficial, Caja de Valores y BYMA. BYMA y MAE no se consultaron (datos de mercado, no del emisor).
- **Prospectos maestros.** No se descargaron el prospecto base de la República en EDGAR ni el indenture de 2016. Las resoluciones de emisión locales (Boletín Oficial) tampoco.
- **Garantías y contingencias.** Los avales y las letras en garantía figuran en SIGADE. No se localizó un inventario oficial de pasivos contingentes (juicios, garantías de PPP o RIGI, fondos fiduciarios).
- **Calendario posterior al corte.** La tabla de vencimientos es una proyección al 30/06/2026. Las licitaciones de julio a octubre de 2026 no están incorporadas.
- **Contenido del 18-K 2025.** Solo se descargó la carátula (44 KB). El anexo D con la descripción de la deuda no se descargó.

## Ajustes de formato posteriores a la validación de Claude Code

- `instruments.csv`: `currency_of_payment` pasa de `ARP` a `ARS` (ISO 4217) en 90 filas. El código SIGADE se conserva en `currency_code_sigade`.
- `documents_manifest.csv`: se agregó la columna `rol`. Las cinco tablas exportadas de SIGADE quedan como `derivado` con `source_id` SRC-0102, y su `local_object_key` apunta a `tablas_sigade/`, que es donde están en la rama.
