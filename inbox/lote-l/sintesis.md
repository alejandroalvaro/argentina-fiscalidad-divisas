# Lote L: síntesis (sin_revisar)

Resumen de lo hallado para los cinco pedidos. Todo queda `sin_revisar`. Cifras en millones de pesos salvo que se diga otra cosa. El detalle y los huecos están en `unresolved.md`; el respaldo, en `claims.csv` y `tablas/`.

## 1. VNO rescatado en las conversiones con el BCRA

**Para Claude:** las normas y los informes oficiales no publican el VN rescatado. Se derivó de las planillas trimestrales de Finanzas (hoja A.1.8, diez cortes de 2024-03-31 a 2026-06-30) más las emisiones de ONCP (`tablas/bonceres_cadena_vno_y_bajas.csv`, `tablas/conversiones_bcra_vno_rescatado.csv`):

| Operación | TZXD7 (INS-C-0373) | TZX28 (INS-C-0380) |
|---|---|---|
| RC 64/2025, liquidada 2025-12-29 (por AE38 y AL35) | 1.550.000 (exacto) | 2.350.000 (exacto) |
| RC 31/2026, liquidada 2026-06-08 (canasta 66% AL35, 34% AE38) | 1.300.000 (exacto) | 1.273.835,9 (incertidumbre de alrededor de 1 millón) |

VN en circulación al 2026-06-30 según Finanzas: TZXD7 9.092.457,493; TZX28 5.339.258,590; TZX27 2.522.244,610. Cortes previos: ver las tablas. Se cargaron cuatro filas `canje_salida` en `contratos/operaciones.csv` con referencia "VNO DERIVADO". Quedan tres bajas sin explicación (TZXD7 2.363,622 y TZX28 1.831,564 en el segundo trimestre de 2025; TZX27 556.267,947 en el primero de 2026).

## 2. TMG27

**Para Claude:** no hay total publicado en una licitación posterior al corte (siete licitaciones revisadas). La planilla de Finanzas al 2026-06-30 da 1.535.738,988, que es 415.000 menos que lo acumulado por ONCP; el TMF27 muestra 485.000 de baja exacta. No se sabe qué operación.

## 3. BONAR Dual 2036

**Para Claude:** no se halló la RC 53/2023. Texto del Anexo III del DNU 164/2023: negociable, a cotizar en el MAE; art. 3 y 4 los dirigen al sector público nacional; la UBA dice que la mayoría de lo involucrado era del FGS. Stock constante en 640.874,451 miles de USD en los diez cortes. No hay publicación de tenedores actuales.

**Para Alejandro:** para consolidación en la fase 3, la norma de base indica que los tenedores iniciales fueron entes del sector público nacional, pero no hay dato oficial hallado sobre quién los tiene hoy.

## 4. BONCER con cupón

**Para Claude:** INS-C-0386 y 0387 son los BONCER 2,00% 2026 y 2,25% 2028 del Decreto 676/2020 (Anexo 4). VN al 2026-06-30 en pesos (cálculo de Grok con el A3500 de la planilla): 0386 222.131,127; 0387 79.555,431; 0388 110.944,635.

## 5. RC 53 y 60/2026 y SIGADE al 2026-09-30

**Para Claude:** nada publicado todavía (ONCP al 2026-08-31, OPC de agosto, Finanzas al 2026-06-30).
