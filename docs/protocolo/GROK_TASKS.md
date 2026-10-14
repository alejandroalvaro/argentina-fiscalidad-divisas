# Encargos para Grok — investigación documental

No redactar conclusiones definitivas ni inventar datos. Entregar lotes por tema, cada uno con `sources.csv`, `claims.csv`, `documents_manifest.csv`, `unresolved.md` y una síntesis breve.

## Lote A — marco conceptual
SFC abierto, jerarquía monetaria, restricción externa, tesorería en divisas, asset-liability management soberano, fondos de estabilización, riesgos de deuda indexada, literatura argentina relevante. Distinguir precedentes de aportes propuestos.

## Lote B — régimen legal argentino
Régimen de retenciones, moneda de determinación y pago, normas de liquidación cambiaria, cuentas del Tesoro en USD, facultades del BCRA, encajes, custodia externa y viabilidad de recaudación automática. Citar artículos y versiones vigentes; no asumir que permiso legal implica habilitación operativa.

## Lote C — inventario de obligaciones
Localizar inventarios oficiales y calendarios de deuda nacional. Catalogar familias: USD, ARS nominal, CER, dólar-linked, dual, tasa variable, multilaterales, bilaterales, garantías y contingencias. Priorizar descargas masivas oficiales y prospectos maestros; identificar ISIN y saldo vigente a fecha de corte. No confundir emisiones con saldo en circulación.

## Lote D — series externas
Exportaciones, derechos de exportación, reservas brutas y netas según definición, depósitos del Tesoro en BCRA, balanza de pagos, pagos de intereses, amortizaciones, cuentas de deuda por moneda y acreedor. Marcar cambios metodológicos.

## Lote E — Brasil comparativo
Series sintéticas de cuenta corriente, deuda por moneda, reservas, posición de inversión internacional y renta primaria; sin reconstrucción de cada título brasileño.

## Esquema mínimo de procedencia
Cada fuente: `source_id,issuer,title,url,publication_date,accessed_at,period_covered,document_type,sha256,license_notes,local_object_key`.
Cada afirmación: `claim_id,claim,source_id,page_or_section,exact_evidence,confidence,review_status`.
Cada instrumento candidato: `instrument_id,issuer,isin,currency_of_account,currency_of_payment,indexation,outstanding_principal,as_of_date,source_id,review_status`.

Entregar datos en UTF-8, CSV o JSONL, sin mezclar valores desconocidos con cero. Señalar contradicciones entre fuentes, no resolverlas por intuición.
