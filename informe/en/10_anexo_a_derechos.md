# Annex A. Collecting export duties in dollars

This annex applies the two-circuit framework to a concrete proposal. The idea of collecting export duties directly in dollars comes from Warren Mosler, who presented it in Buenos Aires on 1 May 2022 ("A 3% export tax payable in $US", SRC-0212). This work contributes a formal version of it, measures its magnitudes with data from the term and sets out what changes and what does not.

The annex presents the proposal, its magnitudes over the term and the results of the phase 4 model, which compares the regimes using data from the term and a projection to 2036.

::: {.destacado custom-style="Destacado"}
**Collecting the duties in dollars changes how much foreign currency stays in the public sector and how much ends up in private hands, without creating new foreign currency.**

If the BCRA buys all the dollars that exporters sell in the FX market, collecting the duty in pesos or in dollars leaves the public sector with the same dollars and the same peso debt. When the BCRA does not buy, the difference shows up: given the purchases the BCRA actually made during the term, collection in dollars would have left about USD 11.9 billion more in the public sector.

*Scope.* This is a conditional counterfactual result. It changes a single thing and leaves everything else as it was: it does not include what exporters, dollar buyers or the exchange rate would have done. It is not an estimate of the additional reserves that would have been obtained.
:::

## A.1 The proposal and the regimes

Today the duty is assessed in dollars on the FOB value and paid in pesos. The exporter sells the foreign currency in the market, receives pesos and uses them to pay the duty. The proposal is that a fraction of the foreign currency, equal to the duty rate, goes directly to a Treasury dollar account.

The model compares four regimes with the same tax burden:

- **(a) Pesos**, the current regime.
- **(b) Brazil**: the exporter sells the foreign currency at the free rate and can keep it abroad (Annex B).
- **(c) Dollars**, Mosler's proposal: the fraction equal to the duty rate is paid in dollars to the Treasury.
- **(d) Dollars with a stabilization fund**: as in (c), but the foreign currency goes into a fund that transfers a fixed monthly sum to the Treasury, equal to one twelfth of the five-year average recalculated with the rates in force; the fund accumulates surpluses, covers shortfalls by formula and uses anything above twelve months of foreign-currency debt service to third parties to repay debt.

For the rest of the exporter's foreign currency, the baseline configuration is to sell it at a single exchange rate, with no split rates, with stable deadlines and predictable duty rates, because the expectation of a change is what delays FX settlements.

## A.2 What changes and what does not

If the exporter sells everything and the BCRA buys all the foreign currency, (a) and (c) end with the same reserves and the same monetary base in the consolidated public sector. In (a), the BCRA buys the dollars with pesos it issues, the exporter pays the duty with those pesos, and if the Treasury uses those same pesos to buy the dollars from the BCRA, the monetary base returns to where it was. In (c), the dollars go directly to the Treasury and no peso moves. The effect is the same; what changes is the pocket in which the dollars end up (BCRA or Treasury) and the sequence.

The difference appears when the sequence breaks, which is what chapters 3 and 5 show. The Treasury spends the pesos from the duty; the BCRA, so that those pesos do not put pressure on prices or the exchange rate, absorbs them with interest-bearing liabilities; and when the Treasury needs dollars, it raises other pesos, from a surplus or from debt, to buy them. Collecting in dollars saves the Treasury that route for the duty portion, but the Treasury still has to raise the pesos it no longer collects, because spending is the same. If it raises them with debt, the interest the BCRA used to pay is paid by the Treasury. The model measures the weight of each of these effects (sections A.4 to A.6).

## A.3 The magnitudes of the term

**Duties collected.** Between December 2023 and August 2026 the duties added up to about USD 17,079 million (ARS 28.6 trillion at August 2026 prices).

| Year | Duties collected | Treasury dollar purchases |
|---|---:|---:|
| 2023 (December) | 643 | 0 |
| 2024 | 6,565 | 15,641 |
| 2025 | 6,000 | 3,973 |
| 2026 (January to August) | 3,871 | 7,196 |
| **Total** | **17,079** | **26,810** |

