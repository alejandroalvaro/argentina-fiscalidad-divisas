# Verificación de SIGADE, lote C (corte 30/06/2026)

Fecha: 2026-10-14. Verificó: Claude Code. Para reproducir:

```bash
uv run python scripts/verify_sigade.py \
  46e2099d96f8dc22dae00a45b0ee4e9f8633ea0af39eecaa3e2e7350da5e28b5 inbox/lote-c/tablas_sigade \
  --xlsx e481f24585ef40b8ce7c2b515e66235c8b8ebcb4001a769091cb531a6373922e
```

## Procedencia

| Objeto | Fuente | SHA-256 | Coincide con Grok |
|---|---|---|---|
| Base SIGADE (.mdb en zip) | SRC-0102 | `46e2099d…` | Sí |
| Cuadros A.1 a A.4 (.xlsx) | SRC-0103 | `e481f245…` | Sí |

Los dos archivos se descargaron de nuevo desde argentina.gob.ar y están en R2.

## Resultados

1. **Exportaciones de Grok.** Las cinco tablas exportadas con `mdb-export` desde la base original son idénticas byte a byte a los CSV de `inbox/lote-c/tablas_sigade/` (753, 15.435, 1.036, 110 y 20 filas).
2. **`instruments.csv`.** Las 753 filas corresponden una a una con la tabla de saldos: nombre de la operación, moneda, saldo en moneda de origen, saldo en dólares, moneda de pago y fecha de firma.
3. **Unidad de medida.** SIGADE expresa los montos en **dólares**, y los cuadros de la planilla en **miles de dólares**. La suma de "Saldo en Dólares" es 471.689.788.348,40 USD, y el cuadro A.1.1 informa 471.689.788,348 miles de USD: coinciden. La síntesis del lote C y la afirmación CLM-C-003 describen los montos de SIGADE como miles de USD, y conviene corregirlo antes de usar `instruments.csv`.
4. **Saldo frente a vencimientos.** La suma del principal futuro de la tabla de vencimientos reproduce el saldo de cada operación, con una diferencia total de 25 USD concentrada en BCIE 2280 (27 USD). Al corte, el saldo de SIGADE es capital pendiente. Las 753 operaciones tienen calendario, que va de 2026 a 2089.
5. **Unidad de los instrumentos CER (UCP).** El tipo de cambio UCP (1,855623) es igual a ARP / CER (1.483,0198 / 799,2033). El saldo UCP está, entonces, en unidades de capital ajustable: multiplicado por el CER al corte (799,2033) da pesos corrientes. Resuelve la cuestión 3 del `unresolved.md` del lote C.
6. **Dólar-linked (DLK).** El tipo de cambio es 1 y la relación entre saldo en origen y saldo en dólares es exactamente 1 en las 8 operaciones. El saldo DLK está expresado en USD, aunque se paga en pesos. Resuelve la cuestión 4.
7. **Inconsistencias de códigos.** Se confirman las que señaló Grok: AED descrito como dólares (dos préstamos provinciales del Fondo Abu Dhabi), KWD descrito como euro (cinco préstamos del Fondo Kuwaití, con pago en EUR) y una operación XDR descrita como dólares (FIDA). No se corrigieron.

## Pendiente

- Validar el resto de los CSV de los lotes B y C contra esquemas (fase 1).
- Revisar la clasificación `instrument_family`: hay 43 instrumentos con indexación CER y 38 en la familia "ARS CER", y 8 dólar-linked frente a 7 en su familia. La diferencia parece venir de los duales, pero falta confirmarlo.
