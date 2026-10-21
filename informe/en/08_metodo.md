# 8. Method

This chapter describes how the work was done, so that anyone can redo each figure and judge its limits. The work was carried out with artificial intelligence agents under the researcher's direction, over four days in October 2026. The method matters as much as the results: it is what makes a work of this size verifiable.

::: {.destacado custom-style="Destacado"}
**Every figure can be rebuilt from its source to its result.**

The more than 1,200 original documents are stored with their SHA-256 hash, every calculation is code with automated tests, and the balance of the 753 SIGADE operations matches the official workbook to the dollar.

*Scope.* Accounting closures, tests and SHA-256 hashes verify different things. The hash proves that the document is the one that was downloaded; the automated test, that the code does what it says; the accounting closure, that the accounts add up. None of them, on its own, guarantees that the economic interpretation is correct.
:::

## 8.1 Roles

- **The researcher** defines the question, takes the method decisions and reviews. The decisions are recorded, with date and rationale, from D-001 to D-019 (`docs/DECISIONES.md`).
- **A first model (GPT)** designed the research and audit protocol (`docs/protocolo/`): the question, the hypotheses, the priority sources and ten checks that every change has to pass.
- **A search agent (Grok)** finds the sources and assembles batches: the list of sources with their official URL, the claims with the verbatim quote and the page, the extracted tables, a summary and a log of what it did not find. It delivers each batch on a GitHub branch and has no access to the storage of the originals. It does not file freedom-of-information requests.
- **A coding agent (Claude Code)** downloads each document from the official URL, computes its SHA-256 hash, stores it, validates the batch, checks the figures to be used against the original, writes the code that does the calculations and merges the batch only if it passes the tests.

The two agents communicated in writing, in 134 messages stored in the repository (`mensajes/`), with no intervention from the researcher except on method decisions.

## 8.2 The originals

Each document that supports a figure is stored once, unmodified, in an object store, with its SHA-256 hash as its name. If two sources deliver the same file, it is stored once. If a source changes the file, the hash changes and the new version is stored next to the old one. The repository manifests record, for each source, the URL, the download date, the response code, the size and the hash, and whether it matches the one computed by the search agent.

When this version closed there were 1,214 stored originals. The 1,074 that are official documents can be downloaded from [datos.8kgm.com.br](https://datos.8kgm.com.br); the other 140, from third parties, are listed with their source URL and their hash. Annex C, section C.4, explains how to verify each one. Some sources could not be stored because the portal blocks automated downloads (ANSES and the IMF, chapter 7); in those cases the web reading was used, and this is indicated.

## 8.3 Validation and verification

Each batch goes through a validator that checks table schemas, identifiers, cross-references between sources, claims and instruments, and duplicates. A batch that fails is not merged.

Validation does not guarantee that the figures are correct, and neither does traceability. That a figure can be redone from its source shows that the calculation is the one the report declares; it does not show that the source measures what the report believes it measures, or that the economic reading is the right one. The error in the dollar purchases of the second draft, for example, was traceable end to end and was still wrong: it mixed two series that measure almost the same thing (chapter 7). For that reason, besides the tests, each draft goes through an external reading. To that end, the coding agent checks against the original document every figure it will use in a calculation. The results of those checks are in the messages and in `docs/verificaciones/`. The 1,404 claims in the batches remain marked as "unreviewed" in their tables, because verification covered the claims that are used, not all of them.

## 8.4 Calculation

Every calculation is code, with tests, and never text from a language model. The language model writes the report; it does not calculate.

- **The contract engine** (phase 2) builds the payment schedule instrument by instrument from its issuance terms: coupons, amortizations, capitalization, CER adjustment with its lag, TAMAR and BADLAR rates (BADLAR being the rate on fixed-term deposits of more than one million pesos), and duales that pay the higher of two legs. Each flow stores separately the currency of denomination, the indexation, the currency of payment and the holder.
- **The reconciliation** (phase 3) checks the inventory against the official workbook, nets out payments to entities within the public sector itself and rebuilds the interest that accrues and is not paid.
- **The flow diagrams** for the term combine the savings-investment-financing (AIF) table, the Finance Secretariat bulletin, the BCRA's FX balance (balance cambiario) and the monetary base factors. Each line is netted over the window, and every diagram has to close: what comes in equals what goes out, and any remaining difference is shown under its own name.

The automated tests (88 at the close) pin down the properties that cannot be broken: that the diagrams close, that dólar linked debt does not count as a dollar need, that a missing value stays empty. Code is merged only if all of them pass.

## 8.5 Non-negotiable rules

- A missing value stays empty. It is never filled with zero.
- The currency in which a debt is denominated, its indexation, the currency of payment and the holder go in separate fields.
- Observed data, contract terms, scenarios and assumptions go in separate tables.
- Net reserves follow the definition in the IMF agreement (D-001).
- The Treasury, the BCRA and the consolidated public sector are presented separately, without double counting what one part of the State owes another.
- Pesos are reported in pesos and dollars in dollars (D-017).
- Every output reports its cut-off date, its source and its version.

## 8.6 Reconciliations that close

| Check | Result |
|---|---|
| SIGADE balance against the Finance Secretariat workbook at 30-06-2026 | USD 471,690 million in both, no difference |
| Flow identities for the second quarter of 2026 | Close to the dollar |
| Official twelve-month maturity profile | Reproduced in all 24 cells |
| Engine schedule against the official profile | Difference of 32,913 million in principal explained with no residual |
| FX market over the term | USD 493,513 million on each side |
| Treasury in dollars | Closes; cross-currency difference of 4,309 million shown openly |
| National public sector in pesos | Closes with a rounding difference of ARS 214,000 million |
| BCRA in pesos | Closes exactly against the change in the monetary base |
| BCRA profits | Identical in the BCRA workbook and in the Budget Secretariat one (ARS 42.9 trillion) |

## 8.7 How to reproduce

The repository contains the code, the tests, the manifests and the small tables. The originals are in the object store, identified by their hash.

```
make install && make check
uv run argfx fetch <sha256> <destino>   # any original by its hash
uv run argfx calendario                 # payment schedule (chapter 2)
uv run argfx conciliacion               # consolidation and checks (chapter 2)
uv run argfx devengados                 # capitalized interest (chapter 3)
uv run argfx flujos                     # the four diagrams for the term
uv run argfx derechos                   # export duties (Annex A)
uv run argfx simular                    # the phase 4 model (Annex A)
uv run argfx graficos                   # the bar charts
python scripts/build_informe.py --docx  # this report in HTML and Word
```

## 8.8 Limits

- Verification against the original covered the figures that are used, not every claim collected.
- Some sources are web readings with no stored hash.
- There are own estimates, labeled in each case: the accrued interest on the LEFI, the part of the TDE25 that the BCRA converted without payment, the proportional allocation of public-sector holdings and the exchange-rate conversions.
- The unexplained difference in the Treasury's dollar accounts, 4,309 million, is attributed to timing and recording mismatches, without being able to prove it month by month.
- The stock is measured at 30 June 2026, with later operations up to 16 October; the flows run to August 2026.
- The agents make mistakes. Chapter 7 lists the errors that verification found. The ones it did not find are the main limit of this work, and the reason everything is reproducible.
