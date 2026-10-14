# Decisiones del investigador

Registro de las definiciones metodológicas que tomó Alejandro. Cada una indica la fecha, la fuente que la sostiene y cómo se aplica en el código.

## D-001. Reservas netas: definición del FMI (2026-10-14)

**Decisión.** El trabajo usa la definición de reservas internacionales netas del TMU del acuerdo EFF (FMI, Country Report 26/105, párr. 11, SRC-0312).

- Reservas brutas: activos líquidos del BCRA frente a no residentes en moneda convertible (BPM6).
- Se restan: pasivos en divisas con vencimiento original de hasta un año, compras netas al FMI desde el inicio del programa, forwards netos, swaps (PBOC, BIS, ESF), encajes en moneda extranjera, SEDESA, ALADI y depósitos de no residentes.
- **No se restan los depósitos en divisas del Tesoro en el BCRA.** Texto del TMU: "Neither the Federal government's foreign liabilities nor its FX deposits at the BCRA are considered as gross foreign liabilities of the BCRA."

**Fundamento.** Los encajes en divisas respaldan depósitos del sector privado, que puede retirarlos, y por eso se restan. Los depósitos del Tesoro son una acreencia dentro del sector público; al consolidar Tesoro y BCRA se cancelan, y las divisas quedan disponibles para quien las necesite.

**Aplicación.**
- Las series de reservas netas se calculan con esta definición. Toda otra definición que aparezca en fuentes o en la literatura se identifica por su nombre y no se mezcla con esta.
- Las divisas que el Tesoro perciba por derechos de exportación y deposite en el BCRA se cuentan una sola vez, como reservas. En la consolidación Tesoro + BCRA no se suman de nuevo como activo del Tesoro.
- En la presentación separada del Tesoro (perímetro del protocolo), esos depósitos sí figuran como activo en USD del Tesoro y como pasivo del BCRA.
