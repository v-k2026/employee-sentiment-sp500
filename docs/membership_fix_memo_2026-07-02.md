# S&P 500 Membership-Filter Fix — Memo, 2026-07-02

## 1. The defect

Notebook 07 built the analytical panels by merging the full CRSP returns panel
(every firm-month 2012–2024 of every firm that was EVER a year-end S&P 500
member) with lagged sentiment. The point-in-time universe file
(`sp500_universe_with_gvkey.parquet`) was loaded but never applied as a row
filter, and notebooks 08–12 never applied it either. Consequences, measured on
the stored panels (2013–2023):

- `panel_monthly`: 15,794 of 75,403 firm-months (**20.9%**) fall outside
  (gvkey, year) membership — 9,028 pre-first-membership, 6,309
  post-last-membership, 457 gap months.
- `panel_yearly` estimation sample: 1,341 of 6,303 firm-years (**21.3%**).
- Example: Tesla (member from 2020) contributes all 132 months of 2013–2023;
  its pre-inclusion run-up sits in the Q5 portfolio for seven years before it
  joined. Quintile sorts held 557–585 firms per year against a ~505-member
  index.

Pre-first-membership rows are a look-ahead selection (index entrants are
chosen after strong performance), and the panel contradicts the thesis text,
which describes point-in-time membership in §1, §3.1, and §3.2.

Found by the 2026-07-01 pre-submission audit (multi-agent, Claude Fable 5);
independently reproduced from the parquets before adoption.

## 2. Pre-committed fix specification (committed before the re-run)

1. **Membership filter, both panels:** inner-join the final analytical panels
   on (gvkey, year) — respectively (gvkey, fyear) — against the year-end
   membership pairs in `sp500_universe_with_gvkey.parquet`. A firm contributes
   outcome rows only for years it was actually a member.
2. **Sentiment lags stay unrestricted:** the t−1 sentiment signal does not
   require membership in t−1; only outcome years are filtered.
3. **Everything else unchanged:** window (2013–2024 panel, 2013–2023
   headline), winsorization recipe (caps from the full panel before the
   headline-window restriction), all estimation specs, quintile construction,
   factor set, standard errors.
4. **Notebook 09 reporting fix (bundled, no data change):** nb09 now also
   prints the 2013–2023 (132-month) raw long-short statistics, since the
   thesis headline quotes that window; previously only the 144-month
   full-sample t-statistic (0.29) was printed and it leaked into the draft as
   a 2013–2023 number. The saved `long_short_returns.parquet` remains the full
   2013–2024 series.

## 3. Deliberately NOT bundled (single-change attribution)

Logged by the same audit, held for separate decisions so the number movement
in this re-run is attributable to the membership filter alone:

- nb05 `pct_change()` legacy pad-fill (fabricates ~18 sales-growth firm-years
  from missing revenue) — recommend fixing with `fill_method=None` in a later
  pass.
- nb12 falsification `shift(2)` is positional, not calendar (wrong lag for
  firms with gap years).
- Delisting returns (`crsp.msedelist`) never pulled — disclosure candidate for
  §3.6.

## 4. Expected impact (audit preview estimates, to be superseded by this re-run)

| Result | Pre-fix (published draft) | Preview with filter |
|---|---|---|
| H2b sales growth | 0.0239, t=2.60, p=.009 | ~0.0217, t≈1.78, p≈.07 |
| H2b ROA | 0.0048, t=1.99, p=.046 | ~0.0039, t≈1.63, p≈.10 |
| H1 raw LS | +0.06%/mo, t=0.29* | ~+0.15%/mo, t≈1.04 |
| H2a alpha 13–23 | +1.33%/yr, t=0.74 | ~+1.43%/yr, t≈1.37 |
| Alpha 13–19 | +3.01%/yr, t=1.83 | ~+0.46%/yr, t≈0.34 |
| Alpha 20–23 | −0.52%/yr, t=−0.17 | ~+3.32%/yr, t≈2.12 (post-hoc, break n.s.) |

*144-month value; see §2.4.

Materiality rule: headline t-stats cross the 1.96/1.65 boundaries → JJ
informed by email 2026-07-02 before adoption; Vlad directed the fix and
re-run the same day.

## 5. Preservation of the pre-fix state

- Git tag `pre-membership-fix-20260702` (code + stored outputs as committed).
- `data/backup_pre_membershipfix_20260702/` — panel_monthly, panel_yearly,
  long_short_returns parquets.
- `output/archive_pre_membership_fix_20260702/` — all 8 result CSVs + the 7
  thesis figures.

## 6. Re-run protocol

Execute notebooks 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 in order,
in-place, under the `thesis` conda env (scratch kernelspec override; the
machine's default `python3` kernelspec points at base Anaconda). Verify row
counts (~59.6k firm-months / ~5.0k firm-years on 2013–2023), compare headline
numbers against the preview above, then commit the executed notebooks.
