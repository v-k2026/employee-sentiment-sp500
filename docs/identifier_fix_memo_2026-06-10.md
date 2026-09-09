# Identifier-Fix Memo — 2026-06-10

**What:** Corrections to the ticker→gvkey mapping (notebook 02), the CRSP link filter
(notebook 04), and one Revelio rcid supplement (notebook 03); full pipeline re-run
(02→05, 07→13). Fix committed **before** re-running (`0c8f90f`), per the
pre-commitment workflow. Pre-fix data and outputs preserved in
`data/backup_pre_idfix_20260610/` and in git history.

**Bottom line: every qualitative conclusion survives.** Alpha remains null, ROA and
sales growth remain significant, the margin remains null, the regime break and the
leadership/culture sub-rating pattern persist. Point estimates move at the second
decimal. Two p-values cross the 0.05 line in the robustness section (details below) —
they were borderline before and remain borderline, just on the other side.

---

## 1. What was wrong

The old notebook 02 collapsed each ticker to a single gvkey
(`groupby("ticker").first()`). Under the universe's forward-corrected-ticker
convention this failed in two ways:

**(a) Zombie-spell collisions** — an unrelated firm's stale ticker spell won the match:

| Ticker | Was mapped to | Should be (now is) |
|---|---|---|
| LB | 006534 La Barge Inc (defense micro-cap) | 006733 L Brands / Bath & Body Works |
| APTV | 024217 Advanced Promotion Technologies (delisted 1996) | 118122 Aptiv PLC (incl. Delphi Automotive era) |
| ES | 178846 EnergySolutions Inc (never an S&P 500 member) | 007970 Eversource Energy (ex-Northeast Utilities) |
| JEF | 006239 Jefferies Group LLC | 006682 Jefferies Financial Group (ex-Leucadia) |

The ES and JEF cases were discovered by auditing all 751 tickers for the same
mechanism — they were not in the original problem report.

**(b) Lineage truncation** — eight tickers legitimately span two gvkeys after corporate
events (AGN, CB, DD, DOW, FOX, FOXA, FTI, IR). Collapsing to one gvkey silently
dropped the other entity: **Chubb Ltd (2016–2024), Allergan plc, Dow Inc, Fox Corp,
TechnipFMC and Ingersoll Rand Inc were entirely absent from all panels.** Fixed by
keeping the (already correct) per-year spell match instead of collapsing per ticker.
A validation cell now asserts exactly these eight tickers span two gvkeys.

**(c) CRSP link filter** — Eaton Corp plc (004199) and Dayforce (023546) carry their
sole primary CRSP link with linktype `LS`, which the `LU/LC`-only filter excluded:
both had **zero returns** in the old panel. No other universe firm has any LS link
(verified), so adding `LS` affects exactly these two. Note: the original report's
hypothesis of a separate post-2012 Eaton plc gvkey was refuted — 004199 *is* Eaton
Corp plc (Compustat kept the gvkey through the 2012 Irish redomiciliation).

**(d) UAL rcid** — Revelio's `company_mapping` row for "United Airlines Holdings,
Inc." (rcid 22214941, ticker UAL, CUSIP 910047109) has a NULL gvkey and zero reviews;
the 8k+ United reviews sit under subsidiary rcid 822516, which Revelio maps to the
subsidiary gvkey 010484. Manual supplement attaches rcid 822516 to parent gvkey
010795 (no double-counting: 010484 is not in the universe).

**Correction to the original problem report:** L Brands was *not* actually missing
from the panels — gvkey 006733 was already present via the BBWI ticker (2021–2024
universe rows), and panels are built full-window per gvkey. The LB ticker rows were
mis-mapped, but the firm's data was there. Aptiv, by contrast, was genuinely absent.

## 2. Panel changes

| Panel | Before | After |
|---|---|---|
| Universe gvkeys | 712 | 717 (−4 wrong firms, +9 correct; 89 of 6,535 firm-year rows changed gvkey) |
| returns_panel | 97,701 rows / 708 firms | 98,978 / 717 (+11 firms incl. Eaton, Dayforce; −31 contaminating months from EnergySolutions & Jefferies Group LLC; all overlapping rows bit-identical) |
| sentiment_panel | 7,982 rows / 656 firms | 8,069 / 664 |
| fundamentals_panel | 8,950 rows / 710 firms | 9,048 / 717 |
| panel_monthly | 81,089 / 644 firms | 82,190 / 653 |
| panel_yearly | 6,778 / 638 firms | 6,864 / 647 |
| Firms without Revelio rcid | 13 | 9 |

Firms gaining full return histories: Aptiv, Eversource, Chubb Ltd, Jefferies
Financial, Eaton (156 months each); Ingersoll Rand Inc (111), Allergan plc (101),
TechnipFMC (96), Dayforce (81), Fox Corp (70), Dow Inc (69).

**Independent of the fix:** re-pulling Revelio also picked up vendor-side revisions —
52 of 7,967 unchanged firm-years (0.7%) shifted (median +5 reviews; max sentiment
change 0.08), concentrated 2023–24, and Leidos (LDOS) lost its (always trivial,
3-review) rcid mapping. This drift moves third decimals and is inseparable from any
re-pull.

## 3. Headline results, before → after (2013–2023, JJ's window)

