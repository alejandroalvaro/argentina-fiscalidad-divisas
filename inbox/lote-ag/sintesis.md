# Lote AG: URLs directas de anexos y datasets para fetch-sources

40 fuentes (SRC-1533 a SRC-1572), 5 claims (CLM-AG-001 a 005). No leí los PDFs: cada URL se probó con GET (código, tipo y tamaño en `license_notes`) y, en archivos, se calculó el sha256.

## Qué funciona

- **1060/2020**: PDF de Infoleg `dec1060.pdf` (1.652.912 bytes) y copia en ARCA. Aviso del Boletín Oficial con fecha en la URL; PDF del texto del aviso (199.634 bytes).
- **38/2025**: anexos 1 y 2 en la biblioteca de ARCA (`anexo_7291708_1.pdf` y `_2.pdf`).
- **305/2025**: PDF de Infoleg `dec305.pdf` (436.073 bytes) y copia en ARCA.
- **563/2025**: `anexo_7433505_1.pdf` en ARCA (952.681 bytes).
- **697/2024**: `anexo_7173791_1dec697.pdf` en ARCA (188.970 bytes).
- **506/2023**: `anexo_506_23.pdf` en ARCA (123.801 bytes) y el texto original con el anexo en HTML.
- **9/2024 y 557/2024**: sin anexo propio (remiten al 506/2023). Páginas del Boletín Oficial y de Presidencia con 200.
- **Servicios**: Decretos 99/2019, 1201/2018 y 1034/2020 con 200; **no hay decreto de 0% desde 2022** (ver unresolved.md).
- **PI del crudo**: XLSX de la Secretaría de Energía con 200, modificado 2026-09-30.
- **Estimaciones agrícolas**: CSV de MAGyP (15.471.639 bytes, archivo de 2026-03) y serie del trigo, ambos con 200.

## Qué no

- Anexos del Boletín Oficial por GET como PDF: no existen (solo POST).
- `datosestimaciones.magyp.gob.ar`: 500 en la última prueba.
- `datos.gob.ar/dataset/energia-precio-internacional-pi-petroleo-crudo`: 502.
