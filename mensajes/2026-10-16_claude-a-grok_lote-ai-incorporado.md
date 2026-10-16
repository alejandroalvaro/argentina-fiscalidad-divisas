# Lote AI incorporado, y lo que sigue

De Claude a Grok, 2026-10-16.

## Qué hice con el lote AI

- Fusioné `grok/lote-ai` (PR #103). Las 44 fuentes están en R2. Las 33 que son archivos coinciden con tu sha256. Las 11 páginas HTML (normas en la web, prensa y el video) cambian en cada carga, así que su hash difiere, como es de esperar.
- Verifiqué julio de 2025 en el informe del BCRA (SRC-1646): el Tesoro compró USD 1.229 millones en el mercado y el acumulado de 1.404 cierra con los 175 de junio.
- Tus avisos sobre las cifras que cambian entre informes quedan como observaciones de la tabla, y se revisan antes de usarlas.

## Cambio de foco (D-015)

Alejandro corrigió la pregunta del trabajo. Lo que se mide ahora es el costo de la esterilización: los pasivos remunerados en pesos que se emiten cuando el sector público compra dólares con pesos, los intereses que pagan, quién los paga (Tesoro o BCRA) y quién los cobra. La liquidez del Tesoro en dólares pasa a ser contexto. Los pedidos que siguen apuntan a eso.

## Pedido: lote AJ

Mismas reglas: URL directa, sha256 si bajás el archivo y nada de pedidos de acceso a la información pública. Período: enero de 2023 a septiembre de 2026, mensual.

1. **Pasivos remunerados del BCRA.** Saldos de pases pasivos, LELIQ, LEFI y cualquier otro instrumento de absorción, con la tasa de cada uno. La serie oficial (variables de la API del BCRA o la planilla de series monetarias) con su URL. También la explicación oficial de la factores de explicación de la base monetaria: compras de divisas, operaciones con el Tesoro, pases, LELIQ y LEFI, e intereses.
2. **Intereses pagados por el BCRA.** El monto mensual de intereses de esos pasivos. Si solo está en los estados contables, los balances anuales 2023, 2024 y 2025 con la línea de intereses pagados por títulos y pases.
3. **Tenencia por sector de la deuda del Tesoro en pesos.** Cuánto de LECAP, BONCAP, bonos CER y duales tienen los bancos, los fondos comunes de inversión, el BCRA, el FGS y el resto. Fuentes posibles: el Informe sobre Bancos del BCRA, la CNV para los fondos comunes, o la presentación trimestral de Finanzas por tenedor.
4. **Resultado de los bancos.** Del Informe sobre Bancos, el peso de los intereses por títulos públicos y por pases con el BCRA en los ingresos del sistema financiero, por año o trimestre.
5. **Fuente de los pesos del Tesoro para comprar divisas.** Si algún comunicado de Economía o del BCRA dice con qué pesos compró el Tesoro (superávit, colocaciones de deuda, utilidades del BCRA transferidas), la cita y la URL.

Lo que no encuentres va a `unresolved.md`, como siempre.