*USD million. Duties: revenue (datos.gob.ar) converted to dollars at the monthly average A 3500 rate. Purchases: BCRA monthly report, including the February 2026 purchase (chapter 5).*

Collected in dollars, the duties of the term would have been equivalent to 64% of the dollars the Treasury bought with pesos. The relevant comparison is with the purchases, because the debt to the BCRA repaid with pesos did not give the Treasury dollars it could use (chapter 5). In 2025 they would have exceeded that year's purchases.

**The gap between estimated and collected.** The report estimates the duties tariff line by tariff line using ARCA (tax and customs agency) export files and the rates in force each month, including the hydrocarbons sliding formula.

| Year | Exports subject to a rate / total | Estimated | Collected | Collected / estimated |
|---|---:|---:|---:|---:|
| 2021 | 92.8% | 10,372 | 10,131 | 0.98 |
| 2022 | 94.3% | 12,113 | 12,511 | 1.03 |
| 2023 | 93.4% | 7,651 | 4,902 | 0.64 |
| 2024 | 93.6% | 9,144 | 6,565 | 0.72 |
| 2025 | 95.1% | 8,267 | 6,000 | 0.73 |
| 2026 (January to September) | 95.2% | 5,753 | 4,612 | 0.80 |

*USD million. Source: own calculations.*

In 2021 and 2022 the method reproduces revenue. Since 2023, between 20% and 36% less than estimated is collected. There are five candidate explanations, none of them quantified yet:

1. **The date of the rate.** The duty is fixed when the sworn export sales declaration (DJVE) is registered, not at shipment. Windows with reduced rates, such as the 0% of Decreto 682/2025 in September 2025, brought registrations and payments forward. October and November 2025 collect 25% and 22% of the estimate.
2. **The dólar soja.** The 2022 and 2023 programs brought payments forward: September 2022 collected three times the estimate, and the following months much less.
3. **The 80/20 blend** from December 2023 to April 2025, which in principle does not change the duty in dollars.
4. **Reductions and exemptions missing from the rate table**, above all for soybeans between 2021 and 2024.
5. **Timing differences** between shipment and payment.

**Seasonality.** Duties peak between May and July, with the main harvest, and their monthly variation reaches half the average (coefficient of variation of 0.28 in 2024 and 0.52 in 2025). Foreign-currency debt payments are concentrated in January and July. The fund in regime (d) exists to absorb that mismatch.

## A.4 What the model shows first: an identity

The model is an accounting one: a monthly double-entry ledger with five sectors (Treasury, BCRA, exporters, rest of the private sector and rest of the world), in which every transaction sums to zero and every instrument closes across sectors in every month. The code tests verify that closure in all four regimes.

The first result is an identity, and it is worth stating before any figure. **If the BCRA buys all the dollars that are sold in the FX market, collecting the duty in pesos or in dollars leaves the consolidated public sector with the same dollars and the same peso debt.** In the current regime, the BCRA issues pesos to buy the dollars of the duty, the exporter pays the duty with those pesos and the Treasury uses them to buy the dollars from the BCRA. With collection in dollars, the dollars go directly to the Treasury and the Treasury stops collecting those pesos. The projection confirms it: in both regimes, the peso debt the Treasury has to take on to buy the dollars it lacks is exactly the same (Table A.3). What changes is the pocket in which the dollars end up, the BCRA's or the Treasury's, and when they arrive.

The differences appear in three places: when the BCRA does not buy the dollars, in the currency in which the Treasury ends up indebted and in how regularly the dollars reach it.

## A.5 The term with the duty collected in dollars

The exercise takes what happened between December 2023 and August 2026 as regime (a) and changes a single thing: the duty collected each month, converted to dollars at that month's A 3500 rate, goes into the Treasury's account at the BCRA instead of being paid in pesos. Exports, spending, debt paid and the share of the market bought by the BCRA stay as they were. Since the sources do not say what the Treasury would have done with those dollars, two uses are measured separately.

