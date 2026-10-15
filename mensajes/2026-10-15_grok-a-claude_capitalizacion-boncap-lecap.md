# Grok a Claude: capitalización de BONCAP y LECAP, escenario de pago en caja y pendientes del lote G

Fecha: 2026-10-15. Pedido de Alejandro por llamada de voz. Rama propuesta `grok/lote-g-capitalizacion` (o dentro de `grok/lote-g`, que sigue sin publicar). Carpeta `inbox/lote-g/`. Todo en `sin_revisar`. Cifras en millones de pesos salvo indicación; un billón son 10^12 pesos, es decir un millón de millones.

## 1. Cuánto interés devengado no se paga cada mes

### Qué instrumentos son
Verificado contra SRC-0103 (cuadros A.1.7 y A.1.8), SRC-0102 (SIGADE al 30-06-2026) y las resoluciones de emisión (SRC-0603, 0606, 0607, 0613):
- **Capitalización de interés con pago íntegro al vencimiento** (a la par, amortización íntegra al vencimiento, tasa efectiva mensual capitalizable): 13 BONCAP y LECAP de TEM fija, 6 BONCAP y LECAP TAMAR más margen y 2 BONCAP Dual. Son los instrumentos que se cuantifican mes a mes.
- **Ajuste por CER devengado y no pagado** (cero cupón CER, LECER, BONCER, BONTE Dual CER/TAMAR y legados Par, Discount y Cuasipar): es indexación del capital y se informa aparte, sin proyectar hacia adelante porque el repositorio no tiene proyección de CER. En el cuadro A.1.8 el coeficiente combina CER y capitalización cuando existe.
- LELINK y BONTE dólar linked: coeficiente 1,0 en dólares al corte; no se cuantifican.
- Instrumentos con cupón en caja (BONAR, Global, BONTE a tasa fija, BONTE USD): sin capitalización.

### Método
1. **Saldo al corte.** SRC-0103 A.1.7 publica el valor nominal residual y el "valor nominal actualizado" (residual por coeficiente de capitalización al 30-06-2026). Ese valor coincide con el Saldo en Dólares de SIGADE (BONCAP 2,05% 15-01-2027: 10.069.640,917 miles de USD en ambos). **El saldo SIGADE incluye la capitalización devengada** (CLM-G-022). SIGADE muestra interés cero al vencimiento y trata el interés capitalizado como capital.
2. **Coeficiente.** El publicado avanza por meses enteros desde la emisión: (1+TEM)^k. Reproduce los 13 instrumentos de TEM fija dentro de 5e-6 (CLM-G-023). La fórmula legal de la RC 4/2025 usa exponente fraccionario (DÍAS/360 por 12, base 30/360; CLM-G-017). La diferencia entre ambos es chica pero existe: se informa `saldo_formula_legal_al_corte` junto al saldo SIGADE en `tablas/capitalizacion_instrumentos.csv`.
3. **TEM.** Fijas: dato del nombre del instrumento (ponderada 2,356%). TAMAR y duales: TEM implícita igual al coeficiente publicado elevado a 1/k, **supuesto** constante hasta el vencimiento (la TAMAR futura no se conoce).
4. **Serie mensual.** Para cada instrumento, B(t) = VN x (1+TEM)^(meses 30/360 desde la emisión). Devengado del mes = B(fin de mes) menos B(inicio de mes). Interés que sale en caja = B(vencimiento) menos VN, en el mes del vencimiento. El capital VN se muestra aparte.

### Cifras (derivadas; `tablas/capitalizacion_mensual.csv`)
Capitalización devengada y no pagada ya contenida en el saldo al 30-06-2026 (`tablas/capitalizacion_stock_corte.csv`):

| Grupo | Saldo SIGADE | Capitalización en el saldo |
|---|---|---|
| 13 BONCAP y LECAP TEM fija | 83.344.076 | 12.538.075 |
| 6 BONCAP y LECAP TAMAR | 30.637.898 | 2.489.064 |
| 2 BONCAP Dual | 11.140.049 | 4.277.447 |
| Total capitalización | 125.122.023 | 19.304.585 |

Ajuste por CER devengado y no pagado, aparte (otra naturaleza): BONCER cero cupón y LECER 61.810.650; BONTE Dual 486.940; BONCER con cupón 4.590.818; legados 24.043.603.

Interés que se devenga y no se paga en caja, mes a mes (julio de 2026 a junio de 2027; la tabla sigue hasta agosto de 2028):

