# RELIFE S.R.L. — Business Plan v9 Analysis

Source: `RELIFE_SRL_CORPORATE_BUSINESS_PLAN_v9__SINTETICO.xlsx` | Reviewed: 2026-06-29
Structured data: `corporate/relife_bp_v9_data.json`

This is the operating-company (Opco) BP, distinct from the property-owning SPVs (e.g. Portonaccio, Pigneto). "Students accommodation" revenue is RELIFE's **operator/management fee**, not gross rent — see Finding 3.

---

## 1. Model integrity issues (fix before showing to any evaluator)

### 1.1 — 2024 revenue is overstated by ~€99,450 (22%) due to a formula bug
`Total Revenues` for 2024 uses `=SUM(B47:B123)`, a contiguous range that sweeps up both the city-level detail rows **and** their subtotal rows for four fee categories (Interior advisory, Construction monitoring, Marketing advisory, Pre-opening fee), double-counting each. Every other year (2025-2031) uses the correct discrete-cell formula `=SUM(D47,D66,D85,D104,D123,D127)`.

| | Reported | Corrected | Delta |
|---|---|---|---|
| 2024 Revenue | €445,262 | €345,812 | -€99,450 |
| 2024 EBIT | €183,976 (41.3% margin) | €84,526 (24.4% margin) | -€99,450 |

This is the year you're calling "real" — an evaluator's first model check (cross-footing each year the same way) will catch this in under five minutes. Fix the formula before sharing externally; it materially overstates your one fully-mature, proven year.

### 1.2 — "Fee Consultant" revenue has no matching cost
Rows 124-126 (Finance Manager / Marketing & Sales Manager / Digital Marketing, each computed as `=salary*0.5`) are summed into "Fee Consultant" and flow into Total Revenue every year (€20.5K in 2024 growing to €105K in 2031). But `Total G&A` explicitly sums only rows 132, 135, 138, 145, 147, 150, 170 — it never references rows 124-127. So this revenue is booked at 100% margin with the underlying staff cost never expensed anywhere in the model.