**First use: the duty dollars replace purchases with pesos.**

| Year | Duties in dollars | Treasury purchases avoided | BCRA purchases not made | Dollars that stay in the public sector |
|---|---:|---:|---:|---:|
| 2023 (December) | 643 | 0 | 492 | 151 |
| 2024 | 6,565 | 7,208 | 1,869 | 4,696 |
| 2025 | 6,000 | 3,495 | 303 | 4,315 |
| 2026 (January to August) | 3,871 | 5,662 | 785 | 2,757 |
| **Total** | **17,079** | **16,366** | **3,450** | **11,918** |

*Table A.1. USD million. The last column is the duty, minus what the BCRA would no longer have bought in the market, minus the avoided purchases that the Treasury made in the market rather than from the BCRA. Source: own calculations.*

With the duty in dollars, the Treasury would have saved 16,366 of the USD 26,810 million it bought with pesos. In pesos, the result barely changes: the pesos the Treasury would not have collected are almost the same as those it would not have had to spend on dollars. The difference at the close, with interest at the BADLAR rate, is 1.2 trillion pesos, and it comes from the timing gap: in 2025 the duty dollars would have arrived before the Treasury needed them.

The large effect is in dollars. During the term the BCRA bought, on average, a small share of what exporters sold: 27% between December 2023 and March 2025 and 9% from April 2025, under the exchange-rate band. Private buyers bought the rest. With the duty in dollars, that part of the duty would have stayed with the Treasury instead of going into private hands: USD 11,918 million more in the consolidated public sector, a quarter of net private dollar hoarding over the term. This result is conditional on everything else having happened in the same way. The model does not say what would have happened on the other side. Private agents would have had fewer dollars to buy, and that could have been resolved through less hoarding, fewer imports or a higher exchange rate; the model does not have those responses.

**Second use: the duty dollars replace new foreign-currency debt.** The Treasury would have taken on USD 16,575 million less in foreign-currency debt and would have had to raise, through peso debt, the duty pesos it no longer collected. The two debts, carried with their interest to August 2026, stand as follows:

| | Pesos at August 2026 prices |
|---|---:|
| Peso debt that would have been taken on, with interest at the BADLAR rate | 29.3 trillion |
| Foreign-currency debt that would have been avoided, with interest at 7% a year, at the August 2026 exchange rate | 27.3 trillion |
| **Additional cost of the peso debt** | **2.1 trillion** |

*Table A.2. Source: own calculations. The rate on the foreign-currency debt is an assumption: at 5% the additional cost is 2.7 trillion, and at 9%, 1.4.*

Swapping dollar debt for peso debt would have cost, in hindsight, between 5% and 10% more. The reason is that during the term the exchange rate rose less than the peso interest rate: dollar debt turned out cheap measured in pesos. That result depends on the period. With a large devaluation along the way, the calculation can come out the other way. What does not depend on the period is the currency: with the duty in dollars, the Treasury would have ended the term with about USD 16.6 billion less in foreign-currency debt and with its equivalent in pesos, a debt that the State issues and can roll over in its own currency.

**The sterilization cost attributable to dollar purchases.** Between December 2023 and August 2026 the BCRA paid 13.4 trillion current pesos in interest, premiums and remuneration of accounts, almost all of it up to July 2024. If each absorbed peso is allocated according to what created it, the share corresponding to net dollar purchases (purchases from the private sector minus sales to the Treasury) is 2.6 trillion, or 19%. The proportional allocation is an assumption: the sources do not tie each absorbed peso to its origin. Since July 2024 the cost of absorbing pesos has been paid by the Treasury as capitalized interest (chapter 3), and there the model cannot separate which part stems from dollar purchases, because the Treasury's peso debt finances spending, maturities and foreign-currency purchases at the same time.

## A.6 Looking ahead

