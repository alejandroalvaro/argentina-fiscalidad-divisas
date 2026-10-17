# Síntesis del lote AJ: pasivos remunerados, intereses y tenedores (enero de 2023 a septiembre de 2026)

Todo lo que sigue sale de las tablas de `tablas/` y de las afirmaciones de `claims.csv` (CLM-AJ-001 a 048). Donde la fuente es prensa, se dice.

## 1. Pasivos remunerados del BCRA (tabla `pasivos_remunerados_bcra_mensual.csv`)

- **Qué hay en cada tramo (fuente oficial: hoja INSTRUMENTOS DEL BCRA de Series.xlsm, con las notas de la hoja NOTAS).**
  - Enero de 2023 a julio de 2024: LELIQ y NOTALIQ más pases pasivos del BCRA (con FCI hasta 2024). Al 31-01-2023: pases $2,5 billones y LELIQ $8,0 billones. Al 29-12-2023: pases $24,2 billones y LELIQ $1,6 billones, con tasa de política monetaria de 100% TNA. Al 31-01-2024 los pases llegaron a $29,9 billones, el máximo del período.
  - Julio de 2024 a julio de 2025: los pases pasivos se suspendieron (el 22-07-2024 según el Informe al Congreso 2024) y las entidades tuvieron LEFI, emitidas por el Tesoro y capitalizadas a la tasa de política monetaria. Al 31-07-2024 las entidades tenían LEFI por $9,6 billones (valor técnico), y al 30-06-2025 por $11,0 billones. Las entidades mantuvieron saldos hasta el 08-07-2025.
  - Desde el 15-07-2025: no hay pases, LELIQ ni LEFI. Queda la columna "Otros": saldo neto de operaciones de corto plazo del BCRA (repos, simultáneas) a tasas de mercado. Al 30-09-2026: $0,96 billones.
- **Relación con la base monetaria** (columna calculada: pases + LELIQ + LEFI + otros sobre la base monetaria del mismo día): 1,98 en enero de 2023, máximo de 3,14 en septiembre de 2023, 2,68 en diciembre de 2023 y 2,73 en enero de 2024. Baja a 0,44 en julio de 2024, 0,30 en junio de 2025 y 0,02 en septiembre de 2026. El BCRA dice lo mismo en su informe de junio de 2026: "Títulos BCRA + Pases llegó a representar 2,5 veces la base monetaria hacia finales de 2023".
- **Quién pasó a pagar.** El BCRA cuenta que en julio de 2024 "el stock de pasivos remunerados fue canjeado por LEFI" y que "se saneó la hoja de los pasivos del balance del BCRA". Sus estados contables 2024 hablan del "traspaso de todos los pasivos remunerados al Tesoro". Es decir, desde julio de 2024 el interés de la absorción bancaria lo capitaliza el Tesoro (LEFI), no el BCRA. Después de julio de 2025 vuelve el BCRA con repos, de monto mucho menor.
- **Factores de explicación de la base monetaria** (tabla `factores_base_monetaria_mensual.csv`, suma mensual de las variaciones diarias de la hoja BASE MONETARIA, millones de pesos): compras al sector privado y al Tesoro, adelantos, utilidades, resto de operaciones con el Tesoro, pases, LELIQ, redescuentos, intereses y primas, LEBAC, LEFI y otros. La nota oficial dice qué incluye cada uno (CLM-AJ-001 a 005). Un detalle clave: en el factor de LELIQ "se excluye la expansión vinculada al pago de intereses", que va en el factor "Intereses, primas y remuneración de cuentas corrientes".
- **Tasas.** Tasa de política monetaria TNA y TEA hasta el 10-07-2025 (100% a fines de 2023, 40% en 2024, 29% en 2025). Desde entonces solo pongo la tasa de pases entre terceros a 1 día como referencia (no es la del BCRA).

## 2. Intereses pagados por el BCRA (tabla `intereses_bcra_estados_contables.csv`)

No hay serie mensual oficial. Lo anual, de los Estados Contables (miles de pesos, moneda constante del cierre de cada informe):

| Ejercicio | LELIQ | NOTALIQ | Primas netas por pases | Intereses perdidos, total |
|---|---|---|---|---|
| 2023 (cierre 2023) | 17.858.764.024 | 690.542.176 | 9.122.062.251 | 28.022.811.966 |
| 2024 (cierre 2024) | 97.540.168 | 2.570.277 | 15.981.057.405 | 17.071.810.697 |
| 2025 (cierre 2025) | 0 | 0 | 276.310.201 | 1.647.504.861 |

- LELIQ, NOTALIQ y pases fueron 98,7% de los intereses perdidos en 2023 y 94,2% en 2024 (cuentas mías sobre los totales de arriba). En 2025 los pases explican 16,8%; el resto es BOPREAL (481.175.172), otras letras (181.029.366) y organismos internacionales (708.875.185).
- En 2024 los pases devengaron primas por $16,0 billones aunque se suspendieron en julio: son los siete primeros meses del año, con pases de $30 billones a 100% y luego 80% y 40% TNA.
- La información comparativa del informe 2024 reexpresa 2023: LELIQ $38.889.892.358 miles y pases $19.864.533.657 miles (pesos de diciembre de 2024). El informe 2025 reexpresa 2024: intereses perdidos $22.457.755.370 miles y pases $21.022.882.933 miles.
- Del lado de lo que cobra el BCRA: intereses ganados sobre títulos públicos de $7.525.634.257 miles (2023), $29.521.024.639 miles (2024) y $23.306.000.106 miles (2025). No están abiertos por título (LEFI incluidas o no).
- Sustituto mensual: el factor "Intereses, primas y remuneración de cuentas corrientes" de la base monetaria suma $32,3 billones en 2023, $21,9 billones en 2024 y cero desde julio de 2025 (pesos corrientes, por eso no se compara con el cuadro anterior).

