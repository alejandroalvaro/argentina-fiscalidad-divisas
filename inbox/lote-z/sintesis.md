# Lote Z: letras en garantía del FODER (SIGADE, 109 letras, USD 3.774 millones)

Todo `sin_revisar`. Hecho el 2026-10-15 (hora de Brasilia). Fuentes nuevas SRC-1278 a SRC-1286; los datos de SIGADE son SRC-0102 (ya en main, tablas del lote C). Los montos marcados "cálculo" son sumas mías sobre las filas de SIGADE.

## Respuesta corta

Las 109 letras son las **Letras del Tesoro en Garantía** del FODER. Las tiene el FODER (fondo fiduciario público, BICE fiduciario). Son **deuda contingente**: cada 31 de diciembre vencen y se devuelven y cancelan sin pago, salvo que un generador ejerza la opción de venta y el Estado no aporte los fondos. SIGADE las muestra con un calendario mecánico anual, que no es un cronograma de pago firme.

## 1. Quién las tiene

- **El FODER**, no los generadores. El Decreto 882/2016 (art. 14) faculta a Hacienda a emitir y entregar las letras "al FODER, por cuenta y orden del Ministerio de Energía y Minería", contra certificados de participación a favor del fiduciante (SRC-1279). El modelo de Acuerdo de Adhesión dice que se transfieren al FODER mediante depósito en la "Cuenta CRYL" (SRC-1282).
- **Fiduciante y fideicomisario: el Estado Nacional** (por el Ministerio de Energía y Minería, hoy sus sucesores); **fiduciario: el BICE**, sustituible por el fiduciante (Ley 27.191 art. 7 y Decreto 882/2016 art. 7; SRC-1278, SRC-1279). La Ley lo llama "Fondo Fiduciario Público".
- Los **generadores son beneficiarios del FODER**, no tenedores: solo pueden subrogarse en el derecho del fiduciario a reclamar el pago a Hacienda si ni Energía ni Hacienda cumplen (cláusula 8.2 del Acuerdo; SRC-1282).
- La contrapartida: el fiduciario emite certificados de participación al fiduciante por el mismo monto (contrato de fideicomiso, cláusula 3.02; SRC-1283). La OPC dice que el colateral son esos certificados a favor del Tesoro (SRC-1286).
- Consecuencia que dejo a tu criterio: legalmente son tenencia de un fondo fiduciario público cuyo fiduciante y fideicomisario es el Estado. Los fondos, si se pagara, se usan "exclusivamente" para pagar a un generador (cláusula 8.1 e; SRC-1282), es decir, a un privado.

## 2. Contingente o con cronograma firme

- **Contingente.** La OPC: "En caso de no realizarse la contingencia, las letras expiran a su vencimiento sin generar pago alguno" y las cuenta como deuda indirecta (SRC-1286). El Decreto 882/2016 art. 14 y el Decreto 471/2017 art. 3: anualmente, si no se ejerció la opción de venta, las letras vencen, se devuelven al fiduciante y Hacienda las cancela y las da de baja del registro de deuda pública, sin aportes de capital (SRC-1279, SRC-1281).
- **Cuándo se pagan.** Solo si un generador ejerce la opción de venta de su central (causales: falta de pago de cuatro liquidaciones consecutivas o seis no consecutivas de CAMMESA; imposibilidad de comprar dólares o transferirlos al exterior; entre otras, Decreto 882 art. 4 y Acuerdo 7.1) **y** el Estado no transfiere los recursos al FODER en el plazo del contrato: ahí las letras "se considerarán vencidas y exigibles" y las paga Hacienda al FODER (Decreto 882 art. 14; Acuerdo 8.1 d). El precio de venta no puede superar la inversión no amortizada (Decreto 882 art. 3; OPC).
- **Primeras líneas de pago antes de las letras:** la cuenta de garantía del FODER, financiada con un cargo a la demanda (Decreto 531/2016 Anexo I art. 7; SRC-1280), y el aporte del Ministerio de Energía.
- **Suspensión:** el vencimiento de las letras se suspende por el monto de la central desde la notificación de la causal de venta (Decreto 471/2017 art. 3; SRC-1281).
- **Qué muestra SIGADE (cálculo, SRC-0102):** 109 letras a tasa cero, saldo USD 3.773,7 millones; las 1.540 filas de vencimientos caen todas un 31 de diciembre; el principal es USD 265,7 millones por año de 2026 a 2038, y después 220,7 (2039), 85,2 (2040), 7,6 (2041) y 5,6 (2042). Los USD 266 millones a 12 meses son el tramo del 2026-12-31. Es el calendario de vencimientos anuales previsto por el Decreto 882 (art. 14: "vencimientos anuales determinados en función de los años de vigencia de los respectivos contratos"), no un pago comprometido.
- **Qué no encontré:** ninguna fuente dice que un generador haya ejercido la opción de venta ni que se haya suspendido o pagado un tramo. Sin eso, la lectura normativa es que el tramo de 2026-12-31 vence y se cancela sin pago.

## 3. Base legal (tabla `tablas/emisiones_letras_en_garantia_foder_y_saldo_sigade.csv`)

- Ley 27.191 art. 7 (crea el FODER; inc. 5 d: avales y garantías para los contratos de CAMMESA). Decreto 882/2016 arts. 3, 4, 7 y 14 (opción de venta, causales, fiduciante y letras). Decreto 531/2016 Anexo I art. 7 (cargo y cuenta de garantía). Decreto 471/2017 art. 3 (suspensión y vencimiento anual).
- Emisiones: Resolución 147-E/2017 (Ministerio de Finanzas), VN USD 4.498,5 millones (Ronda 1: 1.765,5; Ronda 1.5: 1.895,6; contratos de la Res. MEyM 202-E/2016: 837,5). Resolución Conjunta 32/2018, VN USD 2.918,6 millones (Ronda 2). Suma: USD 7.417,1 millones, igual al stock de la OPC a septiembre de 2019.
- Contrato: Acuerdo de Adhesión modelo (Res. MEyM 202-E/2016, anexo) y Contrato de Fideicomiso del FODER del 2016-08-05.
- Las fechas de firma de SIGADE (2017-08-31 y 2018-12-21) coinciden con esas dos emisiones (56 letras por USD 2.415,8 millones y 53 por USD 1.358,0 millones; tabla `sigade_letras_en_garantia_por_prefijo_y_fecha_de_firma_2026-06-30.csv`).
- No cubre la ronda 3 ni MATER: ninguna fuente leída emite letras para ellas; las 109 letras de SIGADE encajan solo con las rondas 1, 1.5 y 2 por fecha de firma.

## 4. Diferencia con lo emitido

Se emitieron USD 7.417,1 millones y SIGADE tiene USD 3.773,7 millones (diferencia de USD 3.643,4 millones, cálculo). Ninguna fuente leída documenta qué tramos vencieron y se cancelaron en 2018 a 2025; es compatible con el vencimiento anual previsto, pero no lo probé.
