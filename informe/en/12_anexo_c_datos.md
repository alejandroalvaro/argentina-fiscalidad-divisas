# Annex C. Data

## C.1 Main sources

| Source | What it provides | Identifier | Chapters |
|---|---|---|---|
| SIGADE at 30-06-2026, Oficina Nacional de Crédito Público (National Public Credit Office) | Every debt operation of the Central Administration | SRC-0102 | 2 |
| Quarterly debt workbook, Secretaría de Finanzas (Finance Secretariat) | Official balances, flows and maturity profile | SRC-0103, SRC-1005 | 2, 8 |
| Monthly bulletin of the Finance Secretariat, 2019-2026 series | Debt by currency (A.1, A.3), operations (A.4) and payments by currency of payment (A.5) | SRC-9002 | 2, 3, 5 |
| Central Administration debt by holder | Public sector, private holders and international organizations | SRC-1014, SRC-1706 to SRC-1715 | 2, 6 |
| Savings-investment-financing (AIF) table, cash basis, Secretaría de Hacienda (Budget Secretariat) | Revenue, spending, balance and financing of the national public sector | batches AM and AN | 3, 5 |
| FX balance (balance cambiario), BCRA | Foreign-currency purchases and sales by item and by sector | SRC-1604 | 2 and 4 |
| Series.xlsm, BCRA | Monetary base factors and BCRA instruments | SRC-1625 | 3 |
| BCRA financial statements 2023 to 2025 | Interest paid and received, profits | SRC-1673 and following | 3, 6 |
| Informe sobre Bancos (banking report), BCRA | Results of the financial system | batch AJ | 6 |
| IMF staff reports, 2025 agreement and reviews | Net reserve targets and outcomes, disbursements | SRC-1263, SRC-1270, SRC-1271, SRC-1611 | 4 |
| Joint resolutions of the Finance and Budget Secretariats | Buybacks, exchanges and conversions | SRC-1257, SRC-2031, SRC-2042, SRC-2047, SRC-2063, SRC-2064 | 5, 6 |
| Treasury foreign-currency purchases (BCRA reports and press releases) | Purchases from the BCRA and in the market | batch AI | 5 |
| Auctions and dollar-denominated debt paid in pesos | Placements and peso payments of dollar debt | batches AQ and AR | 5, 7 |
| Monthly export zip files, ARCA (tax and customs agency) | FOB value by tariff line | SRC-1375 to SRC-1491 | Annex A |
| Export duty revenue, datos.gob.ar | Duties collected | batch D | Annex A |
| National CPI, INDEC | Peso deflator | SRC-2028 | 3, 5 |
| Comunicación A 3500, BCRA | Reference exchange rate | `series/bcra_a3500.csv` | all |

A batch is a delivery from the search agent, stored in the repository folder `inbox/lote-…` with its list of sources, its tables and its notes. The full list of sources, with URL, download date and SHA-256 hash, is in `manifests/downloads.csv` and in each batch's `sources.csv`.

## C.2 Outputs that support the report

| Output | Command | File |
|---|---|---|
| Payment schedule and foreign-currency needs | `argfx calendario` | `data/calendario/` |
| Reconciliation, consolidation and holdings | `argfx conciliacion` | `data/conciliacion/` |
| Capitalized interest by quarter | `argfx devengados` | `data/conciliacion/devengados_trimestral.csv` |
| Diagrams for the term | `argfx flujos` | `data/informe/flujos_*.csv` and `.html` |
| Estimated and collected duties | `argfx derechos` | `data/simulacion/derechos_*.csv` |
| Phase 4 model: the term with collection in dollars and the projection to 2036 | `argfx simular` | `data/simulacion/mandato_*` and `proyeccion_*` |
| Bar charts | `argfx graficos` | `data/informe/grafico_*.csv` and `.html` |
| The whole dollar account (chapter 2.6) | `argfx demanda` | `data/informe/demanda_divisas_observada.csv` and `cuenta_anual_divisas.csv` |
| IMF projection of the trade balance | | `series/fmi_balanza_proyectada.csv` (SRC-1263) |
| IMF projection of the balance of payments | | `series/fmi_cuenta_corriente_proyectada.csv` (SRC-1263) |

All outputs of this version were regenerated on 17 October 2026 from version `57a7c62` of the repository.

## C.3 Method decisions

The researcher's decisions are in `docs/DECISIONES.md`, with date and rationale. The ones that weigh most in this report are:

- **D-001.** Net reserves follow the definition in the IMF agreement, without subtracting Treasury deposits.
- **D-008.** The analysis includes operations after the SIGADE cut-off.
- **D-009.** Interest is also measured on an accrual basis.
- **D-011.** The FODER guarantee notes are contingent debt.
- **D-016.** The report deals with the bimonetary nature of the debt; collection in dollars moves to an annex.
- **D-017.** Each currency in its own unit, charts by currency and a glossary.
- **D-018.** The assumptions of the phase 4 model run.

## C.4 How to verify a figure

Everything that supports this report is public:

- **The repository**, with the code, the tests, the manifests, the tables of each batch, the method decisions and the messages between the agents, with its full history: https://github.com/alejandroalvaro/argentina-fiscalidad-divisas
- **The official original documents**, as downloaded, at https://datos.8kgm.com.br. Each original is in `objects/sha256/` followed by its hash. The table `manifests/publicacion.csv` gives, for each SRC code, the issuer, the source URL, the hash and the public address.
- **Third-party documents** (press articles, academic papers, reports by private business chambers and copies of official texts hosted on third-party sites), 140 of 1,214, are not reproduced because their rights belong to their authors. The same table gives their source URL and their hash, so that anyone who downloads them can check that it is the same file.

To check an original, it is enough to download it and compute its hash (`shasum -a 256 archivo` on macOS or Linux, `certutil -hashfile archivo SHA256` on Windows): it has to match the object's name. To redo a calculation, the repository explains how to install the code and which command produces each output (section C.2).

The code is distributed under the MIT license, and the texts and own tables under the Creative Commons Attribution 4.0 license (CC BY 4.0). The original documents remain the property of their issuers.