| Mes | TEM fija: devengado no pagado | TEM fija: interés que sí sale en caja (al vencimiento) | Flotantes y duales (supuesto): devengado no pagado |
|---|---|---|---|
| 2026-07 | 1.944.985 | 733.736 | 1.069.131 |
| 2026-08 | 1.812.852 | 931.481 | 1.098.109 |
| 2026-09 | 1.700.853 | 1.127.844 | 860.522 |
| 2026-10 | 1.556.398 | 2.811.954 | 826.352 |
| 2026-11 | 1.264.442 | 936.647 | 848.130 |
| 2026-12 | 1.199.216 | 0 | 744.504 |
| 2027-01 | 1.054.089 | 6.462.590 | 636.021 |
| 2027-02 | 843.327 | 0 | 598.056 |
| 2027-03 | 988.108 | 0 | 548.594 |
| 2027-04 | 950.492 | 6.035.838 | 527.373 |
| 2027-05 | 552.124 | 3.583.588 | 540.335 |
| 2027-06 | 312.730 | 4.465.413 | 553.616 |

Lectura: en julio de 2026 se devengan unos 1,9 billones en las fijas y 3,0 billones sumando flotantes y duales (supuesto) sin que se pague ese monto en el mes. En los meses de vencimiento sale de una vez el interés de toda la vida del instrumento (por ejemplo 6,46 billones en enero de 2027 en las fijas).

Totales hasta el vencimiento (solo el stock vigente al 30-06-2026): devengado posterior al corte 14.179.614 en las fijas y 14.629.123 en flotantes y duales (supuesto). Capital VN que se paga al vencimiento: 70.806.002 y 32.585.954.

## 2. Escenario: el interés se paga en caja cada mes

### Definición
Contrafáctico simple: el saldo B0 de cada instrumento al corte (fórmula legal) queda constante, paga cada mes interés = B0 x ((1+TEM)^(días/30) menos 1) y devuelve B0 al vencimiento. No hay nueva emisión ni refinanciación después del 30-06-2026. Δ = interés del escenario menos interés que realmente sale en caja ese mes (`tablas/escenario_interes_en_caja.csv`).

### Comparación con lo publicado (SRC-0610, 0611, 0612)
Por definición el resultado primario excluye los intereses; el Boletín Fiscal expone el financiero como primario menos intereses netos (primer semestre de 2026: 7.327.029,2 menos 5.870.835,1 igual a 1.456.194,1). **El pago de interés en caja no modifica el primario; modifica el financiero.** Esto ajusta la premisa del pedido ("el superávit primario no se sostendría"): lo que cambia es el resultado financiero.

| Mes | Cobertura | Financiero publicado | Δ interés (escenario menos real) | Financiero ilustrativo |
|---|---|---|---|---|
| Julio 2026 | solo TEM fija | 244.897 | +1.211.249 | -966.352 |
| Julio 2026 | fijas más flotantes y duales (supuesto) | 244.897 | +2.280.380 | -2.035.483 |
| Agosto 2026 | solo TEM fija | 635.529 | +839.223 | -203.694 |
| Agosto 2026 | fijas más flotantes y duales (supuesto) | 635.529 | +150.752 | +484.777 |

Primario publicado: julio 2.960.333, agosto 1.990.322 (sin cambio en el escenario). Intereses netos publicados: julio 2.715.436, agosto 1.354.793.

### Dato oficial de capitalización
El Boletín Fiscal 2T26 informa "Capitalización de Bonos, Letras y otros préstamos" de 11.996.722,1 millones en el segundo trimestre y 24.401.605,2 millones en el primer semestre de 2026 (CLM-G-025). Contra el financiero del semestre (1.456.194,1) la diferencia aritmética es -22.945.411,1. **Solo aritmética, sin comparabilidad en rigor:** la línea es de la Administración Central en deuda bruta e incluye "ampliaciones" (alcance exacto no especificado), el resultado es del SPN neto de intereses intra-sector, y no se conocen las tenencias del propio sector público. La línea de rentas del BCRA del cuadro base caja figura en 24.400.000,0, cerca de la capitalización; son cuadros distintos y no se afirma relación.

### Qué no se pudo hacer
- No hay fuente oficial en el repositorio que desglose cuánto del interés pagado de julio y agosto corresponde a vencimientos de LECAP y BONCAP. El supuesto de que los intereses publicados incluyen el pago íntegro al vencimiento es mío. En julio, el interés de las LECAP fijas que vencen (733.736) cabe dentro de los 2.715.436 publicados; no se verificó la composición.
- Flotantes y duales dependen de una TEM implícita constante.
- Cobertura: solo el stock al 30-06-2026; las emisiones posteriores (que hubo en julio y agosto) no están en los datos. No se proyecta CER.
- El cuadro mensual del Boletín Fiscal está titulado "2025" pero sus totales coinciden con 2026; señalado, no resuelto.

## 3. Costo que se evita hoy y se acumula

Efecto medido con el contrafáctico del punto 2: como el interés no se paga, se capitaliza y devenga interés sobre sí mismo. Frente a pagar cada mes sobre un saldo constante, el interés sobre interés posterior al corte suma unos 1.316.151 en las fijas y 2.879.945 en flotantes y duales (supuesto), total cercano a 4,2 billones solo por el stock actual. Ese monto es el costo futuro que se posterga; no incluye lo ya capitalizado antes del corte (19,3 billones dentro del saldo).

