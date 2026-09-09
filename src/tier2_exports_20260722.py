"""Tier 2 exports (2026-07-22) — export-only, no specification or sample changes.

Produces three artifacts from the frozen pipeline's existing data:
1. output/table_alpha_subperiod.csv — six-factor loadings for the Table 3
   sub-period rows (2013-2019, 2020-2023), same regression as nb10 (OLS,
   HAC/Newey-West 3 lags). Gate: must reproduce the full-window loadings in
   output/table_alpha_regression.csv and the published sub-period alphas
   (0.46 t=0.34; 3.32 t=2.12) before anything is written.
2. output/table_quintile_characteristics.csv — mean firm characteristics by
   sentiment quintile, quintiles exactly as nb09 assigns them (qcut(5) on
   lagged sentiment within year, monthly analytical panel), characteristics
   aligned as in nb08's Table 2 (contemporaneous fyear; December market
   equity; book-to-market = seq/me; raw values).
3. output/fye_share.csv — share of firm-years and firms with non-December
   fiscal year end, for the Section 5.4 alignment caveat.

No existing artifact is modified. Materiality rule not applicable (no
correction; nothing previously reported changes).

RUN RECORD 2026-07-22 (gates A+B passed on first run):
- Sub-period loadings (NW 3): 2013-2019 MKT 0.04 (1.02), SMB -0.24 (-2.99),
  HML 0.00 (0.06), RMW -0.02 (-0.23), CMA -0.29 (-2.68), MOM -0.04 (-0.49);
  2020-2023 MKT 0.07 (1.45), SMB -0.20 (-2.09), HML -0.13 (-2.20),
  RMW -0.23 (-2.08), CMA -0.14 (-1.60), MOM -0.09 (-2.33).
- Quintile means (raw): sentiment 2.88->4.06; market equity $28.2B (Q1) ->
  $96.9B (Q5); log assets 9.80->10.12 (peaks Q4 10.22); B/M 0.42->0.32;
  ROA 0.058->0.077; op. margin 0.246->0.276; leverage 0.64->0.62;
  sales growth 0.078->0.126; N per quintile 992-998 (991-994 w/ fundamentals).
- FYE: 24.2% of firm-years (24.1% of firms) have non-December fiscal year end
  (N = 5,434 firm-years, 635 firms; largest non-Dec months: Sep 268, Jan 243,
  Jun 199).
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "output"

# ---------------------------------------------------------------- 1. sub-period loadings
ls = pd.read_parquet(DATA / "long_short_returns.parquet")
ls["date"] = pd.to_datetime(ls["date"])
factors = pd.read_parquet(DATA / "factors.parquet")
factors["date"] = pd.to_datetime(factors["date"])

reg = ls.merge(factors[["date", "mkt_rf", "smb", "hml", "rmw", "cma", "mom"]],
               on="date", how="inner")

FACTORS = ["mkt_rf", "smb", "hml", "rmw", "cma", "mom"]

def six_factor(frame):
    y = frame["long_short"].astype("float64")
    X = sm.add_constant(frame[FACTORS].astype("float64"))
    return sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})

windows = {
    "2013-2023": (2013, 2023),
    "2013-2019": (2013, 2019),
    "2020-2023": (2020, 2023),
}
rows = []
results = {}
for label, (y0, y1) in windows.items():
    sub = reg[(reg["date"].dt.year >= y0) & (reg["date"].dt.year <= y1)]
    res = six_factor(sub)
    results[label] = res
    rows.append({"window": label, "term": "alpha_pct_yr",
                 "coefficient": res.params["const"] * 12 * 100,
                 "z_stat": res.tvalues["const"], "n_months": int(res.nobs)})
    for f in FACTORS:
        rows.append({"window": label, "term": f,
                     "coefficient": res.params[f], "z_stat": res.tvalues[f],
                     "n_months": int(res.nobs)})

sub_tbl = pd.DataFrame(rows)

# Gate A: full window must reproduce the committed artifact digit-for-digit (4dp).
committed = pd.read_csv(OUTPUT / "table_alpha_regression.csv", index_col=0)
full = results["2013-2023"]
for term in ["const"] + FACTORS:
    assert round(full.params[term], 4) == round(committed.loc[term, "coefficient"], 4), term
    assert round(full.tvalues[term], 4) == round(committed.loc[term, "z_stat"], 4), term
assert int(full.nobs) == 132

# Gate B: sub-period alphas must reproduce Table 3 as published (2dp).
a_pre = results["2013-2019"].params["const"] * 12 * 100
t_pre = results["2013-2019"].tvalues["const"]
a_post = results["2020-2023"].params["const"] * 12 * 100
t_post = results["2020-2023"].tvalues["const"]
assert (round(a_pre, 2), round(t_pre, 2)) == (0.46, 0.34), (a_pre, t_pre)
assert (round(a_post, 2), round(t_post, 2)) == (3.32, 2.12), (a_post, t_post)
assert (int(results["2013-2019"].nobs), int(results["2020-2023"].nobs)) == (84, 48)
print("Gates A+B passed: full-window loadings and published sub-period alphas reproduced.")

sub_tbl.to_csv(OUTPUT / "table_alpha_subperiod.csv", index=False)
print(sub_tbl.round(4).to_string(index=False))

# ------------------------------------------------- 2. quintile characteristics
panel_monthly = pd.read_parquet(DATA / "panel_monthly.parquet")
panel_yearly = pd.read_parquet(DATA / "panel_yearly.parquet")

# Quintile assignment exactly as nb09 (firm-year level, within-year qcut on
# lagged sentiment, over the monthly analytical panel), headline window.
fy = (panel_monthly[(panel_monthly["year"] >= 2013) & (panel_monthly["year"] <= 2023)]
      .groupby(["gvkey", "year"])[["sentiment_overall_lag", "n_reviews_lag"]]
      .first().reset_index())
fy["quintile"] = (fy.groupby("year")["sentiment_overall_lag"]
                  .transform(lambda x: pd.qcut(x, q=5, labels=[1, 2, 3, 4, 5])))

# December market equity per firm-year (as nb08's Table 2 construction).
me_dec = (panel_monthly[panel_monthly["month"] == 12]
          [["gvkey", "year", "me"]].rename(columns={"year": "fyear"}))

chars = panel_yearly.merge(me_dec, on=["gvkey", "fyear"], how="left")
chars["book_to_market"] = chars["seq"] / chars["me"]
chars["me_bn"] = chars["me"] / 1_000  # me is in $ millions -> billions

merged = fy.merge(chars, left_on=["gvkey", "year"], right_on=["gvkey", "fyear"],
                  how="left", suffixes=("", "_y"))

VARS = {
    "sentiment_overall_lag": "Sentiment (lagged)",
    "n_reviews_lag": "Number of reviews (lagged)",
    "me_bn": "Market equity ($ billion)",
    "log_at": "Log total assets",
    "book_to_market": "Book-to-market",
    "roa": "Return on assets",
    "operating_margin": "Operating margin",
    "leverage": "Leverage",
    "sales_growth": "Sales growth",
}
q_mean = merged.groupby("quintile", observed=True)[list(VARS.keys())].mean().T
q_mean.index = [VARS[v] for v in q_mean.index]
q_mean.columns = [f"Q{int(c)}" for c in q_mean.columns]
q_n = merged.groupby("quintile", observed=True).size()
q_n_funda = merged.dropna(subset=["fyear"]).groupby("quintile", observed=True).size()
q_mean.loc["Firm-years (sort)"] = q_n.values
q_mean.loc["Firm-years (with fundamentals)"] = q_n_funda.values

q_mean.to_csv(OUTPUT / "table_quintile_characteristics.csv")
print("\nQuintile characteristics (means, raw values):")
print(q_mean.round(3).to_string())

# sanity: market-equity sanity vs the SMB loading story (Q5 larger than Q1)
assert q_mean.loc["Market equity ($ billion)", "Q5"] > q_mean.loc["Market equity ($ billion)", "Q1"]

# --------------------------------------------------------------- 3. FYE share
ana = panel_yearly.dropna(subset=["sentiment_overall_lag"]).copy()
ana["fye_month"] = pd.to_datetime(ana["datadate"]).dt.month
fy_share = (ana["fye_month"] != 12).mean()
firm_share = (ana.groupby("gvkey")["fye_month"].agg(lambda m: (m != 12).any())).mean()
dist = ana["fye_month"].value_counts().sort_index()

out = pd.DataFrame({
    "measure": ["firm_years_non_december_share", "firms_any_non_december_share",
                "firm_years_total", "firms_total"],
    "value": [fy_share, firm_share, len(ana), ana["gvkey"].nunique()],
})
out.to_csv(OUTPUT / "fye_share.csv", index=False)
print(f"\nNon-December fiscal year end: {fy_share:.1%} of firm-years "
      f"({firm_share:.1%} of firms have at least one non-December FYE; "
      f"N = {len(ana):,} firm-years, {ana['gvkey'].nunique()} firms)")
print("FYE month distribution:")
print(dist.to_string())
print("\nAll Tier 2 exports written.")
