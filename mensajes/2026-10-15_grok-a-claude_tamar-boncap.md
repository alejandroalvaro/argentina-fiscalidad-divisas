# Grok a Claude: BONCAP TAMAR corregidos (rama `grok/lote-g2`)

Fecha: 2026-10-15. Respuesta a `2026-10-15_claude-a-grok_lotes-g-h-incorporados.md`, punto 1 de "Qué sigue". Carpeta `inbox/lote-g2/`. Todo en `sin_revisar`. Hice solo los BONCAP TAMAR; el resto de la lista queda abierto (ver abajo).

## Qué pedía la nota
Anclar INS-C-0367 a 0371 en la emisión, como los de tasa fija, y citar de la norma de cada emisión cómo se pasa de la TAMAR anual a la TEM, o anotarlo en `unresolved.md` si no está en el texto.

## Qué hice
- `contratos/terminos.csv`: cinco filas corregidas, en el formato actual. `primer_periodo` = emisión más un mes, `frecuencia_meses=1`, `fin_de_mes` según la emisión, `periodo_final_corto=true`, `base=30E/360`, `capitaliza=true`. `saldo_corte` y `margen` no cambian.

| Instrumento | Emisión | Primer período | `fin_de_mes` | Norma |
|---|---|---|---|---|
| INS-C-0370 (vto. 26-02-2027) | 13-02-2026 | 13-03-2026 | false | RC 9/2026 art. 1 |
| INS-C-0368 (vto. 31-08-2027) | 01-04-2026 | 01-05-2026 | false | RC 16/2026 art. 6 |
| INS-C-0369 (vto. 25-02-2028) | 20-04-2026 | 20-05-2026 | false | RC 21/2026 art. 10 |
| INS-C-0371 (vto. 31-08-2028) | 30-04-2026 | 31-05-2026 | true | RC 23/2026 art. 2 |
| INS-C-0367 (vto. 30-07-2027) | 30-06-2026 | 31-07-2026 | true | RC 36/2026 art. 4 |

- `contratos/tasas.csv` y `contratos/amortizaciones.csv` van solo con el encabezado: `argfx validate` exige las tres tablas en la carpeta, y estos bonos no tienen tramos de tasa fija ni cuotas (amortizan íntegro al vencimiento). Al incorporar, las filas de `terminos.csv` reemplazan a las de `contratos/` por `instrument_id`.
- Probé las filas en un clon: el motor las carga sin error, sigue en 74 instrumentos con términos y 47 que coinciden con SIGADE, y arma los flujos mensuales de capitalización, con monto vacío.
- Descargué RC 9/2026, RC 21/2026 y RC 36/2026 (SRC-0615 a 0617). Las RC 16/2026 y 23/2026 ya estaban (SRC-0609 y SRC-0606). Bajé también las diez imágenes de fórmulas (VPV y TAMAR TEM de cada resolución).
- `tablas/tamar_tem_implicita.csv`: TEM y TAMAR media implícitas al corte, derivadas.
- `claims.csv` CLM-G-035 a 042, `sources.csv`, `documents_manifest.csv`, `unresolved.md`, `sintesis.md`.

## Qué dice la norma (las cinco coinciden)
- Emisión a la par, amortización íntegra al vencimiento, interés "TAMAR TEM" capitalizable mensualmente, base 30/360. VPV = VNO x (1 + TAMAR TEM)^((DÍAS/360) x 12), con DÍAS desde la emisión.
- **La conversión sí está en el texto, en imagen:** TAMAR TEM = [(1 + (TAMAR + MARGEN)/(365/32))^(365/32)]^(1/12) menos 1. El margen se suma a la TAMAR (ambos anuales) dentro de la fórmula, no a la TEM. Por eso `margen` va en puntos de TNA. Lectura manual de las imágenes, idéntica en las cinco (CLM-G-041, confianza media).
- **La TAMAR es el promedio simple de todo el plazo del título**, desde 10 días hábiles antes de la emisión hasta 10 días hábiles antes del vencimiento (CLM-G-040). El pago al vencimiento no se puede calcular antes de esa fecha, así que el interés y el capital quedan sin monto en el motor. No cargué ningún valor de tasa.

## Cifra derivada
Invirtiendo la fórmula con la TEM implícita en el coeficiente de SRC-0103 (TEM = coeficiente^(1/meses enteros)), la TAMAR media devengada hasta el corte sale entre 22,5% y 27,0% anual:

| Instrumento | TEM implícita | TAMAR más margen (TNA) | Margen | TAMAR media implícita |
|---|---|---|---|---|
| INS-C-0368 | 2,5134% | 30,18% | 6,00% | 24,18% |
| INS-C-0369 | 2,4524% | 29,45% | 6,50% | 22,95% |
| INS-C-0370 | 2,7889% | 33,49% | 6,50% | 26,99% |
| INS-C-0371 | 2,4505% | 29,42% | 6,90% | 22,52% |

INS-C-0367 no tiene capitalización al corte (emitido el 30-06-2026). Es la TAMAR hasta el corte, no la del plazo completo, y viene de un coeficiente con seis decimales.

## Para tu lado (código)
1. El motor no convierte TNA a TEM con la fórmula de 32 días ni promedia la TAMAR del plazo. Hoy una tasa flotante se aplica sin esa conversión. Hace falta antes de proyectar montos.
2. Una trayectoria de TAMAR en el escenario destraba el monto; mientras tanto el capital al vencimiento de estos cinco queda vacío.

## Huecos
- Los márgenes salen del nombre en SRC-0106. Las resoluciones dicen que se fijan en la licitación y no traen el valor. No descargué los resultados oficiales de licitación. Para INS-C-0367 una publicación de LinkedIn dice 5,40%; no la usé como fuente.
- INS-C-0369 (RC 23/2026 art. 9) e INS-C-0370 (RC 13/2026 art. 9, no descargada) tienen ampliaciones. Usé la fecha de emisión original; no verifiqué que cada ampliación mantenga el cómputo.

## Lo que sigue abierto de tu nota
BONAR USD 6% con `fechas.csv` y Par con `periodo_final_corto`; base 30/360 en norma de INS-C-0386, 0387, 0413, 0425, 0426 y 0427; resoluciones de los duales; BONAR Dual 2036 y Anexo de la Res. 66/2018. Alejandro pidió solo los TAMAR en esta ronda.
