# Grok a Claude: lote E listo

- Rama `grok/lote-e`, archivos en `inbox/lote-e/`. Los originales (CSV/JSON/PDF de origen) no van en el commit. Las URLs y sha256 están en sources.csv y documents_manifest.csv.
- IDs de fuente: SRC-0401 a SRC-0423. Claims: CLM-E-001 a 009, todos sin_revisar.
- Tabla: `tablas/series_lote_e.csv` (9.470 filas). Las unidades quedan vacías salvo % PIB, porque los metadatos del SGS no estaban disponibles.
- Ver unresolved.md: dos metodologías de deuda bruta (4537 y 13762) y el WEO alineado con 4537. Las proyecciones del WEO hasta 2031 están mezcladas con los datos observados.

**Para Alejandro:** ¿se quiere clasificar la DPF por indexador (cambial, Selic, IPCA, prefijado) a partir del código de título, o se prefiere esperar al RMD oficial?
