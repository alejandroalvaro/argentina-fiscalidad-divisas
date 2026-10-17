# 8. Método

Este capítulo describe cómo se hizo el trabajo, para que cualquiera pueda rehacer cada cifra y juzgar sus límites. El trabajo se hizo con agentes de inteligencia artificial bajo la dirección del investigador, en cuatro días de octubre de 2026. El método importa tanto como los resultados: es lo que permite que un trabajo de este volumen sea verificable.

## 8.1 Roles

- **El investigador** define la pregunta, toma las decisiones de método y revisa. Las decisiones están registradas, con fecha y fundamento, de D-001 a D-017 (`docs/DECISIONES.md`).
- **Un primer modelo (GPT)** diseñó el protocolo de investigación y de auditoría (`docs/protocolo/`): la pregunta, las hipótesis, las fuentes prioritarias y diez controles que cada cambio tiene que pasar.
- **Un agente de búsqueda (Grok)** encuentra las fuentes y arma lotes: la lista de fuentes con su URL oficial, las afirmaciones con la cita textual y la página, las tablas extraídas, una síntesis y un registro de lo que no encontró. Entrega cada lote en una rama de GitHub y no tiene acceso al almacenamiento de los originales. No presenta pedidos de acceso a la información pública.
- **Un agente de código (Claude Code)** baja cada documento desde la URL oficial, calcula su huella sha256, lo guarda, valida el lote, coteja contra el original las cifras que se van a usar, escribe el código que calcula y fusiona el lote solo si pasa las pruebas.

Los dos agentes se comunicaron por escrito, en 134 mensajes guardados en el repositorio (`mensajes/`), sin intervención del investigador salvo en las decisiones de método.

## 8.2 Los originales

Cada documento que sostiene una cifra se guarda una sola vez, sin modificar, en un almacenamiento de objetos, con su huella sha256 como nombre. Si dos fuentes entregan el mismo archivo, se guarda una vez. Si una fuente cambia el archivo, la huella cambia y se guarda la nueva versión al lado de la vieja. Los manifiestos del repositorio registran, para cada fuente, la URL, la fecha de descarga, el código de respuesta, el tamaño y la huella, y si coincide con la que calculó el agente de búsqueda.

Al cierre de este borrador había 1.198 originales guardados. Algunas fuentes no se pudieron guardar porque el portal bloquea la descarga automática (ANSES y el FMI, capítulo 7); en esos casos se usó la lectura web, y se indica.

## 8.3 Validación y verificación

Cada lote pasa por un validador que revisa los esquemas de las tablas, los identificadores, las referencias cruzadas entre fuentes, afirmaciones e instrumentos y los duplicados. Un lote que no pasa no se fusiona.

La validación no garantiza que las cifras sean correctas. Para eso, el agente de código coteja contra el documento original cada cifra que va a usar en un cálculo. Los resultados de esas verificaciones están en los mensajes y en `docs/verificaciones/`. Las 1.404 afirmaciones de los lotes siguen marcadas como "sin revisar" en sus tablas, porque la verificación se hizo sobre las que se usan y no sobre todas.

## 8.4 Cálculo

Todo cálculo es código, con pruebas, y nunca texto de un modelo de lenguaje. El modelo de lenguaje escribe el informe; no calcula.

- **El motor contractual** (fase 2) arma el calendario de pagos instrumento por instrumento con sus condiciones de emisión: cupones, amortizaciones, capitalización, ajuste por CER con su rezago, tasas TAMAR y BADLAR (la de los plazos fijos de más de un millón de pesos), duales que pagan la mayor de dos ramas. Cada flujo guarda por separado la moneda en que está escrito, la indexación, la moneda en que se paga y el tenedor.
- **La conciliación** (fase 3) contrasta el inventario con la planilla oficial, descuenta los pagos a organismos del propio sector público y reconstruye el interés que se devenga y no se paga.
- **Los diagramas de flujos** del mandato combinan el esquema ahorro-inversión-financiamiento, el boletín de Finanzas, el balance cambiario y los factores de la base monetaria. Cada línea se neta en la ventana, y cada diagrama tiene que cerrar: lo que entra es igual a lo que sale, y la diferencia que queda se muestra con nombre propio.