**Ilustración (no es proyección).** Por cada 100 pesos de saldo, interés acumulado si se capitaliza frente a interés total si se paga cada mes (`tablas/ilustracion_posponer_interes.csv`):

| TEM | Meses | Capitalizando | Pagando cada mes | Interés sobre interés |
|---|---|---|---|---|
| 2,0% | 12 | 26,82 | 24,00 | 2,82 |
| 2,5% | 12 | 34,49 | 30,00 | 4,49 |
| 3,0% | 12 | 42,58 | 36,00 | 6,58 |
| 2,5% | 24 | 80,87 | 60,00 | 20,87 |
| 3,0% | 24 | 103,28 | 72,00 | 31,28 |

## 4. Estado de los pendientes del lote G

1. **Fechas explícitas.** `contratos/fechas_explicitas.csv` (51 filas) para INS-C-0359 (RC 11/2026, art. 4) e INS-C-0360 (RC 16/2026, art. 5, que incluye el 29-02-2028). El cargador no lee listas de fechas; falta decidir si se agrega esa lista o una regla. Los Par con período final corto siguen sin cubrir.
2. **Resoluciones de emisión.** Descargadas, con sha256 en `documents_manifest.csv`: RC 4/2025 (BONCAP Dual 15-09-2026 y 15-12-2026), RC 23/2026, RC 25/2026 y RC 32/2026 (BONTE Dual CER/TAMAR), RC 18/2022 (BONTE 23-05-2027), RC 24/2025 (BONTE 2030 a tasa fija), RC 62/2025 (BONTE USD 6,5% 2029), RC 16/2026 y Res. 66/2018. **Sin encontrar** la del BONAR Dual 2036 (SRC-0106 cita "Res. Conj. 53-E/2023"; la RC 53/2023 publicada trata otra materia). **Res. 66/2018:** el texto remite a un Anexo (IF-2018-12038106-APN-SECF#MF) que no está en la página, así que faltan las fracciones de las 125 cuotas (CLM-G-030). Los duales quedan descritos como máximo entre dos ramas (CLM-G-018 y 021); el motor no los carga.
3. **Tope de las letras BCRA.** `contratos/topes_propuesta.csv`: INS-C-0443, 0440 y 0441 con SOFR_TERM_1A (margen 0,71513 pp y -1,0 pp), INS-C-0444 y 0445 con LIBOR_1A (-1,0 pp), INS-C-0442 y 0447 sin tope. Propuesta de formato, no cargada.
4. **Base 30/360 y saldo.** Confirmada por norma en las resoluciones leídas (RC 4/2025, 23/2026, 24/2025, 25/2026, 62/2025, 11/2026, 16/2026, 40/2022 y Res. 66/2018). De los ocho instrumentos sin base en SRC-0106 quedan seis sin confirmar en norma: INS-C-0386, 0387, 0413, 0425, 0426 y 0427. El saldo SIGADE incluye la capitalización devengada (punto 1, método 1).

Contradicción señalada, sin resolver: SRC-0106 describe el BONTE USD 6,5% 2029 con pago "al tipo de cambio aplicable"; la RC 62/2025 dice pago en dólares y SIGADE también (CLM-G-007 y CLM-G-033).

Nota sobre el motor: el lote G ya carga la capitalización con períodos mensuales anclados hacia atrás desde el vencimiento. La fórmula legal usa exponente DÍAS/30 y SIGADE avanza por meses enteros desde la emisión. Conviene revisar cuál adopta el motor.

## Archivos
- `inbox/lote-g/tablas/`: `capitalizacion_instrumentos.csv`, `capitalizacion_mensual.csv`, `capitalizacion_stock_corte.csv`, `capitalizacion_oficial_flujos.csv`, `resultado_fiscal_publicado.csv`, `escenario_interes_en_caja.csv`, `ilustracion_posponer_interes.csv`.
- `inbox/lote-g/contratos/`: `fechas_explicitas.csv`, `topes_propuesta.csv`.
- `inbox/lote-g/`: `sources.csv` (SRC-0603 a 0614), `claims.csv` (CLM-G-017 a 034), `documents_manifest.csv`, `unresolved.md`, `sintesis.md`, `scripts/` (cálculo reproducible).
- Los originales de `docs/` quedan fuera del commit por .gitignore.

## Para decidir
1. Formato de lista de fechas explícitas o regla de período final corto.
2. Campo de tope para letras BCRA.
3. Número de la resolución del BONAR Dual 2036 y el Anexo de la Res. 66/2018.
4. Tenencias del sector público en BONCAP y LECAP, para acercar el perímetro al del SPN.
5. Si se incluyen las emisiones posteriores al 30-06-2026.
