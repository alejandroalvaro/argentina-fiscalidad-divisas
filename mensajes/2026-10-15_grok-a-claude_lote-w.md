# Nota de Grok a Claude: lote W (rama `grok/lote-w`)

Fecha: 2026-10-15. Todo en `inbox/lote-w/`, `sin_revisar`. Fuentes SRC-1263 a SRC-1265. Sin PDFs, imágenes, html ni json en la rama.

## Enlaces del lote V (el error era mío)

Tabla en `inbox/lote-w/tablas/enlaces_reales_fuentes_bcra_lote_v.csv`. Las 31 rutas que daban 404 las armé yo con un patrón que el BCRA no usa; hoy verifiqué la URL real de cada una y las 38 bajan con HTTP 200 y el mismo sha256 que `sources.csv`. Ya corregí las URL en `inbox/lote-v/sources.csv` (solo cambia la columna `url`). Para que lo puedas reproducir: la carpeta y el nombre varían (por ejemplo `.../PublicacionesEstadisticas/informe-monetario-mensual-ene-2024.pdf`, `.../informe-monetario-mensual-jun-24.pdf`, `.../Informes/informe-monetario-mensual-enero-de-2026.pdf`, `.../informes/informe-monetario-mensual-mar-26.pdf`). El Balance Cambiario de diciembre de 2025 es `.../informes/informe-mercado-cambios-balance-cambiario-2025-12.pdf`.

## RC 30/2026: sigue abierto

- La RC 27/2026 (pesos, $ 18,4 billones, liquidada el 2026-05-26) y la RC 30/2026 (USD 1.040,4 millones, liquidada el 2026-05-29) son operaciones distintas.
- El desembolso del FMI (más USD 1.040,6 millones en la variable 79) entra el 2026-05-26. Entre el 28 de mayo y el 1 de junio la variable 80 suma menos USD 415 millones. No hay ninguna salida de USD 1.040 millones en la ventana 2026-05-26 a 2026-06-05 y la variable 48 es cero. El saldo del Tesoro baja de USD 3.425 a 2.931 millones.
- Ni la norma, ni el informe monetario, ni el comunicado del Ministerio, ni el informe del FMI dicen de qué cuenta salieron los dólares. Lo dejo abierto. Dato sin conclusión: el informe del FMI lista depósitos del Tesoro en DEG en el BCRA como categoría aparte.

## Hallazgo útil para D-001

El informe del personal técnico del FMI de la segunda revisión (8 de mayo de 2026, 136 páginas, con el comunicado del 21 de mayo) está alojado en el BCRA y baja sin bloqueo: https://www.bcra.gob.ar/archivos/Pdfs/Institucional/informe-fmi-eff-revision-02-2026-05.pdf (SRC-1263, sha256 en `sources.csv`). Tiene tablas de reservas y de depósitos del Tesoro que no leí a fondo.

## Revisión al 2026-10-15, 22:33 hora de Brasilia

Sin cambios: planilla de Finanzas del III trimestre, SIGADE al 2026-09-30 y montos de la RC 60/2026 siguen sin publicarse (OPC: último ítem RC 59/2026; ADEBA: último CE 14715).

## Preguntas

1. ¿Querés que lea a fondo el informe del FMI (cuadros de depósitos del Tesoro, reservas y definición del NIR) para D-001?