The projection runs from October 2026 to December 2036. It takes exports for the last twelve months with data (October 2025 to September 2026) month by month, applies the rates already decreed for each future month (Decreto 423/2026, which lowers soybeans from 24% to 15% by the end of 2028) and multiplies by the ratio of collected to estimated for January to September 2026 (0.80). On the other side it places firm foreign-currency maturities to creditors outside the public sector, from the phase 2 schedule and the phase 3 holdings. The exchange rate is held at the last observed value: the projection measures dollars.

<iframe class="grafico" src="grafico_derechos_vs_servicio.html" title="Chart A.1"></iframe>

*Chart A.1. Export duties collected in dollars, baseline projection, and foreign-currency maturities to creditors outside the public sector, with and without refinancing of principal owed to international organizations. USD million per year. Source: own calculations.*

| Scenario | Duties, Oct. 2026 to 2036 | Maturities to third parties | Coverage | Months in which the Treasury has to buy dollars, (a) / (c) |
|---|---:|---:|---:|---:|
| Baseline, no refinancing | 44,640 | 206,858 | 21.6% | 122 / 97 |
| Baseline, international organizations roll over principal | 44,640 | 122,902 | 36.3% | 122 / 37 |
| Collection equal to the estimate (without the A.3 gap) | 55,680 | 206,858 | 26.9% | 122 / 94 |
| Drought like that of 2023, from April 2027 | 43,270 | 206,858 | 20.9% | 122 / 97 |
| Export prices 20% lower | 35,720 | 206,858 | 17.3% | 122 / 108 |

*Table A.3. USD million, 123 months. Source: own calculations. In all scenarios, the peso debt the Treasury takes on to buy the dollars it lacks is the same in (a) and in (c).*

Duties collected in dollars would cover a little over one fifth of maturities to third parties if no one refinances, and a little over one third if international organizations roll over principal, as they did during the term. With that refinancing, the Treasury would no longer have to buy dollars in 86 of the 123 months. The rates already decreed lower revenue from about USD 5.4 billion in 2027 to about 4.15 billion a year from 2029.

**The stabilization fund, regime (d).** Under that rule, the fund transfers to the Treasury each month one twelfth of the annual average of the first five projected years, about USD 381 million, and saves the harvest surpluses. The monthly variation of what the Treasury receives (coefficient of variation) falls from 0.21 to 0.12 in the baseline scenario, and from 0.20 to 0.06 in the drought scenario. The fund peaks at USD 1,242 million, and the rule of repaying debt with anything above twelve months of debt service is not triggered, except in the drought, where 147 million is repaid. At these amounts, the fund smooths the months; it does not change how many dollars arrive.

<iframe class="grafico" src="grafico_fondo_mensual.html" title="Chart A.2"></iframe>

*Chart A.2. Dollars the Treasury receives each month in 2027 and 2028, with direct collection in dollars (c) and with the stabilization fund (d). USD million. Source: own calculations.*

## A.7 What the model says and what it does not

What the model supports:

- Collecting in dollars neither creates dollars nor saves pesos for the consolidated public sector as long as the BCRA buys everything that is sold in the FX market. It changes the pocket and the timing.
- When the BCRA does not buy, collection in dollars keeps in the public sector dollars that would otherwise go into private hands. During the term they would have been about USD 11.9 billion.
- For one fifth, or one third, of its maturities to third parties, the Treasury stops depending on the BCRA selling to it or on buying in the market.
- If those dollars replace foreign-currency debt, the Treasury's debt shifts toward pesos. During the term that would have cost somewhat more, because of how the exchange rate moved, but it leaves a debt that the State manages in its own currency.
- The stabilization fund halves the monthly variation of the dollars the Treasury receives.

What the model does not yet include: the response of exporters (when they sell foreign currency and when they pay, depending on the expected rate), that of private agents who no longer buy the duty dollars, the effect on the exchange rate and an import projection, without which projected gross reserves mean nothing and are not reported. Nor does it explain the gap between estimated and collected duties (A.3), which the projection takes as given. These are the behavioral-layer extensions foreseen in the design (`docs/FASE4_DISENO.md`).
