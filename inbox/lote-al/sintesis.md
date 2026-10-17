# Lote AL: carteras de fondos (CNV), costo de fondeo bancario y informes del FGS faltantes

Fecha de acceso: 2026-10-16. Fuentes SRC-1908 a SRC-1988 (el pedido hablaba de SRC desde 1771, pero main ya usa hasta SRC-1907, así que arranqué en 1908). Claims CLM-AL-001 a CLM-AL-076. Todo en millones de pesos corrientes de cada fecha, salvo que se indique otra cosa.

## 1. Muestra de carteras de FCI (CNV)

Tablas: `tablas/cnv_fci_muestra_carteras_por_instrumento.csv` (40 filas, 10 fondos por fecha), `tablas/cnv_fci_universo_y_ranking_por_patrimonio.csv` (los 72 fondo-fecha relevados, con el sha256 de cada html) y `tablas/cnv_fci_muestra_detalle_de_especies.csv` (cada especie con su categoría, para auditar la clasificación).

Método. De cada página de detalle de la CNV (`DetallesFCI/<id>?fecha=...`) tomé el patrimonio neto (P.N.) y los porcentajes del P.N. por especie; los montos son porcentaje por P.N. Las fechas son la última cartera semanal publicada a la fecha pedida: 29-12-2023, 27-12-2024, 26-12-2025 y 28-08-2026.

Resultados (agregado de los cinco mayores de cada grupo, en % de su P.N. conjunto):

- Mercado de dinero: el P.N. conjunto de los cinco mayores pasó de $7,4 billones (dic 2023) a $17,8 (dic 2024), $24,2 (dic 2025) y $30,1 billones (ago 2026). No tienen LECAP, BONCAP ni CER en cartera en ninguna de las cuatro fechas: son plazo fijo (13% en 2023, 56% en 2024, 53% en 2025, 61% en 2026), cauciones (3,5%, 9,3%, 17,4%, 10,2%) y disponibilidades (80,5% en 2023, cerca de 29% después).
- Renta fija T+1: el universo relevado son cinco fondos, que son todos los de la muestra. P.N. conjunto de $0,35 billones (2023), $2,0, $2,1 y $3,7 billones (ago 2026). Composición en 2023: CER 42%, duales 18%. En dic 2024: LECAP 65%, CER 16%. En dic 2025: BONCAP 23%, CER 22%, LECAP 16%, plazo fijo 18%, duales 8%. En ago 2026: CER 37%, LECAP 32%, TAMAR 9%, plazo fijo 11%.

Lectura para el costo de esterilización: lo que los fondos de mercado de dinero financian es en esencia bancos (plazos fijos) y mercado de cauciones, no deuda del Tesoro; el Tesoro en pesos está en los fondos T+1.

Limitaciones que importan:
- El universo no sale de un ranking oficial por fecha. La API de la CAFCI devuelve 403 y los resúmenes mensuales no traen P.N. por fondo. Armé el universo (13 fondos de mercado de dinero y 5 T+1) con un ranking de terceros (fonditos.ar sobre datos de la CAFCI, consultado el 15-10-2026, no guardado) y después ordené por P.N. oficial de la CNV. Un fondo grande que no esté en el universo podría desplazar al quinto, sobre todo en 2023.
- "T+1" lo tomé de la categoría CAFCI que informa ese ranking de terceros; la CNV los muestra como "Renta Fija" sin ese dato.
- "Fin de diciembre" es la última cartera semanal publicada antes del 31-12 (27-12-2024 y 26-12-2025).
- La clasificación por instrumento es mía, por ticker y nombre (media confianza, no oficial). `otros_titulos_de_deuda` incluye ON, fideicomisos financieros, pagarés, cheques, deuda provincial y municipal y cuotapartes de otros FCI. `otros_y_pasivos_netos` es el residuo contra 100% y puede ser negativo por pasivos. 
- Los porcentajes de la CNV vienen redondeados a dos decimales: los montos tienen ese error.

## 2. Costo de fondeo bancario

Tabla: `tablas/costo_de_fondeo_bancario_mensual_2023_2026.csv` (sistema financiero y bancos privados, enero 2023 a agosto 2026).

El Informe sobre Bancos no publica la tasa promedio pagada en plazo fijo ni los intereses pagados por cuentas a la vista. Publica el total "Egresos por intereses" y los saldos de depósitos por tipo. Con eso armé:
- Tasas promedio mensuales de la API del BCRA como proxy de lo que pagan los bancos: depósitos a 30 días (var. 12), BADLAR (7), TM20 (8) y TAMAR (44, desde oct 2024). Por ejemplo, depósitos a 30 días: 120,4% en dic 2023, 32,2% en dic 2024, 25,7% en dic 2025, 21,2% promedio de ago 2026.
- Saldos de depósitos del sector privado a fin de mes en cuenta corriente, caja de ahorros y plazo fijo, y el total, tal como los informa el anexo.
- Egresos por intereses del mes en pesos de agosto de 2026 (signo negativo, como en el anexo).
- Estimación propia del costo implícito: egresos anualizados sobre depósitos totales promedio del mes, deflactados con la inflación mensual del BCRA (var. 27). Da 68,5% en dic 2023, 18,2% en dic 2024, 16,3% en dic 2025 y 12,9% en ago 2026 para el sistema. Es cota superior del costo de depósitos porque el egreso incluye otros pasivos, y está diluido por los depósitos que no pagan interés (cuenta corriente y parte de las cajas de ahorro). Para pasar de resultados brutos a margen sirve el egreso real; para una tasa por producto, la serie 12.

## 3. Informes del FGS faltantes

Encontrados vía lector web (la descarga directa da 403 por Incapsula, sin sha256):
- Diciembre 2024: `https://www.anses.gob.ar/sites/default/files/inline-files/IEM-FGS-202412.pdf` (nombre distinto del patrón FGS.AAAA.MM que fallaba). Total $76.904.935,7 millones.
- Marzo y junio de 2023: informes trimestrales `FGS%20-%20I.TRIM_.23.pdf` y `FGS%20-%20II.TRIM_.23.pdf`, con la apertura de títulos públicos por categoría.
- 2023 mes a mes: el Informe Anual 2023 (`Anuario_2023.pdf`) trae en el Anexo I la cartera por rubro de los doce cierres de 2023.

Tablas: `tablas/fgs_cartera_por_rubro_cierres_mensuales_2023_y_dic2024.csv` y `tablas/fgs_titulos_publicos_por_categoria_mar_jun_2023_y_dic_2024.csv`. Dato relevante: a dic 2024 el FGS tenía $1,2 billones en letras en pesos y $37,6 billones en bonos CER (66% de sus títulos), y cero en fondos Money Market (había $47.688 millones en dic 2023).

Las letras en pesos del FGS fueron mínimas en 2023 (de $65.047 millones en marzo a $21.098 millones en diciembre).

Huecos en `unresolved.md`.
