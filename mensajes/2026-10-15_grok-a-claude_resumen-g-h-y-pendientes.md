# Grok a Claude: resumen de los lotes G y H, hallazgos, límites y preguntas para Alejandro

Fecha: 2026-10-15. Alejandro pidió pasarte lo hecho con una nota explicativa. Todo está `sin_revisar`. Dos PR, uno por lote, ramas `grok/lote-g` y `grok/lote-h-fondos`. Esta nota viaja en el PR del lote G.

## Lote G (rama `grok/lote-g`, carpeta `inbox/lote-g/`)
- Términos contractuales de 70 instrumentos: `contratos/terminos.csv` (70), `tasas.csv` (70), `amortizaciones.csv` (461). `unresolved.md` lista 51 operaciones sin cargar con el motivo. `verificacion_motor.csv` compara fecha por fecha contra SIGADE (60 coinciden, 10 con diferencias explicadas).
- Capitalización de BONCAP y LECAP (pedido por voz): `tablas/capitalizacion_*.csv`, `escenario_interes_en_caja.csv`, `ilustracion_posponer_interes.csv`, `resultado_fiscal_publicado.csv`. Detalle en `mensajes/2026-10-15_grok-a-claude_capitalizacion-boncap-lecap.md`.
- Propuestas de formato: `contratos/fechas_explicitas.csv` (51 filas) y `contratos/topes_propuesta.csv` (7 filas).
- Fuentes SRC-0601 a SRC-0614 y claims CLM-G-001 a CLM-G-034. `scripts/` reproduce el cálculo.

## Lote H (rama `grok/lote-h-fondos`, carpeta `inbox/lote-h/`)
- 13 fuentes (SRC-0701 a 0713) y 29 claims (CLM-H-001 a 029) sobre fondos de estabilización: Chile FEES, Noruega GPFG, Colombia FAE, Perú FEF.
- `tablas/fondos_comparacion.csv` (5 filas) y `tablas/opciones_diseno_fondo_d.csv` (18 filas, sin recomendación).
- `docs/APORTES_PROPUESTOS.md`: aporte 6 con cuatro regímenes (se agregó la definición de (d) con D-007).

## Hallazgos clave
1. **Capitalización.** El saldo SIGADE al 30-06-2026 incluye la capitalización devengada: 19.304.585 millones en 21 BONCAP y LECAP (12.538.075 fijas, 2.489.064 TAMAR, 4.277.447 duales). En julio se devengan unos 1,9 billones en las fijas sin pagarse en el mes.
2. **Primario y financiero.** El primario excluye intereses por definición, así que pagar ese interés en caja no lo cambia. Cambia el financiero. Julio ilustrativo solo con las fijas: 244.897 publicado contra -966.352. Esto corrige la premisa del pedido original.
3. **Dato oficial.** El Boletín Fiscal 2T26 informa capitalización de 24.401.605 millones en el primer semestre contra un financiero de 1.456.194. La diferencia aritmética no es comparable en rigor por perímetro (Administración Central bruta contra SPN neto).
4. **BONCER 2,5% 2031.** SRC-0106 dice amortización íntegra al vencimiento; la Res. Conj. 40/2022 y SIGADE dicen diez cuotas semestrales. Se cargó la resolución. Contradicción señalada.
5. **Correcciones de SRC-0106.** Global USD 2035 con amortización del 2030 y tramo de tasa omitido; error de fecha en el EUR 2041 ("09-97-2021"); BONTE USD 6,5% 2029 con pago "al tipo de cambio aplicable" frente a pago en dólares en la RC 62/2025 y en SIGADE (CLM-G-007 y CLM-G-033).
6. **Convención de capitalización.** SIGADE avanza por meses enteros desde la emisión, la fórmula legal usa exponente DÍAS/30 y el lote G ancla los períodos hacia atrás desde el vencimiento. Conviene decidir cuál adopta el motor.

## Limitaciones
- Cobertura de capitalización: solo el stock al 30-06-2026, sin emisiones posteriores ni rollover. CER y dólar linked no se proyectan. Flotantes y duales usan una TEM implícita constante (supuesto).
- No hay fuente que desglose cuánto del interés pagado en julio y agosto es de vencimientos de LECAP y BONCAP.
- Resoluciones no encontradas: BONAR Dual 2036 y el Anexo IF-2018-12038106 de la Res. 66/2018. Seis instrumentos sin base 30/360 confirmada en norma: INS-C-0386, 0387, 0413, 0425, 0426 y 0427.
- Lote H: Colombia desde leyes.co (no oficial); Noruega leída con WebFetch (`.txt` son transcripciones); Perú sin saldo del FEF como porcentaje del PBI. Contradicción abierta en la nota 18 de los Principios de Santiago (precio de referencia del cobre).
- El Boletín Fiscal titula "2025" un cuadro mensual cuyos totales coinciden con 2026.

## Cinco preguntas para Alejandro
1. Formato de lista de fechas explícitas o regla de período final corto para el cargador.
2. Campo de tope para las letras BCRA (LIBOR o SOFR menos un punto).
3. Número de la resolución del BONAR Dual 2036 y el Anexo de la Res. 66/2018.
4. Tenencias del sector público en BONCAP y LECAP, para acercar el perímetro al del SPN.
5. Si se incluyen las emisiones posteriores al 30-06-2026.

Además, las reglas del fondo del régimen (d) del lote H las decide Alejandro (D-007).

## Arquitectura de agentes
Existe `/workspace/arquitectura_agentes.md` en la caja (no se sube al repo: no pertenece a un lote). Resumen:
- **Publicar sin la Mac.** Recomendado: token de grano fino (un solo repo; Contents y Pull requests en lectura y escritura; vencimiento de 30 a 90 días) guardado en la caja, más un ruleset sobre `main` (PR obligatorio, push restringido). Variante más segura y más trabajosa: GitHub App con token de una hora. Un token de grano fino no se puede limitar por nombre de rama, por eso el ruleset. No verificado: si los rulesets están disponibles en repos privados del plan actual.
- **Cola de decisiones.** `docs/DECISIONES_PENDIENTES.md` o, mejor para avisos, un Issue por decisión con la etiqueta `necesita-alejandro` (aviso push en GitHub Mobile). Cada nota de `mensajes/` abriría con `Para:`, `De:`, `Acción requerida:` y `Bloquea a:`.
- **Validación.** Opcional: Claude Code GitHub Action para correr `make validate-grok` en cada PR.
- Alejandro tendría que crear el token y el ruleset en su sesión de GitHub. Los precios y puntos marcados "no verificado" están así en el documento.
