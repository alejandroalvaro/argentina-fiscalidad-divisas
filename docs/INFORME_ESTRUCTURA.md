# Estructura del informe final

Borrador del 17-10-2026, a partir de D-016. Ordena los capítulos y dice de dónde sale cada uno. Las cifras se escriben en la fase 5, a partir de las salidas del código.

## Idea central

La deuda pública argentina se mueve en dos circuitos. El de los pesos lo comandan el Tesoro y el BCRA, que pueden emitir, colocar y refinanciar en su propia moneda. El de los dólares lo comandan los exportadores, que traen las divisas, y los prestamistas, que las adelantan. Un superávit en pesos no paga una deuda en dólares: para eso alguien tiene que vender los dólares, y el Tesoro tiene que comprarlos con pesos. El caso argentino vale para cualquier economía periférica que comercia con el mundo en una moneda ajena.

## Capítulos

1. **Dos monedas, dos circuitos.** El planteo, el alcance y por qué medir cada moneda por separado. Brasil como contraste acotado.
2. **La deuda por moneda y por tenedor.** Los stocks separados por moneda de cuenta, indexación, moneda de pago y tenedor (sector público, organismos y privados), de 2024 a 2026, con la consolidación del sector público. Fuentes: fases 2 y 3, boletines y presentaciones de Finanzas.
3. **El circuito de los pesos.** Los pasivos remunerados y su traspaso del BCRA al Tesoro (pases y LELIQ, LEFI, LECAP y BONCAP), los intereses capitalizados que no aparecen en el resultado fiscal (D-009), y el superávit fiscal como fuente de pesos. Fuentes: lotes AJ, AK y AL, `argfx devengados`.
4. **El circuito de los dólares.** De dónde vienen y adónde van: exportaciones y derechos, liquidación, FMI y otros organismos, mercado, atesoramiento privado y reservas. La tabla de fuentes y usos desde la salida del cepo. Fuentes: balance cambiario del BCRA (lote AH), zips de ARCA, calendario de la fase 2.
5. **Donde se cruzan.** Las compras de dólares del Tesoro, al BCRA y en el mercado, la recompra de Letras Intransferibles con fondos del FMI y las necesidades en dólares de 2026 y 2027 frente a lo disponible. Fuentes: lote AI, programa financiero 2026-2027.
6. **Quién gana y quién pierde.** Quién se queda con los pesos (bancos, fondos comunes, FGS) y quién con los dólares (atesoramiento, acreedores, organismos), y quién paga (Tesoro, BCRA).
7. **La opacidad como dato.** Lo que costó reconstruir los dos circuitos: instrumentos, fuentes, series que no existen, cifras que cambian entre publicaciones y portales que bloquean la descarga.
8. **Método.** Protocolo, agentes, originales guardados por sha256, validación, conciliación, reglas y límites. Cómo reproducir cada cifra.

## Anexos

- **A. Cobrar los derechos de exportación en dólares.** La propuesta de Mosler (D-006), el costo de la esterilización (D-015) y la comparación de regímenes de la fase 4.
- **B. Brasil.** El contraste acotado.
- **C. Datos.** Inventario de fuentes, manifiestos y decisiones.
