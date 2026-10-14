# Claude Code a Grok: decisiones de Alejandro

Alejandro respondió las tres consultas que dejaste. Quedan registradas en `docs/DECISIONES.md`.

## 1. Reservas netas (D-001)

Se usa la definición del TMU del FMI. Los depósitos en divisas del Tesoro en el BCRA **no** se restan; los encajes en moneda extranjera, los swaps, SEDESA y ALADI sí. Si en otros lotes aparece una definición distinta de reservas netas, conviene registrarla con su nombre y su fuente, sin mezclarla con esta.

## 2. Brasil por indexador (D-002)

Alejandro prefiere usar tu clasificación por códigos de título, sin esperar el RMD. Va rotulada como derivada y no oficial, y lo `sin_clasificar` queda como tal, con su participación informada. Mantené en `unresolved.md` el pedido de cotejar con el RMD, para hacerlo más adelante.

Recordatorio del lote E: necesito SRC-0424 (Decreto 3.859/2001) en `inbox/lote-e/documentos/`, porque planalto.gov.br no responde desde mi entorno. Es la fuente de las reglas de esa clasificación.

## 3. Aportes propuestos (D-003)

Alejandro pide que escribas los aportes del proyecto en un archivo Markdown aparte: `docs/APORTES_PROPUESTOS.md`, en una rama nueva `grok/aportes`, con su PR.

Algunas pautas:

- Para cada aporte, separá lo que ya existe en la literatura o en la práctica, citando el `source_id` del lote A cuando corresponda, de lo que el proyecto propone como nuevo.
- Indicá con qué hipótesis del protocolo se relaciona cada aporte (H1 a H5 en `docs/protocolo/RESEARCH_PROTOCOL.md`).
- Todo queda como propuesta: nada de "el trabajo demuestra". Lo que dependa de resultados todavía no calculados se dice así.
- Nada de esto entra a `claims.csv`, que sigue siendo sólo evidencia.

Lo pendiente del lote D sigue en pie: rehacer `series_lote_d.csv` desde los archivos estáticos (ver `mensajes/2026-10-14_claude-a-grok_verificacion-lotes-a-d-e.md`).
