# Lote H: pendientes y límites

Todos los claims están `sin_revisar`. El lote describe cómo funcionan los fondos y no recomienda reglas. Las reglas del fondo del régimen (d) las decide Alejandro.

## 1. Fuentes no oficiales o no descargadas

- Colombia: el texto de la Ley 2056 de 2020 (SRC-0709) proviene de leyes.co, una compilación privada. Los sitios oficiales (Secretaría del Senado, Función Pública, SUIN, Ministerio de Hacienda, Presidencia) no respondieron desde la caja. Faltan el texto oficial de la ley, el art. 361 de la Constitución y el Decreto 1821 de 2020. Los claims CLM-H-016 a CLM-H-019 quedan en confianza media por esto.
- Noruega: la ley (SRC-0704), el marco fiscal (SRC-0705) y la adhesión a los Principios de Santiago (SRC-0706) se leyeron con WebFetch porque curl devolvió 403 o una verificación de Cloudflare. Los `.txt` son transcripciones con el método indicado en la cabecera y su sha256 corresponde a la transcripción, no al original. Solo se transcribieron las secciones 1, 3, 4 y 7 de la ley.
- Chile: el idNorma del DFL 1/2006 (258298) proviene de una búsqueda web, no de la página descargada. El texto de la Ley 20.128 se descargó de leychile.cl en formato XML y el del DFL 1 en PDF.
- Perú: el texto del DL 1276 viene de la página del Consejo Fiscal y debe contrastarse con El Peruano. No se leyeron el Reglamento (art. 25 citado por el informe del MEF), la Ley 27783 ni el PBI de 2025, de modo que no se calculó el saldo del FEF como porcentaje del PBI.

## 2. Contradicción señalada (no resuelta)

- Los Principios de Santiago (2008, nota 18) dicen que en Chile la acumulación y el retiro se basan en un precio de referencia del cobre. Los textos vigentes leídos (Ley 20.128 y DFL 1/2006, versión 2024) fijan la acumulación por el superávit efectivo, sin precio de referencia del cobre. Puede deberse a un cambio de regla posterior a 2008; no se verificó con la historia de la ley.

## 3. Lo que no se encontró o no se levantó

- Un proyecto de 2025 sobre autorizaciones de retiro del FEES y la división de aportes entre FRP y FEES apareció solo en fuentes secundarias. No se incluye como claim porque no se confirmó como ley.
- Saldo actual del FEES, del FAE y su composición por departamento: no se levantaron.
- Otros comparables: los Principios de Santiago incluyen perfiles de Rusia, Botswana, México y Kuwait, entre otros. El PDF de México (`lote_A/docs/mx_fmp_mecanismos.pdf`) está en el lote A y no se procesó aquí.
- La clasificación del GPFG como fondo de ahorro proviene de la nota 19 de los Principios de Santiago (SRC-0206). Si corresponde compararlo con un fondo de estabilización queda abierto.

## 4. Decisiones que quedan en manos de Alejandro (sin recomendación)

Las opciones y sus precedentes están en `tablas/opciones_diseno_fondo_d.csv`.

1. Ingresos que acumula el fondo (d): saldo de un resultado, fracción de un ingreso específico, flujo completo o aportes extraordinarios.
2. Destino de los rendimientos: quedan en el fondo o pasan al Tesoro.
3. Regla de retiro: disparador por caída de ingresos, situaciones de excepción, uso presupuestario anual, o regla ligada a un rendimiento esperado.
4. Tope: umbral de saldo, tope de aporte, tope de retiro o ninguno.
5. Quién decide: ministro por decreto, Congreso por resolución, directorio colegiado o disparador legal con comité de inversión.
6. Moneda y base de los umbrales: los precedentes usan porcentajes del PIB o del ingreso; en un régimen en USD falta definir la unidad.
