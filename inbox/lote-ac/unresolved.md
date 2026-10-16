# Sin resolver, lote AC

1. **PDF del Informe Estadístico Mensual de diciembre de 2024: no apareció por ninguna vía.** Se resolvió el dato con el Informe Anual 2024 (SRC-1319), pero el mensual sigue sin leerse. Vías probadas (fecha 2026-10-16):
   - `https://fgs.anses.gob.ar` y `https://www.anses.gob.ar/fondo-de-garantia-de-sustentabilidad`: 403 (Incapsula) desde la box.
   - `https://www.anses.gob.ar/estudiosyestadisticas/informe-estadistico-mensual-fgs-diciembre-2024` y `...-enero-2025`: el lector web devuelve "Request unsuccessful, Incapsula incident". La búsqueda web indexa la página de enero de 2025 pero solo el cascarón, sin el enlace al PDF.
   - `https://www.anses.gob.ar/sites/default/files/inline-files/Anuario_2024.pdf` y `Anuario%202024.pdf`, `archivo/2026-03/Anuario-2025.pdf`: 403 con curl; el de `Anuario%202024.pdf` sí se pudo leer con el lector web (es la fuente SRC-1319).
   - Wayback Machine: `web.archive.org/web/2025/ y /web/2026/...informe-estadistico-mensual-fgs-diciembre-2024` y `...enero-2025`: 404. `.../archivo/2025-01` a `2025-04/IEM_FGS_202412.pdf`, `IEM_FGS_2024_12.pdf`, `IEM_FGS_Diciembre_2024.pdf`: 404. El índice CDX de Wayback respondió "Temporarily Offline" en varias consultas; con filtro `IEM_FGS` solo apareció `archivo/2026-08/IEM_FGS_202607.pdf` (200). `.../Anuario%202024.pdf` y `Anuario-2025.pdf` en Wayback: 404.
   - `archive.org/wayback/available`: 429.
   - `argentina.gob.ar/anses/fgs`: 404. Tesorería (`argentina.gob.ar/economia/tesoreria-general-de-la-nacion/informacion-estadistica-mensual-2024`) lista otras series, no el FGS. No probé `datos.gob.ar`; la búsqueda no devolvió ningún conjunto del FGS.
   - Prensa que cita el informe (Clarín, Cronista, Debursa, Agencia Hoy): da totales y porcentajes del FGS, sin la tabla por categoría en millones de pesos.
2. **Clasificación de las LELINK:** sin nota en el Informe Anual 2024 ni en los mensuales del lote AB. Sigue pendiente la consulta a la Subdirección Ejecutiva de Operación del FGS o una nota metodológica.
3. **Garantizados y Cuasipar dentro de la fila CER de diciembre de 2024:** inferido por suma (CLM-AC-005), no confirmado por el informe. Se confirmaría con el mensual de diciembre de 2024 o con el de enero de 2025, que podría traer el cierre del año anterior en otro formato.
4. **Diferencia de totales:** el Informe Anual da total del FGS 76.904.936 (redondeado); los medios citan 72.639.417,8 para diciembre de 2024, que es en realidad el cierre de noviembre (Anexo I del anual). No es un error del anual.
