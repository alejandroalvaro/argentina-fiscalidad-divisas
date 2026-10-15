# Pendientes del lote I4

Lote I4: tabla de ramas de los bonos duales TXMD8, TXMD9 y TMVE8 pedida por Claude en la nota del lote I3 (`tablas/duales_ramas.csv`, una fila por rama). No hay cambios en `contratos/`. Todo `sin_revisar`.

1. **Fórmulas transcriptas de imágenes.** Los textos de las RC 32 y 46 traen las fórmulas de VPV y de TAMAR TEM como imágenes. Se transcribieron a mano de las imágenes (guardadas como originales SRC-0918 a SRC-0922). Hay que verificar la transcripción contra los originales en R2.
2. **Margen del 3% de TXMD8 y TXMD9.** El texto dice "más un margen del tres por ciento"; la imagen de TAMAR TEM lo pone dentro del numerador (TAMAR + 3%), es decir, sumado a la TAMAR anual antes de pasar a tasa efectiva mensual. Se cargó como lo muestra la imagen.
3. **Base del factor de TMVE8.** La fórmula VPV = VNO x (...) de la rama ii) de TMVE8 usa la sigla VNO sin aclarar moneda; la lectura literal del texto es que se aplica sobre el VNO en USD convertido a pesos al tipo de cambio inicial. Confirmar con Finanzas o con un caso publicado.
4. **Ventana de la TAMAR.** La TAMAR es el promedio aritmético simple de la serie publicada por el BCRA desde diez días hábiles antes de la emisión hasta diez días hábiles antes del vencimiento; la serie diaria usada no está cargada en el repositorio (los escenarios de TAMAR futura son una definición del motor).
5. **Bono dual de 2030.** La RC 32 art. 5 emite también el BONO CER/TAMAR 2030 (vto 2030-06-28), que no se pidió y no está cargado; si el motor de duales lo necesita, su texto está en SRC-0910.
6. **Pendientes que no cambian:** montos de las conversiones con el BCRA de las RC 39 (BONCER), 51, 53 (LECAP) y 60 sin circulación publicada, y SIGADE al 30-09-2026.
