# Síntesis, lote AC: cartera del FGS por categoría al cierre de diciembre de 2024

Todo `sin_revisar`. Fuente única nueva: SRC-1319, Informe Anual del FGS 2024 de ANSES (lectura web; el PDF no se pudo bajar).

## Resultado

El Informe Estadístico Mensual de diciembre de 2024 no apareció por ninguna vía. Lo que sí apareció es el **Informe Anual del FGS 2024** (ANSES, Subdirección Ejecutiva de Operación del FGS), que en su Cuadro 4 trae la misma tabla de títulos públicos nacionales por categoría, en millones de pesos, para diciembre de 2023 y para marzo, junio, septiembre y diciembre de 2024. La fila de diciembre de 2024 queda así (millones de pesos):

| Categoría | dic-24 | % del total de títulos |
|---|---|---|
| Bonos, $, tasa variable (CER) | 37.581.175 | 66,4% |
| Bonos, USD, tasa fija | 10.537.433 | 18,6% |
| Bonos, $, tasa variable (Dólar-linked) | 4.665.598 | 8,2% |
| Letras, $ | 1.218.491 | 2,2% |
| Bonos, $, tasa fija | 1.150.155 | 2,0% |
| Letras, USD | 1.122.361 | 2,0% |
| Bonos, €, tasa variable (PBI) | 169.218 | 0,3% |
| Bonos, USD, tasa variable (PBI) | 151.244 | 0,3% |
| Bonos, $, tasa variable (BADLAR) | 34.359 | 0,1% |
| Bonos, $, tasa variable (PBI) | 1.377 | 0,002% |
| **Total títulos públicos nacionales** | **56.631.411** | 100% |

Las diez categorías suman exactamente el total. Marzo, junio y septiembre de 2024 de ese cuadro coinciden cifra por cifra con las filas del lote AB, lo que valida la lectura.

## Lo que hay que saber antes de usarlo

1. **No es el mensual.** Es el informe anual, que usa la misma clasificación pero abre el total completo de títulos por categoría. Los informes mensuales recientes (por ejemplo julio de 2026) separan "Bonos públicos garantizados" y "Bonos Cuasipar" del bloque sujeto al límite del art. 74. En diciembre de 2024 los garantizados suman 401.427 y el Cuasipar 8.735.199 (Cuadro 1). Como el Cuadro 4 suma 56.631.411, igual al total con ambos, la fila CER (37.581.175) probablemente los incluye. Por eso, para comparar con filas de 2025 y 2026 que sí los separan, hay que restar esos dos montos de la fila CER: 37.581.175 menos 9.136.626 da 28.444.549 de CER en el bloque sujeto al límite. Es una inferencia por suma, no una nota del informe (CLM-AC-005).
2. **Bonos, $, tasa fija aparece en diciembre de 2024** (1.150.155), no en marzo de 2025 como decía la nota del lote AB (CLM-AC-003).
3. **Letras por moneda (Cuadro 5):** letras en pesos 1.218.491 y letras en dólares 1.122.361, sin cambio de criterio respecto de septiembre de 2024 (2.226.171 y 1.051.362).
4. **LELINK:** el Informe Anual 2024 tampoco trae nota de clasificación. La pregunta sigue abierta (CLM-AC-006).
5. **Fuente de segunda mano.** Es lectura web de un PDF que ANSES bloquea con 403. Se guarda la transcripción de los Cuadros 1, 4 y 5 con su sha256, marcada como derivada.

## Para la serie

Con esto la serie trimestral por categoría queda completa de marzo de 2024 a junio de 2026 (diez cierres), con la salvedad del punto 1 para diciembre de 2024. Falta, si se quiere el mensual exacto, el PDF del IEM de diciembre de 2024 (ver `unresolved.md`).
