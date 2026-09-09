"""One-time patch (2026-07-12): recompute sales_growth in the stored
fundamentals panel with the fixed fiscal-year logic from notebook 05.

Why a patch instead of re-executing notebook 05: the notebook's first cells
re-pull comp.funda from WRDS, which would move the Compustat vintage and
contaminate the before/after attribution of this fix. The stored parquet
already carries raw revt for every firm-year (2011-2024, pre-membership
filter), so the corrected growth can be computed from frozen data.

Bug being fixed: groupby("gvkey")["revt"].pct_change() (pandas 2.2.3)
pad-fills missing revenues by default before differencing, fabricating
growth values in and after NaN-revenue firm-years, and differences by row
position rather than fiscal year.

Run once from the repo root:  python src/patch_sales_growth_20260712.py
See docs/shift_fix_memo_2026-07-12.md and the pre-commit for context.
"""
import pandas as pd
from pathlib import Path

PANEL = Path(__file__).resolve().parents[1] / "data" / "fundamentals_panel.parquet"

f = pd.read_parquet(PANEL)
assert not f.duplicated(subset=["gvkey", "fyear"]).any(), "duplicate (gvkey, fyear) rows"

f = f.sort_values(["gvkey", "fyear"]).reset_index(drop=True)
f["_old_sales_growth"] = f["sales_growth"]

_prev = f[["gvkey", "fyear", "revt"]].copy()
_prev["fyear"] = _prev["fyear"] + 1
f = f.merge(_prev.rename(columns={"revt": "revt_prev"}), on=["gvkey", "fyear"], how="left")
f["sales_growth"] = f["revt"] / f["revt_prev"] - 1
f = f.drop(columns=["revt_prev"])

old, new = f["_old_sales_growth"], f["sales_growth"]
# NOTE: with nullable Float64, (old == new) yields pd.NA where one side is NA,
# and boolean masks treat NA as False — fillna(False) keeps the diff honest.
# (The original 2026-07-12 run printed "changed: 0" because of this; the write
# itself was correct — 14 values changed, verified against the backup.)
same = ((old == new) | (old.isna() & new.isna())).fillna(False)
changed = f.loc[~same, ["gvkey", "fyear", "revt", "_old_sales_growth", "sales_growth"]]

print(f"Rows total: {len(f):,}")
print(f"sales_growth values changed: {len(changed)}")
print(f"  value -> NaN (fabricated growth removed): {(old.notna() & new.isna()).sum()}")
print(f"  NaN -> value: {(old.isna() & new.notna()).sum()}")
both = changed[changed["_old_sales_growth"].notna() & changed["sales_growth"].notna()]
print(f"  value -> different value: {len(both)}")
if len(changed):
    print("\nChanged rows by fyear:")
    print(changed["fyear"].value_counts().sort_index().to_string())
    print("\nAll changed rows:")
    print(changed.to_string(index=False, max_rows=80))

f = f.drop(columns=["_old_sales_growth"])
f.to_parquet(PANEL, index=False)
print(f"\nSaved patched panel to {PANEL}")