| Result | Before | After | Verdict |
|---|---|---|---|
| H1 raw long-short (full 144 mo) | 0.062%/mo, t=0.31 | 0.058%/mo, t=0.29 | null, unchanged |
| H2a FF5+MOM alpha | 1.44%/yr, t=0.80, p=0.42 | 1.33%/yr, t=0.74, p=0.46 | null, unchanged |
| SMB loading | −0.450, t=−3.69 | −0.447, t=−3.66 | unchanged |
| Regime: 2013–2019 alpha | 3.18%/yr, t=1.93, p=0.054 | 3.01%/yr, t=1.83, **p=0.068** | still marginal; slightly weaker |
| Regime: 2020–2023 alpha | −0.35%/yr, t=−0.12 | −0.52%/yr, t=−0.17 | null, unchanged |
| ROA | 0.00526, t=2.14, p=0.033, N=6,225 | 0.00496, t=2.05, p=0.040, N=6,303 | significant, slightly weaker |
| Operating margin | t=0.69 | t=0.75 | null, unchanged |
| Sales growth | 0.0305, t=3.01, p=0.003 | 0.0314, t=3.13, p=0.002 | significant, slightly stronger |

Full-sample (2013–2024): alpha 0.90%→0.83%/yr (t 0.51→0.47); ROA t 2.28→2.21;
sales growth t 3.35→3.49; margin still null. Quintile sort still monotonic in
sentiment (2.85→4.06); per-year LS pattern essentially identical (2021 −1.69%,
2022 −0.68%, 2023 +0.94%).

## 4. Robustness, before → after — including the two threshold crossings

- **≥30-review threshold, ROA: t=1.97 (p=0.049) → t=1.89 (p=0.058).** Crosses 5%.
  §3 of the project doc already framed this as "survives marginally"; it is now
  marginal on the other side of the line. Coefficient still positive (0.0096);
  the power interpretation is unchanged. Sales growth: t=1.61→1.62 (unchanged).
- **Precision weighting:** ROA t=2.03→1.97 (p=0.0494, still just under 5%);
  sales growth t=2.94→3.05.
- **Sub-ratings on ROA:** leadership t=3.20→3.10*, culture 2.26→2.17*,
  **compensation 2.04 (p=0.042) → 1.95 (p=0.051)** — second crossing; career
  1.87→1.77, WLB 0.74→0.64. On sales growth: leadership 3.19→3.14*, culture
  2.96→3.03*, compensation 2.80→2.96*, career 1.94 (p=0.052)→2.02 (p=0.044, crosses
  *into* significance), WLB 1.87→1.79. The grouped claim — management-quality
  dimensions predict, perks don't, no precise ranking — is unaffected; if anything
  the borderline shuffling underlines why only the grouped claim was committed to.
- **Falsification:** ROA still fails (backward t=2.50→2.56); sales growth still
  passes (t=−0.76→−0.71).
- **H2b regime split:** 2013–2019 sales growth t=3.18→3.31, ROA t=1.80→1.78;
  2020–2024 both still null.
- **Descriptives:** essentially unchanged (sentiment–size corr 0.142; autocorrelation
  0.601; within-firm share 70.5%; the 2021 level jump persists).

All seven figures regenerated (visually equivalent; fig2's pre-period bar now 3.01
with t=1.83 label).

## 5. Required text/outline updates

1. **Outline §3.2 sample size:** 74,410 firm-months / 639 firms → **75,403 / 649**
   (`docs/outlines/thesis_outline.docx` still carries the old numbers).
2. **§3.6 coverage caveat:** "13 firms with no rcid" → **9 firms** (Chubb Corp,
   Allergan Inc, Intl Game Technology, Old Copper Co (JCPenney), Integrys, Kraft
   Foods Group — all dead/acquired pre-2016 — plus Dayforce, Solventum, GE Vernova).
   The survivorship-direction framing still holds.
3. Any drafted text quoting exact coefficients should be refreshed from the
   regenerated `output/` tables; the narrative does not change.
4. Regime-alpha sentence: pre-period p moves 0.054 → 0.068 — keep calling it
   marginal, do not round it into significance.

## 6. Candidate fixes found but NOT applied (decision for Vlad/JJ)

Same defect class as UAL (Revelio NULL-gvkey rcid), found while enumerating the 9
no-rcid firms — applying them would require only adding rows to the notebook 03
supplement and re-running 03→07→08–13:

- **Dayforce** (gvkey 023546, in-window 2021–2024): rcid 820766 "Dayforce, Inc.",
  3,229 reviews — name-exact but NULL ticker/cusip, so weaker evidence than UAL's.
- **GE Vernova** (045169) → rcid 7760997; **Solventum** (045167) → rcid 96357101.
  Both 2024-only members — no effect on the 2013–2023 headline window.
- **Leidos** (165123): present in returns/fundamentals but its Revelio mapping
  (never more than 3 reviews) was dropped vendor-side; the real Leidos reviews
  presumably sit under an unmapped rcid. Larger judgment call; not pursued.

## 7. Disclosure note sent to the supervisor

> While preparing the methodology chapter I audited the ticker→gvkey identifier
> mapping and found that 11 firms (incl. Chubb, Eaton, Eversource, Aptiv, Dow, Fox)
> were silently dropped by mechanical mapping edge cases, and two non-members had
> leaked in. I fixed the mapping (committed before re-running), re-ran the full
> pipeline, and re-verified all headline results: conclusions are unchanged
> (alpha null; ROA t=2.05 and sales growth t=3.13 significant; regime pattern
> intact). Sample sizes in §3.2 change slightly (now 75,403 firm-months, 649 firms).
> Full before/after comparison available if useful.
