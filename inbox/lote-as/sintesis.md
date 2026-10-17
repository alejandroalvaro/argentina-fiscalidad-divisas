# Lote AS: enero 2025, febrero 2024 y pendientes

Rama `grok/lote-as`. Fuentes nuevas SRC-2060 a SRC-2066; claims CLM-AS-001 a CLM-AS-014. Todo en el idioma de las series: USD millones donde dice USD, pesos millones donde dice pesos; no sumé pesos con dólares.

## 1. Enero 2025 y el BONAR DUAL 31-01-2025 (TDE25)

**La RC 4/2025 no lo convirtió.** El anexo IF-2025-08038033 (copia de InfoLeg, SRC-2060) lista TE1 a TE11, todos en pesos (LECAP, un cero cupón CER, un BONCAP y un BONCER). El resultado de Finanzas (SRC-2061) adjudicó $ 8.043.220 millones de VNO y emitió $ 3.500.632 millones de cada bono dual nuevo. ONCP coincide fila por fila (tabla `rc4_2025_titulos_elegibles_vs_oncp.csv`).

**Lo que sí pasó con el TDE25 fue otra resolución, la RC 5/2025** (BORA del 27-01-2025, SRC-2063). El artículo 4 convierte TDE25 con el BCRA por una canasta de 46% S31M5, 36% S16Y5 y 18% S18J5, con liquidación el 24-01-2025, siete días antes del vencimiento. ONCP lo registra en Otras Operaciones (filas 4 a 6, tres LECAP por 4.071.877,4 millones de pesos de VN, en proporción 46/36/18) y no como baja. Con los precios del artículo 4 estimo (derivado, no publicado) un VN de TDE25 convertido de USD 4.162,0 M, 48,4% de los USD 8.596,4 M. Quedarían USD 4.434,3 M para el vencimiento.

**El 3.123 de la A.5 no se suma al 8.596,4.** El capital en moneda extranjera de la A.5 (3.123,3) es Bonares y Globales del 9 de enero (2.813,3) más capital de préstamos (310,4), y ya está dentro del total de la A.4 en moneda extranjera: 8.596,4 + 2.813,3 + 312,1 = 11.721,8. Contra el AIF (USD 8.795,2 M) la diferencia es de menos 2.926,6 si se compara con ese total, y de más 1.235,4 si se descuenta la conversión del BCRA. No sé cuál es el tratamiento del AIF; lo dejo sin explicar (ver `unresolved.md`). Mi hipótesis, sin probar, es que el AIF excluye la conversión por no ser caja y que el resto de la diferencia está en la forma de valuar el pago en pesos del TDE25 o en tenencias del sector público.

**Rótulo de ONCP.** La baja "BONTE/U$S/0%/30-06-2025 Paga en pesos" de la conversión del 29-01-2025 es, por el monto y por el anexo, el TZX25 (CER). Eso corrige la lectura de CLM-AO-025 y toca cualquier tabla que haya tomado esas filas como BONTE U$S.

## 2. Febrero 2024 y los cerca de USD 2.400 M

El residuo de USD 2.425,5 M del lote AP aparece por haber puesto el vencimiento del BONAR DUAL 28-02-2024 (4.938,7, que paga en pesos) como parte de la amortización en moneda extranjera. La operación grande en moneda extranjera de febrero de 2024 es la compra al BCRA de AL35 por VNO USD 7.595,9 M (RC 13/2024, liquidada el 20-02-2024, SRC-2064), que ya estaba como baja sin contrapartida en la A.4 (fila 378). Con AL35 en lugar del BONAR DUAL, más letras USD de organismos públicos (1.173,7) y préstamos (1.111,2), la suma es 9.880,8 contra 9.649,1 del AIF: diferencia de menos 231,7 (2,4%). La OPC de febrero de 2024 (SRC-2066) confirma la recompra de AL35. El TDF24 de entidades del Estado se canjeó en parte por BONCER TX25 (RC 14/2024, SRC-2065). Es una explicación compatible, no una prueba de cómo imputa el AIF.

## 3. Pendientes

Informe sobre Bancos de agosto (PDF) y las páginas del BCRA siguen en HTTP 502. El balance cambiario de septiembre sale el 30-10-2026.
