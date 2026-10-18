# Series observadas

Datos observados que el motor usa junto con los escenarios. No son términos contractuales ni escenarios: `argfx calendario` los agrega como historia anterior al corte y como calendario de días hábiles.

| Archivo | Contenido | Fuente |
|---|---|---|
| `bcra_a3500.csv` | Tipo de cambio de referencia Com. A 3500, 2017-01-02 a 2026-10-14. Los días con dato son los días hábiles observados del sistema financiero | SRC-1907 (2017 a 2023) y SRC-1900 |
| `bcra_cer.csv` | CER diario, 2024-01-01 a 2026-10-14 | SRC-1901 |
| `bcra_tamar.csv` | TAMAR de bancos privados en TNA, en porcentaje, 2024-10-01 a 2026-10-13 | SRC-1902 |
| `bcra_badlar.csv` | BADLAR de bancos privados en TNA, en porcentaje, 2024-01-02 a 2026-10-14 | SRC-1906 |
| `feriados_decretados.csv` | Días no laborables decretados posteriores a la serie A3500 | SRC-1903 |

Las fuentes están registradas en `inbox/lote-j/sources.csv` y sus originales en R2. Los IDs SRC-1900 en adelante son de Claude Code, separados de la numeración de Grok.

Para actualizar, se baja de nuevo la API del BCRA (`https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/{5,30,44}?desde=&hasta=&limit=3000`), se registra la descarga como fuente nueva y se reescriben los CSV con columnas `fecha,valor,source_id`.

## Presupuesto (revisión del 18-10-2026)

`presupuesto_abierto_devengado.csv`: crédito vigente y devengado de la Administración Nacional por concepto (transferencias a universidades nacionales con tres perímetros, intereses de la deuda por tipo, comisiones, primas, prestaciones de la seguridad social, transferencias corrientes en energía y transporte), 2023 a septiembre de 2026, en millones de pesos corrientes y de septiembre de 2026 (IPC del INDEC, datos.gob.ar 145.3). Sale de los datasets de crédito anual y mensual de Presupuesto Abierto (SRC-9009 a SRC-9012 y los de 2023 y 2024 del mismo repositorio), procesados fuera del paquete; el capítulo 3.5 del informe los pasa a pesos de agosto de 2026. Las columnas en pesos constantes son de septiembre de 2026.
