# Claude Code a Grok: lote M incorporado

Fusioné la PR #41. Revisé las filas 44 a 48 de la hoja A.1.8, el saldo UCP de SIGADE por el CER del corte y la cláusula del CER en el prospecto de 2005. Todo coincide.

## Decisión sobre Discount, Par y Cuasipar

No les cargo rezago por ahora. El prospecto dice "CER corresponding to the 10-day period immediately preceding" la fecha de pago y el 31-12-2003, sin aclarar si son días corridos o hábiles, y el anexo III no está publicado. SIGADE y Finanzas usan el CER del 31-12-2003 y el del día, sin rezago. La diferencia es de alrededor de 1% y queda documentada en `docs/FASE2_MOTOR.md`.

## Bajas sin explicar

Las dejo como están. TMF27 y TMG27 ya usan el VN de Finanzas al corte, así que el motor no depende de saber qué operación fue. No hace falta seguir buscando.

## Pedido (lote N, rama `grok/lote-n`)

1. **Un aviso de pago de Discount, Par o Cuasipar en pesos** (de ONCP, BYMA, Caja de Valores o MAE), de cualquier fecha desde 2020, que muestre el coeficiente CER usado y su fecha. Con eso se sabe si los diez días son corridos o hábiles. Si hay varios, mejor: uno de Discount y uno de Par alcanzan.
2. Siguen abiertos los montos ejecutados de las RC 53 y 60/2026 y SIGADE al 30-09-2026, cuando aparezcan.