## 3. Quién tiene la deuda en pesos del Tesoro

- **Oficial, por acreedor (Finanzas, deuda bruta total, no solo pesos):** al 30-06-2026 la deuda en poder de agencias del sector público era USD 197.213 millones (41,6% del total) y la del sector privado USD 177.738 millones. La serie trimestral va en `deuda_bruta_por_acreedor_trimestral.csv`. Finanzas no abre BCRA y FGS.
- **Oficial, por instrumento (Finanzas, cuadro A.1.7, USD millones, valor actualizado):** al 30-06-2026 LECAP USD 30.467, BONCAP USD 46.391, BONCAP duales USD 7.512, dollar linked USD 8.954; total de títulos en moneda nacional USD 95.428. LEFI de USD 22.363 a 23.835 millones entre septiembre de 2024 y junio de 2025 (cuadro por trimestre en `deuda_tesoro_en_pesos_por_instrumento_trimestral.csv`).
- **Bancos (Informe sobre Bancos, `bancos_cartera_titulos_mensual.csv`):** títulos públicos totales de cada grupo, con LEBAC/NOBAC/LELIQ y pases activos aparte, en pesos corrientes. No abre LECAP, BONCAP ni CER.
- **BCRA:** títulos públicos en su balance: $45,9 billones (2023), $74,6 billones (2024), $110,6 billones (2025), cada uno en pesos de su cierre (`bcra_balance_titulos_pases_base_monetaria_anual.csv`).
- **Estimaciones de prensa, confianza media:** 1816 (mayo de 2026): 49% de los títulos en pesos cotizantes en BCRA y FGS, 28% en bancos, 23% en FCI, seguros, no residentes y otros. Facimex (octubre de 2025): 58% en manos oficiales; entre lo privado, bancos 41% y FCI 7%.
- **Huecos:** FCI (CNV/CAFCI) sin bajar. Ver `unresolved.md`, punto 5.

## 4. Resultado de los bancos (`bancos_resultados_anual.csv` y `_mensual.csv`, millones de pesos de agosto de 2026)

| Sistema financiero | Margen financiero | Resultado por títulos valores | Primas por pases | Resultado total |
|---|---|---|---|---|
| 2023 | 101,9 billones | 93,6 billones | 30,2 billones | 14,9 billones |
| 2024 | 89,1 billones | 34,5 billones | 25,2 billones | 15,9 billones |
| 2025 | 50,2 billones | 22,8 billones | -0,01 billones | 2,6 billones |
| Enero a agosto de 2026 | 37,4 billones | 14,2 billones | 0,28 billones | 3,6 billones |

- Títulos más primas por pases equivalen a 122% del margen financiero en 2023, 67% en 2024, 45% en 2025 y 39% en enero a agosto de 2026. Son razones brutas, no una parte del resultado: el margen incluye egresos por intereses que no se descuentan en esos dos rubros (ver `unresolved.md`, punto 6).
- Bancos públicos: las primas por pases pesaron más en 2024 (11,9 billones, contra 8,6 de resultado por títulos). Bancos privados: 20,4 billones en 2023 y 13,2 en 2024.
- El BCRA da la explicación en palabras: el espacio de LELIQ y pases en el activo "fue reemplazado por las tenencias de LEFI, otros instrumentos de financiamiento al sector público y por la creciente relevancia del crédito al sector privado", y atribuye la caída de la rentabilidad de 2024 a "un menor margen financiero integral real". En 2026 destaca "menores egresos por intereses" y la banca pública.

## 5. Con qué pesos compra el Tesoro

- No hay un comunicado que lo diga compra por compra (`unresolved.md`, punto 9). Las declaraciones oficiales son estas, de la tabla `origen_de_los_pesos_del_tesoro_declaraciones.csv`:
  - BCRA, junio de 2026: el Tesoro modera "la demanda de dólares al BCRA con pesos provenientes del superávit fiscal" al financiarse en dólares.
  - BCRA, junio de 2026: en mayo de 2026 el Tesoro usó "$ 12 billones de las utilidades" del BCRA para recomprar Letras Intransferibles.
  - BCRA, abril de 2026: las licitaciones de deuda en pesos superaron vencimientos y los fondos "fueron depositados en el BCRA".
  - Economía, programa financiero 2026-2027: "los intereses se pagan con superávit fiscal" y la deuda nueva "se emite exclusivamente para refinanciar el capital".
  - Caputo (Presidencia): comprar dólares acompañando la demanda de dinero, sin "esterilizando pesos y generando un déficit cuasifiscal".
- La secuencia que describe la prensa (Bopreales al BCRA contra pesos, esos pesos para comprar dólares al BCRA) es de una fuente no oficial y la dejé con confianza media.

## Qué cambia respecto de D-015

1. El costo de esterilizar de 2023 y enero de 2024 está medido del lado del BCRA: $27,7 billones de intereses y primas en 2023 (pesos de diciembre de 2023) y $16,1 billones en 2024 (pesos de diciembre de 2024). Los cobraron los bancos: primas por pases de $30,2 billones en 2023 y $25,2 billones en 2024 en el resultado del sistema.
2. Desde julio de 2024 el costo de la absorción bancaria pasó del BCRA al Tesoro (LEFI) y desde julio de 2025 es mucho menor (repos). El costo ya no está en los balances del BCRA, está en los intereses del Tesoro y en el resultado por títulos de los bancos (sin abrir por instrumento).
3. Para el período 2024 a 2026, la medida de D-015 requiere una estimación propia con saldo y tasa de LEFI y LECAP/BONCAP. Esa estimación no está en este lote.