Las pruebas automáticas (88 al cierre) fijan las propiedades que no se pueden romper: que los diagramas cierren, que la deuda dólar linked no cuente como necesidad de dólares, que un dato que falta quede vacío. El código solo se fusiona si pasan todas.

## 8.5 Reglas que no se negocian

- Un dato que falta queda vacío. Nunca se completa con cero.
- La moneda en que está escrita una deuda, su indexación, la moneda en que se paga y el tenedor van en campos separados.
- Los datos observados, los términos contractuales, los escenarios y los supuestos van en tablas separadas.
- Las reservas netas siguen la definición del acuerdo con el FMI (D-001).
- El Tesoro, el BCRA y el sector público consolidado se presentan por separado, sin contar dos veces lo que una parte del Estado le debe a otra.
- Los pesos se informan en pesos y los dólares en dólares (D-017).
- Cada salida informa su corte, su fuente y su versión.

## 8.6 Conciliaciones que cierran

| Control | Resultado |
|---|---|
| Saldo de SIGADE contra la planilla de Finanzas al 30-06-2026 | 471.690 millones de USD en las dos, sin diferencia |
| Identidades de flujos del segundo trimestre de 2026 | Cierran al dólar |
| Perfil oficial de vencimientos a doce meses | Reproducido en sus 24 casillas |
| Calendario del motor contra el perfil oficial | Diferencia de 32.913 millones de capital explicada sin residuo |
| Mercado de cambios del mandato | 493.513 millones de USD de cada lado |
| Tesoro en dólares | Cierra; diferencia entre monedas de 3.522 millones a la vista |
| Sector público nacional en pesos | Cierra con $214.000 millones de redondeo |
| BCRA en pesos | Cierra exacto contra la variación de la base |
| Utilidades del BCRA | Iguales en la planilla del BCRA y en la de Hacienda ($42,9 billones) |

## 8.7 Cómo reproducir

El repositorio contiene el código, las pruebas, los manifiestos y las tablas chicas. Los originales están en el almacenamiento, identificados por su huella.

```
make install && make check
uv run argfx fetch <sha256> <destino>   # cualquier original por su huella
uv run argfx calendario                 # calendario de pagos (capítulo 2)
uv run argfx conciliacion               # consolidación y controles (capítulo 2)
uv run argfx devengados                 # interés capitalizado (capítulo 3)
uv run argfx flujos                     # los cuatro diagramas del mandato
uv run argfx derechos                   # derechos de exportación (anexo A)
uv run argfx simular                    # el modelo de la fase 4 (anexo A)
uv run argfx graficos                   # los gráficos de barras
python scripts/build_informe.py --docx  # este informe en HTML y en Word
```

## 8.8 Límites

- La verificación contra el original se hizo sobre las cifras que se usan, no sobre todas las afirmaciones reunidas.
- Algunas fuentes son lecturas web sin huella guardada.
- Hay estimaciones propias, rotuladas en cada caso: el interés devengado de las LEFI, la parte del TDE25 que el BCRA convirtió sin pago, el reparto proporcional de la tenencia del sector público y las conversiones de tipo de cambio.
- La diferencia sin explicar del Tesoro en dólares, 3.522 millones, se atribuye a desfasajes de calendario y de registro, sin poder probarlo mes a mes.
- El stock se mide al 30 de junio de 2026, con las operaciones posteriores hasta el 16 de octubre; los flujos llegan hasta agosto de 2026.
- Los agentes se equivocan. El capítulo 7 lista los errores que la verificación encontró. Los que no encontró son el límite principal de este trabajo, y la razón de que todo sea reproducible.
