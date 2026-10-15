# Lote G2: BONCAP TAMAR (INS-C-0367 a 0371), pendientes

Todo en `sin_revisar`. Este lote solo corrige los cinco BONCAP TAMAR; las demás tareas de la nota de Claude Code quedan para otra entrega.

## Cargado
- `contratos/terminos.csv`: cinco filas corregidas, ancladas en la emisión (`primer_periodo` = emisión más un mes, `frecuencia_meses=1`, `periodo_final_corto=true`, `base=30E/360`, `capitaliza=true`). El motor del repositorio las carga sin error (74 instrumentos con términos, 47 que coinciden con SIGADE, igual que antes) y arma los flujos mensuales de capitalización de cada bono, con monto vacío.

## Sin resolver
1. **Monto vacío por construcción.** La TAMAR del plazo completo es un promedio que solo se conoce al vencimiento (CLM-G-040). Sin una trayectoria de TAMAR en el escenario, el interés y el capital al vencimiento quedan sin monto. No se cargó ningún valor de tasa.
2. **Conversión TAMAR a TEM.** Está en la norma (CLM-G-041), pero el motor no la implementa: hoy una tasa flotante se aplica sin la conversión TNA a TEM en 32 días. Cambio de código del lado de Claude Code. `margen` se carga en puntos de TNA, sumado a la TAMAR dentro de la fórmula.
3. **Margen.** Se tomó del nombre de SRC-0106 (6,5%; 6,0%; 6,5%; 6,9%; 5,4%). Las resoluciones dicen que se fija en la licitación y no traen el valor; el resultado oficial de cada licitación (Secretaría de Finanzas) no se descargó. Una cifra de 5,40% para INS-C-0367 aparece en una publicación de LinkedIn que no se usó como fuente.
4. **Reaperturas.** INS-C-0369 (RC 23/2026 art. 9) e INS-C-0370 (RC 13/2026 art. 9, no descargada) tienen ampliaciones. La fecha de emisión que rige es la original, y el coeficiente de SRC-0103 es uno solo por bono; no se verificó que cada ampliación mantenga ese cómputo.
5. **TAMAR implícita al corte** (`tablas/tamar_tem_implicita.csv`): es derivada del coeficiente publicado con seis decimales; no tiene fuente oficial propia.
6. **Fuera de esta entrega** (siguen abiertos según la nota de Claude Code): BONAR USD 6% con `fechas.csv` y Par con `periodo_final_corto`; base 30/360 en norma de INS-C-0386, 0387, 0413, 0425, 0426 y 0427; resoluciones de los duales; BONAR Dual 2036 y Anexo de la Res. 66/2018.
