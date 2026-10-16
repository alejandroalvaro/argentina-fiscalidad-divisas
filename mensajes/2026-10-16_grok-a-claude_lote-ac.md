# Nota de Grok a Claude: lote AC (rama `grok/lote-ac`), cartera del FGS por categoría en diciembre de 2024

Fecha: 2026-10-16. Todo en `inbox/lote-ac/`, `sin_revisar`. Fuente SRC-1319. Claim ids CLM-AC-001 a CLM-AC-006. Sin PR.

Alejandro me pidió buscar el PDF de diciembre de 2024 por otra vía antes de pedir nada por acceso a la información pública.

## Lo que conseguí

El Informe Estadístico Mensual de diciembre de 2024 sigue sin aparecer (detalle de vías y códigos en `unresolved.md`). Encontré el **Informe Anual del FGS 2024** de ANSES (`.../inline-files/Anuario%202024.pdf`, leído con el lector web), cuyo Cuadro 4 trae la tabla de títulos públicos nacionales por categoría en millones de pesos para dic-23, mar, jun, sep y dic de 2024. Con eso queda completa la serie trimestral de marzo de 2024 a junio de 2026.

Diciembre de 2024 (millones de pesos): CER 37.581.175; USD tasa fija 10.537.433; Dólar-linked 4.665.598; Letras $ 1.218.491; Bonos $ tasa fija 1.150.155; Letras USD 1.122.361; PBI € 169.218; PBI USD 151.244; BADLAR 34.359; PBI $ 1.377; total 56.631.411 (las diez suman el total). La tabla está en `tablas/fgs_titulos_publicos_por_categoria_dic_2024_lectura_web.csv`, en el mismo formato que la de lote AB.

## Cuidados

1. **La fila CER probablemente incluye garantizados y Cuasipar.** El Cuadro 1 da garantizados 401.427 y Cuasipar 8.735.199; el Cuadro 4 suma el total completo. Los informes mensuales de 2026 los separan. Para comparar, 37.581.175 menos 9.136.626 da 28.444.549. Es una inferencia por suma.
2. **Corrección al lote AB:** "Bonos, $, tasa fija" aparece en diciembre de 2024, no en marzo de 2025.
3. **Control cruzado:** marzo, junio y septiembre de 2024 del anual coinciden cifra por cifra con las filas del lote AB.
4. **LELINK:** el anual tampoco trae nota de clasificación.
5. Es lectura web, no el original; la transcripción de los Cuadros 1, 4 y 5 queda en `inbox/lote-ac/fuentes/` con sha256, como archivo derivado.

## Pregunta

Queda pendiente solo la clasificación de las LELINK y el mensual exacto de diciembre de 2024. Si querés cerrar eso, el camino es el pedido por acceso a la información pública, que Alejandro decide.
