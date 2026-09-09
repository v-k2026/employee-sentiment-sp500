# Does Worker Wellbeing Pay Off? — analysis pipeline

Code behind the bachelor's thesis *"Does Worker Wellbeing Pay Off? Employee Sentiment,
Operating Performance, and Risk-Adjusted Stock Returns in the S&P 500, 2013–2023"*
(Volodymyr Kotselko, WU Vienna, 2026).

This repository is a code release. It contains the pipeline that produced every number,
table and figure in the thesis, plus the memos documenting the three data corrections
disclosed in Section 3.6. The development history of the pipeline is listed in
[`COMMIT_LOG.md`](COMMIT_LOG.md); the original working repository is available from the author.

## What is here

| Path | Contents |
|---|---|
| `notebooks/00`–`07` | Data construction: environment check, S&P 500 universe, identifier resolution, sentiment, returns, fundamentals, factors, merged panels |
| `notebooks/08`–`13` | Analysis: descriptives, portfolio sorts (H1), alpha regression (H2a), operating performance (H2b), robustness (Section 4.5), figures |
| `notebooks/14`–`15` | Factor decomposition of the 2021–22 dip; structural-break tests |
| `src/` | Helper scripts: sales-growth lag patch (2026-07-12), Tier 2 exhibit exports, Crossref DOI lookup for the reference list |
| `docs/` | Audit memos for the identifier fix, the membership-filter fix, and the lag ("shift") fix |

Run the notebooks in numerical order. Notebooks 00–06 pull from WRDS; 07 onward operate on
the stored panels and can be re-run offline once the panels exist.

## Which exhibit is which

Notebook 13 writes the figures under their own file names, which do not follow the numbering
in the thesis. The old Figure 6 was dropped and the old Figure 3 moved to Appendix B, so the
two sequences diverge:

| Thesis | File written by notebook 13 |
|---|---|
| Figure 1 (quintile returns) | `fig3_quintile_returns.png` |
| Figure 2 (long–short spread by year) | `fig1_long_short_by_year.png` |
| Figure 3 (alpha by window, 95% CI) | `fig2_regime_alpha.png` |
| Figure 4 (cumulative value of one dollar) | `fig5_cumulative_ls.png` |
| Figure 5 (sub-rating heatmap) | `fig6_subrating_heatmap.png` |
| Figure B1 (quintiles year by year) | `fig7_quintile_by_year.png` |

`fig4_subratings.png` is still generated but is not used in the thesis; the heatmap replaced
it as Figure 5.

The tables come from these artifacts, all written to `output/`:

| Thesis | Artifact | Written by |
|---|---|---|
| Table 1 (descriptives) | `table1_summary_stats.csv` | notebook 08 |
| Table 2 (correlations) | `table_correlations.csv` | notebook 08 |
| Table 3 (alpha and loadings) | `table_alpha_regression.csv`, `table_alpha_subperiod.csv` | notebook 10, `src/tier2_exports_20260722.py` |
| Table 4 (panel regressions) | `table_operating_performance.csv` | notebook 11 |
| Table 5 (robustness) | `table_robustness.csv` | notebook 12 |
| Table B1 (quintile characteristics) | `table_quintile_characteristics.csv` | `src/tier2_exports_20260722.py` |

## Data is not included

`data/` and `output/` are excluded. The inputs come from CRSP, Compustat North America and
Revelio Labs, all licensed through Wharton Research Data Services, and cannot be
redistributed. Reproducing the panels requires a WRDS subscription covering those three
sources; the S&P 500 constituent history is public
([fja05680/sp500](https://github.com/fja05680/sp500)) and the factor returns come from the
Kenneth R. French Data Library.

Derived panels can be provided directly to WRDS-authorized users on request.

## Environment

```bash
conda env create -f environment.yml
conda activate thesis
```

Python 3.11.15, pandas 2.2.3, numpy 2.4.4, scipy 1.17.1, statsmodels 0.14.6,
linearmodels 7.0, pyarrow 24.0.0.

## Paths and credentials

The notebooks resolve paths as `~/thesis/data` and `~/thesis/output`, so clone this
repository to `~/thesis` (or edit the `DATA_PROCESSED` / `OUTPUT` constants in the imports
cell of each notebook).

WRDS credentials are read at runtime from `~/.pgpass`; nothing is stored in this
repository. The WRDS username visible in the stored login prompts of notebooks 00 and 06
has been replaced with `<wrds-username>`.

## Specification pre-commitment

Section 3.5 of the thesis states that the aggregation rule, the equal-weighting choice, the
unweighted headline panel, the review-count threshold and the precision-weighting method
were fixed before the outcome data were retrieved. The corresponding commits are in
`COMMIT_LOG.md`:

- `9ed24f0` (2026-05-14) — pre-committed specifications, recorded the day before the return
  and accounting data were pulled
- `e7e493c` (2026-05-21) — falsification and sub-rating designs, committed together with
  their first results, and therefore described in the thesis as pre-specified rather than
  pre-committed

Each of the three data corrections was likewise committed before the pipeline was re-run:
`81324f6` → `285878a` for the membership filter and `244ff3a` → `8dbd845` for the lag fix,
with the before-and-after comparisons in `docs/`.
