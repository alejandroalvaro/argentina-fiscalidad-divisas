# Grok a Claude Code: lote H, fondos de estabilización (rama `grok/lote-h-fondos`)

Todo está `sin_revisar`. El lote describe y no recomienda: las reglas del fondo del régimen (d) las decide Alejandro.

## Contenido
- `inbox/lote-h/`: 13 fuentes (SRC-0701 a SRC-0713), 29 claims (CLM-H-001 a CLM-H-029), manifiesto, `unresolved.md`, `sintesis.md`.
- `tablas/fondos_comparacion.csv` (5 filas): ingresos que acumula, regla de retiro, tope y quién decide, para Chile FEES, Noruega GPFG, Colombia FAE, Perú FEF y la referencia general.
- `tablas/opciones_diseno_fondo_d.csv` (18 filas): opciones por dimensión con sus precedentes y la cuestión que deja abierta, sin recomendación.
- Comparables de CLM-A-008: CLM-H-027 a CLM-H-029 sobre los Principios de Santiago (SRC-0206, ya en el lote A, sin duplicar el archivo).
- `docs/APORTES_PROPUESTOS.md`: aporte 6 y fila 6 de la tabla resumen con cuatro regímenes (se agregó la definición de (d) con D-007), y (d) en la columna de compatibilidad de la sección 8 y en el párrafo de compatibilidad.

## Límites
- Colombia: texto de la Ley 2056 tomado de leyes.co (no oficial), porque los sitios oficiales no respondieron. Confianza media en CLM-H-016 a CLM-H-019.
- Noruega: tres textos leídos con WebFetch (curl devolvió 403). Los `.txt` son transcripciones y su sha256 corresponde a la transcripción.
- Perú: no se calculó el saldo del FEF como porcentaje del PBI.
- Contradicción sin resolver: la nota 18 de los Principios de Santiago (2008) habla de un precio de referencia del cobre en Chile; los textos vigentes leídos no lo traen.
