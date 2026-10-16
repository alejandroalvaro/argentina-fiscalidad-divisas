# Lote AG, de Grok a Claude

Rama `grok/lote-ag`, carpeta `inbox/lote-ag/`. SRC-1533 a SRC-1572 (40 fuentes), CLM-AG-001 a 005 sin revisar. No leí ningún PDF: probé cada URL con GET y anoté código, tipo y tamaño; los archivos llevan sha256. No hay manifest (solo encabezado), porque no guardo originales en la rama.

## Funcionan (GET 200)

- 1060/2020: PDF de Infoleg y copia de ARCA (SRC-1533, 1534), aviso del Boletín Oficial con fecha (SRC-1535).
- 38/2025: anexos 1 y 2 en ARCA (SRC-1537, 1538).
- 305/2025: PDF de Infoleg y copia de ARCA (SRC-1541, 1542).
- 563/2025 (SRC-1544) y 697/2024 (SRC-1546): PDF en ARCA.
- 506/2023: PDF en ARCA (SRC-1549); 9/2024 y 557/2024: avisos y textos (SRC-1552 a 1555).
- 557/2023: anexos 1, 9 y 11 en ARCA (SRC-1557 a 1559).
- Servicios: 1201/2018, 99/2019, ARCA, 1034/2020 (SRC-1560 a 1564).
- PI del crudo: XLSX de Energía (SRC-1566). MAGyP: CSV de estimaciones y del trigo (SRC-1569, 1570).

## No funcionan o con reparos

- Anexos del Boletín Oficial: no hay GET de PDF, solo POST. Dejé la URL del aviso con fecha y la copia de ARCA o Infoleg.
- `datosestimaciones.magyp.gob.ar` (SRC-1572): 200 en una prueba y 500 en la última.
- Slug de PI en datos.gob.ar: 502 (no está en sources).

## Hallazgos

- No encontré decreto de 0% para servicios desde 2022. El 5% (Decreto 99/2019, art. 24) venció el 2021-12-31; es inferencia. El `norma-351268` que había anotado es la RG 5013/2021 de ARCA, no un decreto (SRC-1565).
- El 557/2024 solo prorroga la suspensión láctea; carne y lácteos están en el 697/2024. 9/2024 y 557/2024 no tienen anexo propio y remiten al del 506/2023.
- No hay resolución de la SE para el PI: el XLSX modificado el 2026-09-30 es lo vigente.

Detalle en `inbox/lote-ag/unresolved.md` y `sintesis.md`.
