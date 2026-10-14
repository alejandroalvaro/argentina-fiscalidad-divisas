# Encargos para Claude Code — infraestructura reproducible

## Fase 0
Crear repositorio Python 3.11+ con `pyproject.toml`, `src/`, `tests/`, `schemas/`, `scripts/`, `docs/`, `manifests/`, `.gitignore`, `.env.example`, README y Makefile. No subir documentos originales, parquet voluminoso, DuckDB, credenciales o logs sensibles a Git. Adoptar DuckDB + Parquet + almacenamiento S3 compatible (R2), con rutas locales configurables y funcionamiento offline para tests.

## Fase 1 — ingesta
Validar formatos Grok con Pydantic/Pandera; deduplicar por SHA-256 de documento e identificador de instrumento; registrar fuente, versión, fecha de corte, trazabilidad de extracción, error y revisión. Mantener objetos originales inmutables. Crear manifiestos versionados en Git que apunten a objetos por hash.

## Fase 2 — motor contractual
Modelar moneda de cuenta, indexación, liquidación, emisor, acreedor y residencia por separado. Generar cupones, amortizaciones, capitalización de intereses, tasas flotantes y opciones con módulos especializados. Mantener obligaciones contractuales firmes separadas de escenarios y deuda contingente. Salida mensual hasta 36 meses y anual hasta 20 años.

## Fase 3 — reconciliación
Pruebas: saldo inicial + emisiones + capitalizaciones - amortizaciones +/- ajustes = saldo final; conciliación de saldos con series oficiales; no doble conteo intra-sector público; pasivos dólar-linked pagaderos en ARS fuera de necesidad contractual de USD; conservación de activos/pasivos en matrices SFC. Emitir reporte de diferencias con materialidad configurable.

## Fase 4 — simulación
Implementar tres regímenes con igual carga tributaria inicial: (1) cobro en ARS y compras FX; (2) cobro directo USD; (3) cobro USD con fondo de estabilización. Incluir demanda de pesos, decisiones de esterilización, precio/cantidad exportada, shocks, calendario de deuda y maduración de inversión. No codificar superioridad de escenario en supuestos.

## Fase 5 — escritura
Manuscrito en Markdown y exportaciones reproducibles. Integrar las skills de estilo del autor únicamente en capa de redacción, nunca en extracción o cálculo. Registrar código, versiones de datos, parámetros y fecha de corte de cada gráfico y tabla.

## Seguridad y costo
Credenciales sólo en entorno local o secretos CI, permisos mínimos R2; bucket privado. Evitar descargas reiteradas usando caché por hash; agrupar consultas; no consumir API LLM para cálculo determinístico. No publicar documentos con licencias restrictivas sin revisión.
