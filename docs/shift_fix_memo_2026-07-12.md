# Shift-Fix Memo — 2026-07-12

**What:** three instances of one defect class — within-firm lags built by row position (and pandas' pad-fill default) instead of by fiscal year — fixed, re-run, verified, and adopted.

| Where | Defect | Fix |
|---|---|---|
| nb05 (sales growth) | `groupby("gvkey")["revt"].pct_change()` pad-fills missing revenues (pandas 2.2.3 default) and differences by row position | strict `revt(fyear)/revt(fyear−1) − 1` via merge on `(gvkey, fyear+1)` |
| nb12 cells 6+7 (falsification) | backward outcome via positional `shift(2)`; membership gaps made "t−2" grab t−3 or older | merge taking the winsorized outcome from exactly `fyear−2` |
| nb08 (persistence) | prior-year sentiment via positional `shift(1)` across the same gaps | merge on `(gvkey, fyear+1)` |

All three merges carry `validate="m:1"` as insurance against future duplicate keys.

**Why nb05 was patched in place, not re-executed:** the notebook's first cells re-pull `comp.funda` from WRDS, which would move the Compustat vintage and contaminate the before/after attribution. The stored panel carries raw `revt` for all 9,048 firm-years, so `src/patch_sales_growth_20260712.py` applied the identical logic to the frozen data. nb05's stored outputs therefore predate the fix (documented in the cell); a from-scratch re-execution would re-pull and could drift.

## Measured impact

- **nb05 (D1): prophylactic only.** 34 NaN-revenue firm-years existed; pad-fill had fabricated **14** growth values (9 NaN-revenue years given exactly 0.0 growth + 5 following years whose growth silently spanned the gap; the other 25 NaN rows were group-leading, nothing to pad from). **Zero of the 14 reach the analytical sample** — the 2026-07-02 membership row-filter had already excluded them all. `panel_yearly` and `panel_monthly` are value-identical pre/post (panel_monthly sha256 unchanged: `96c0d653…ebc5`); Tables 1/2/3/4, correlations, alpha, and all figures byte-identical.
- **nb12 (D2): the only realized result change.** Of 3,741 backward-ROA pairs, 21 had wrong-vintage sources (t−3 or older) and were removed; 5 correct t−2 pairs the positional shift had missed were recovered (net N 3,741→3,725; SG 3,740→3,724).
  - ROA backward: coef 0.00709 → **0.00754**, t 2.355 → **2.131**, p 0.019 → **0.033**. Still significant at 5% — **the "ROA fails falsification" verdict stands.**
  - Sales growth backward: coef −0.00866 → **−0.01065**, t −0.841 → **−0.977**, p 0.40 → 0.33. **Still passes cleanly.**
- **nb08: persistence 0.616 → 0.629** (4,337 → 4,314 pairs; 23 gap-crossing pairs nulled). Prose "around 0.6" remains accurate. ANOVA decomposition unchanged (49.7/50.3).

**Materiality rule: not crossed.** Headline coefficients moved 0%; no t-statistic crossed 1.96/1.65; no qualitative verdict changed. Adopted without a JJ pause; worth one line in the next weekly email alongside the running corrections log.

## Verification

Three independent agents after the re-run: (1) adversarial code review — PASS (fyear arithmetic exact; bitwise-equal to the old code wherever the old code was right; no downstream cell relies on the replaced index/order); (2) independent numerical reproduction — all seven claims reproduced digit-for-digit from scratch implementations, including reproducing the OLD numbers under the buggy alignment (delta fully attributable to the fix); (3) completeness sweep — no remaining instance of the defect class in notebooks 00–15 (nb07's sentiment lag was already merge-based; nb15's positional indexing is safe on the verified gap-free 144-month series; nb02's identifier ffill is a different, documented mechanism).

## Honest imperfections

1. `src/patch_sales_growth_20260712.py`'s original run printed "sales_growth values changed: 0" — a nullable-Float64 mask bug in the *report* (with `Float64`, `value == NA` → `NA`, and masks treat `NA` as False). The write itself was correct; the 14 changes were verified against `data/backup_pre_shiftfix_20260712/`. The script's mask is now `.fillna(False)`. **Rule for future audits: compare panel columns as numpy float64, never with naive `==` masks.**
2. nb08's two standalone figures (`output/fig_sentiment_distribution.png`, `fig_sentiment_over_time.png`) were overwritten at re-execution without archiving. Harmless — the panel they draw from is value-identical — but the pre-fix bytes are gone.
3. nb05 stored outputs predate the fix (see above), a documented deviation from the stored-outputs standard.

## Prose ledger (for the docx — the only mandatory edits)

| Location | Old | New |
|---|---|---|
| Table 5, falsification row | −0.84 (passes) / 2.36 (fails) | **−0.98 (passes) / 2.13 (fails)** |
| §4.5 falsification paragraph | "backward t = −0.84" / "backward t = 2.36" | **−0.98** / **2.13** |
| §4.1 persistence (optional) | "around 0.6" | still true (0.629); no change required |

Do **not** touch: Table 1's sales-growth minimum "−0.84" (coincidence, unrelated) and the senior-leadership sub-rating "t = 2.36" in §4.5 (unrelated, unchanged). §5.2's "at least as strongly" comparison still holds (backward 2.13 > forward 1.68).

**Pre-fix state:** tag `pre-shiftfix-20260712`, `data/backup_pre_shiftfix_20260712/`, `output/archive_pre_shiftfix_20260712/`. Fix pre-committed in `244ff3a` before execution.