If this is a genuine pass-through recharge to SPV clients with no cost to RELIFE, label it that way explicitly. If it's a recharge of RELIFE's own people, the cost is missing and EBIT is overstated by this full amount every year (€47K in 2026 → €105K in 2031 — modest at scale, but ~13% of revenue in 2026, which matters while you're loss-making).

### 1.3 — No D&A line
There's no depreciation/amortization row anywhere in the cost structure, despite capitalizable spend implied by "Interior & FF&E advisory" and growing IT/software costs (rows 138-144, scaling from €14.7K to €455K by 2031). EBIT and EBITDA are being treated as identical. An evaluator will ask for this split — without it they can't sanity-check your margin claims against any comp set (comps are quoted on EBITDA, not EBIT).

---

## 2. Growth trajectory — this is the biggest red flag

| Year | New beds added | New properties opened | Cities |
|---|---|---|---|
| 2024 | — | 1 (Turin, baseline) | 1 |
| 2025-26 | 0 | 0 | — (stabilization year) |
| 2027 | +714 | **3** | Padova, Rome, Modena |
| 2028 | +1,155 | **6** | Pisa, Turin 2, Bologna, Monza, Siena, Trieste |
| 2029 | +1,943 | **5** | Piacenza, Cagliari, Mestre, Verona, Rome 2 |
| 2030 | +950 | 2 | Bari, Ferrara |
| 2031 | +264 | 1 | Rome 3 |

In five years (2027-2031) the plan calls for opening **17 new properties in 14 new cities**, having opened and stabilized exactly **one** in the prior five. 2028 alone assumes six simultaneous openings — a ~10x jump in execution velocity with zero demonstrated multi-site track record.

This is precisely what an institutional evaluator will challenge first, because:
- There's nothing in the file (LOIs, signed leases, term sheets) showing the 2027 pipeline is actually secured — let alone 2028-2029.
- Real, well-capitalized PBSA platforms with established systems typically scale at **2-4 new properties/year** at peak velocity, not 5-6.
- Multi-city (not multi-site-in-one-city) expansion adds regional complexity — new local counsel, new local relationships, more travel — that typically works *against* G&A leverage, not with it (see §3).

**What would de-risk this for an evaluator:** signed agreements (even non-binding) for the 2027 cohort, a delivery org-chart showing who runs parallel fit-outs, and ideally one demonstrated second/third opening before underwriting six-in-a-year.

## 3. Cost structure vs. market

- **G&A/bed** falls from €1,453 (2026) to €605 (2028) to €399 (2031) — a ~3.6x improvement in cost leverage in 5 years. Directionally right for an asset-light platform, but the model is scaling into **14 different cities**, not increasing density in 2-3 hubs. Geographic dispersion (each new city needs local admin, legal, and relationship overhead) usually erodes G&A leverage relative to a single-region rollout — the plan assumes the opposite effect at a faster pace than the geography supports.
- **EBIT margin** climbs from -32% (2026) to 65-75% (2028-2031). For comparison, mature **asset-light** branded hospitality/residential operators (Accor, IHG-style — the closest comp class for a pure management-fee business) typically run **40-55% EBITDA margins on fee revenue** at scale. 65-75% is above that range and should be supported by an explicit bridge (which cost lines stay flat as beds scale 16x from 331→5,357) rather than asserted.
- **CEO compensation** is flat at €182,000 through all three loss/breakeven years (2024-2026), then grows ~6.5%/year to €350,425 by 2031. Paying full senior-executive comp through a -€117K EBIT year while everything else gets a "we're investing ahead of scale" framing is the kind of related-party item a diligence team flags and asks you to justify or normalize out.

## 4. Revenue model — confirm this explicitly

Reverse-engineering Turin (your only mature, single-property data point): accommodation revenue/bed runs **€741-1,208/year**, roughly 6-10x below what the GSL Italy market report indicates for *gross* Turin PBSA rent (€1,200/month prime → ~€9,600-13,200/year). Cross-checked against the industry-standard **8-12% management fee on gross rent** for student housing operator contracts, Turin's numbers imply almost exactly that fee rate.

**Conclusion: "Students accommodation" revenue in this BP is RELIFE's operator fee, not gross rent.** This matters enormously for valuation (§5) — it confirms RELIFE is a fee-based management company, not a rental-income business, which is the right framing but should be stated as an explicit assumption on the BP itself, since an evaluator will otherwise assume gross revenue and conclude your rent-per-bed is absurdly low.

---

## 5. How asset-light operators like this get valued

Three approaches apply, and the right one depends on which year you're valuing:

1. **EV/EBITDA multiple** — works for *profitable, proven-at-scale* operators. Mature asset-light hospitality/residential managers trade 10-15x EBITDA (strong brand, contracted recurring fees, minimal capex). Unproven growth-stage platforms (RELIFE's category once 2027-28 prove out) trade at a discount: **6-9x forward EBITDA** is a defensible private-market range.
2. **Revenue multiple** — used when EBITDA is negative (your 2025-2026 reality). Asset-light real estate service platforms with recurring fee revenue and credible growth typically see 1-3x revenue in private transactions — soft, comp-scarce territory.
3. **Risk-adjusted forward multiple (the right one for "today")** — take a future proof-point year, multiply, discount back at a high required return that prices in execution risk, then apply a delivery haircut to the underlying plan.

**Caution on real-estate comps:** the Nido/Livensa deal (€1.2bn for ~9,000 beds, ~€133k/bed, closed Q4 2025) is a **real-estate NAV transaction** — Nido bought buildings + operations together. It is not a comp for valuing RELIFE as a pure management company; don't let anyone (including yourself) anchor on a €/bed real-estate number for an Opco-only valuation.

### Valuation today (mid-2026)

2026 is loss-making (-€117K EBIT on one property), so there's no current EBITDA to multiply. Value today is almost entirely the **discounted, risk-adjusted option value** of the 2027-2028 plan:

- Take 2028 EBIT (€2.48M) as the proof-point year.
- Haircut for realistic multi-city delivery risk: **50-60%** of plan achieved (typical for an unproven rollout of this velocity) → ~€1.2-1.5M risk-adjusted EBITDA.
- Apply **6-8x** (unproven-platform multiple) → €7.2-12M value *in 2028*.
- Discount back 2 years at a **30% risk-adjusted rate** (appropriate given execution + pipeline + key-person risk) → **≈ €4.3-7.1M today**.

### Valuation in 2028 ("a couple of years")

If the 2027 cohort (Padova/Rome/Modena, 714 beds) actually opens and stabilizes on schedule, most of the platform-risk discount above should unwind:

- **Plan executes ~70-80%** of 2028 scale (a more typical outcome than 100%, given the pace) → EBIT ≈ €1.7-2.0M.
- Apply **7-10x EBITDA** (now a *proven* multi-city platform, smaller discount to mature comps) → **≈ €12-20M**.
- If 2027 slips or underdelivers, this collapses back toward the 2026 range — 2027 is the single highest-leverage proof point in the whole plan.

**These are triangulated planning ranges, not an appraisal.** The swing factors are the execution haircut and the multiple — both move the answer by 2-3x. Before using any number in a real conversation with an investor or buyer, get a banker/valuation advisor to run this against actual private PBSA-operator transaction data (which isn't public) — what's above is the right *framework*, sized with your own numbers.

---

## 6. Punch list before this goes to an evaluator

1. Fix the 2024 revenue formula (§1.1) — five-minute fix, removes the single easiest-to-catch error.
2. Add the missing Fee Consultant cost, or relabel it as a zero-margin recharge (§1.2).
3. Add a D&A line and report EBITDA explicitly, not EBIT-as-EBITDA (§1.3).
4. Attach evidence for the 2027 pipeline (LOIs/leases) — this is what makes or breaks the entire valuation story (§2).
5. State the management-fee assumption (and the %) explicitly on the BP rather than leaving it implicit (§4).
6. Add a one-line bridge explaining why G&A/bed nearly thirds while expanding into 14 new cities (§3).
7. Consider normalizing CEO comp in the loss years, or footnoting it, ahead of diligence (§3).
