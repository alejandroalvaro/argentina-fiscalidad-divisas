# Lote C: síntesis breve (inventario de obligaciones)

Corte principal: 30/06/2026 (base SIGADE y planilla trimestral de la Secretaría de Finanzas). Montos en miles de USD según las fuentes oficiales.

**Fuente masiva.** La Secretaría de Finanzas publica cada trimestre una base SIGADE en formato Access, con saldo por operación y perfil de vencimientos. La base al 30/06/2026 tiene 753 operaciones en situación de pago normal. Su suma en USD coincide con el cuadro oficial de deuda en pago normal (471.689.788). Las tablas se exportaron a CSV en `data/` sin modificar valores.

**Agregados oficiales.** Deuda bruta de la Administración Central: 474.197.959. Moneda local: 225.156.583, de la cual ajustable por CER 126.507.979. Moneda extranjera: 246.638.484. Organismos internacionales: 96.424.997, de los cuales FMI 57.705.452. Deuda elegible pendiente de reestructuración: 2.402.892.

**Familias.** SIGADE permite separar moneda del préstamo, moneda de pago y tipo de tasa. Los instrumentos CER (código UCP) y dólar-linked (código DLK) se pagan en pesos. Los duales (BONCAP, BONAR y BONTE) se identifican por nombre. Los préstamos de multilaterales y bilaterales aparecen en el mismo registro.

**Limitaciones.** Ninguna fuente oficial descargada vincula ISIN con saldo vigente; la columna queda vacía. El registro tiene inconsistencias de códigos que se documentan en unresolved.md. El inventario cubre solo la Administración Central y no incluye al BCRA ni pasivos contingentes fuera de avales.
