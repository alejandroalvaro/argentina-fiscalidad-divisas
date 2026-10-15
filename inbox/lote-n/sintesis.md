# Lote N: síntesis (sin_revisar)

Rama `grok/lote-n`. Fuentes SRC-1020 a SRC-1047; claims CLM-N-001 a CLM-N-028; tablas en `tablas/`; huecos en `unresolved.md`. Los tres `contratos/*.csv` van solo con encabezado.

## Resultado

1. **Rezago del CER de Discount, Par y Cuasipar en pesos: diez días hábiles.** 21 avisos oficiales de pago (MAE, notas de la Dirección de Administración de la Deuda Pública) con la cifra "Variación del CER a aplicar" o "CER a aplicar". Dos avisos de Par dan las fechas de la división (13/03/2020 y 16/03/2021 sobre 16-12-2003). El CER del BCRA del décimo día hábil anterior al vencimiento dividido por 1,4551 reproduce la cifra de los 20 avisos verificados con diferencia relativa máxima de 5,5e-6; noveno día, undécimo o diez corridos no cuadran (mínimo 5,6e-4). La Resolución MAE C 1498 (2006) dice "10 días hábiles anteriores".
   - Valores a tener presentes: `indice_base` 1,4551 (CER del 2003-12-16 redondeado a cuatro decimales; sin redondear 1,45506393984) y `rezago_habiles` 10 para los tres instrumentos. La decisión de qué cargar en `terminos.csv` es de Claude.
   - Al 2026-06-30 el método del aviso da 543,94 y la valuación de Finanzas del lote M 548,60 (0,86% de diferencia).
2. **RC 53 y 60/2026 y SIGADE al 2026-09-30:** sin publicación nueva.

## Cómo leer las cifras

Las cifras de los avisos son datos publicados (cada claim los cita). Las comparaciones con el CER del BCRA son cálculo de Grok y están marcadas así. "Día hábil" se aproximó con los días de publicación del A3500.
