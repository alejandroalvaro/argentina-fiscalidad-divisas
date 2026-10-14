# Lote C: síntesis breve (inventario de obligaciones)

Corte principal: 30/06/2026 (base SIGADE y planilla trimestral de la Secretaría de Finanzas). Unidades: las cifras de los cuadros oficiales A.1.x se expresan en miles de USD. La base SIGADE expresa los montos en dólares (unidades, no miles). En `instruments.csv`, `outstanding_usd_equiv_sigade` está en USD y `outstanding_principal` está en la moneda de origen de la operación (`currency_code_sigade`): pesos para ARP, unidades de capital ajustable por CER para UCP y USD para DLK.

**Fuente masiva.** La Secretaría de Finanzas publica cada trimestre una base SIGADE en formato Access, con saldo por operación y perfil de vencimientos. La base al 30/06/2026 tiene 753 operaciones en situación de pago normal. Su suma en USD coincide con el cuadro oficial de deuda en pago normal: 471.689.788.348 USD en SIGADE frente a 471.689.788 miles de USD en A.1.1. Las tablas se exportaron a CSV en `data/` sin modificar valores.

**Agregados oficiales (cuadros A.1.x, miles de USD).** Deuda bruta de la Administración Central: 474.197.959. Moneda local: 225.156.583, de la cual ajustable por CER 126.507.979. Moneda extranjera: 246.638.484. Organismos internacionales: 96.424.997, de los cuales FMI 57.705.452. Deuda elegible pendiente de reestructuración: 2.402.892.

**Familias.** SIGADE permite separar moneda del préstamo, moneda de pago y tipo de tasa. Los instrumentos CER (código UCP) y dólar-linked (código DLK) se pagan en pesos. Los duales (BONCAP, BONAR y BONTE) se identifican por nombre. Los préstamos de multilaterales y bilaterales aparecen en el mismo registro.

**Indexación frente a familia.** En `instruments.csv` hay 43 operaciones con indexación CER y 38 en la familia "ARS CER", y 8 dólar-linked frente a 7 en la familia "dólar-linked". La verificación sobre los datos indica que la diferencia corresponde a los duales: 5 BONTE DUAL CER/TAMAR (código UCP, INS-C-0408 a 0412) y 1 BONAR DUAL 2036 (código DLK, INS-C-0357) están en la familia "dual". Los otros 2 duales (BONCAP DUAL, código ARP) no tienen indexación informada. 38 + 5 = 43 y 7 + 1 = 8.

**Limitaciones.** Ninguna fuente oficial descargada vincula ISIN con saldo vigente; la columna queda vacía. El registro tiene inconsistencias de códigos que se documentan en unresolved.md. El inventario cubre solo la Administración Central y no incluye al BCRA ni pasivos contingentes fuera de avales.
