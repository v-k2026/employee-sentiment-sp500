# Commit history of the analysis pipeline

Exported from the working repository on 2026-08-13. Oldest first.

| Commit | Date | Message |
|---|---|---|
| `728fe5b` | 2026-05-13 | Initial commit: gitignore |
| `5ceecb7` | 2026-05-13 | Add environment check notebook — all packages working, WRDS connected |
| `f33b80e` | 2026-05-13 | Add SP500 universe notebook — 6535 firm-year panel from fja05680 GitHub |
| `c3a9af3` | 2026-05-13 | Add SP500 universe notebook — 6535 firm-year panel from fja05680 GitHub |
| `3195f6b` | 2026-05-14 | Update 01 notebook documentation — correct sanity check results and add caveats |
| `61ce903` | 2026-05-14 | Add universe-to-gvkey mapping via comp.sec_idhist — 100% coverage |
| `9ed24f0` | 2026-05-14 | Document pre-committed weighting decision in notebook 03 |
| `a9559d6` | 2026-05-15 | Add CRSP returns panel — 97,701 firm-months, 98.5% universe coverage |
| `91dc0a7` | 2026-05-15 | Add Compustat fundamentals panel — 8,950 firm-years, 98.5% universe coverage |
| `5afbdc4` | 2026-05-15 | Add Fama-French + momentum factor panel — 156 months (2012-2024) |
| `a8bb209` | 2026-05-15 | Rename notebook 02: sentiment_panel → universe_to_gvkey |
| `7dc54a2` | 2026-05-15 | Add merged analytical panels — 81,089 firm-months (A), 6,778 firm-years (B) |
| `427e8e8` | 2026-05-21 | Add descriptive statistics — Table 1, correlations, sentiment trends |
| `22cb909` | 2026-05-21 | Add H1 portfolio sorts — full-sample null masks 2021-22 reversal |
| `c5e26b8` | 2026-05-21 | Add H2a alpha regression — alpha null (z=0.51), strong negative SMB loading |
| `be1e704` | 2026-05-21 | Add H2b operating performance — ROA (t=2.28) and sales growth (t=3.35) significant, margin null |
| `e7e493c` | 2026-05-21 | Add robustness checks — regime-dependence, sub-ratings, ROA fails falsification |
| `cd616bd` | 2026-05-22 | Add thesis figures notebook — 6 figures incl. sub-rating heatmap |
| `048acef` | 2026-05-31 | Verify headline results hold restricted to 2013-2023 (per JJ direction) |
| `33d9ed5` | 2026-06-10 | Commit pending notebook re-execution outputs (07-13) |
| `d0bcfb9` | 2026-06-10 | Fix dataset citation and stale markdown in notebooks 01-02 |
| `a290685` | 2026-06-10 | Add THESIS_PROJECT.md handoff document to version control |
| `c34e713` | 2026-06-10 | Add operational instructions for the identifier-fix session |
| `0c8f90f` | 2026-06-10 | Fix ticker->gvkey mapping: per-year assignment + 4 zombie-spell overrides + LS links + UAL rcid |
| `881e172` | 2026-06-10 | Re-run pipeline after identifier fix — all conclusions hold, decimals shift |
| `0499c63` | 2026-06-10 | Mark identifier fix adopted; propagate post-fix numbers to prose; remove relay file |
| `9306c6b` | 2026-06-11 | Draft methodology 3.3-3.6 (in v2 docx); add Newey-West 1987 to references |
| `07a5154` | 2026-06-11 | Gloss pass on lit review (11 plain-language first-use explanations); word-count update |
| `bc55e1f` | 2026-06-11 | Decline memo §6 rcid candidates; freeze sample numbers; log JJ timeline |
| `58def99` | 2026-06-11 | Add thesis_outline_v2.docx pointer (clean outline-only version for JJ) |
| `d2491b1` | 2026-06-11 | Fix intro methodology paragraph; drop orphaned Fama-MacBeth reference |
| `f1a381d` | 2026-06-11 | Americanize intro; create consolidated sections 1-3 draft docx |
| `2f333a3` | 2026-06-16 | Add 18 Edmans-snowball sources to references (44 total); log JJ word targets |
| `19806a4` | 2026-06-16 | Trim introduction to 980 words (JJ target 1,000) |
| `47567d5` | 2026-06-17 | Compress methodology to 2,126 words (no appendix) |
| `87f431c` | 2026-06-17 | Weave Harvey et al. (2016) into methodology sub-rating caveat |
| `e21aece` | 2026-06-17 | Rewrite lit review with 16 snowball sources integrated (3,791 words) |
| `1daab4f` | 2026-06-17 | Add reviewer-status disclosure to methodology 3.6 |
| `292fd0d` | 2026-06-17 | Complete literature folder: 14 snowball PDFs + Newey-West + BLS JOLTS; add index |
| `f2ba4b8` | 2026-06-19 | Draft Results chapter (ch4); drop Chen from references (43 entries) |
| `bff09ca` | 2026-06-19 | Regenerate Results figures to 2013-2023; archive full-sample versions |
| `b94ad44` | 2026-06-22 | Fix winsorization NaN-fill bug; reframe H2b (sales growth robust, ROA suggestive) |
| `b0e54dc` | 2026-06-22 | Restrict notebook 13 to 2013-2023 (was producing full-sample figures) |
| `480367d` | 2026-06-23 | Restrict nb11/nb12 to 2013-2023 so table CSVs reproduce the Results chapter |
| `38db412` | 2026-06-23 | Restrict nb08/nb10 to 2013-2023; fix variance decomposition to proper ANOVA |
| `7b3ed36` | 2026-06-23 | Refresh nb08/10/11/12 stored outputs to 2013-2023; add robustness CSV |
| `b7b3371` | 2026-06-23 | Refresh nb13 + nb08 inline figures to 2013-2023 |
| `9c2ab48` | 2026-06-23 | Update handoff doc: Results pipeline reproducibility closed (2026-06-23) |
| `d0b9d3e` | 2026-06-28 | Add notebook 14: factor decomposition of the 2021-22 reversal |
| `06ef24e` | 2026-06-29 | Add notebook 15: structural-break test of the sentiment long-short alpha |
| `c392378` | 2026-06-29 | Update handoff: Conclusion + Abstract drafted; all chapters 1-6 + abstract complete |
| `81324f6` | 2026-07-02 | Pre-commit membership-filter fix: inner-join panels on point-in-time S&P 500 membership |
| `285878a` | 2026-07-02 | Re-run pipeline 07-15 under membership filter; adopt post-fix numbers |
| `63d2462` | 2026-07-02 | Update handoff: membership-filter fix adopted; §3 banner with official post-fix numbers; decisions-log entry |
| `92b942b` | 2026-07-02 | nb13: winsorize before window restriction in sub-rating figure cells (caps now match notebooks 11-12; heatmap annotations agree with Table 5 prose to the last digit) |
| `b8790da` | 2026-07-02 | nb07: relabel pre-filter coverage diagnostic (was ambiguously labeled 'analytical sample'); re-executed, panels byte-identical |
| `244ff3a` | 2026-07-12 | Pre-commit shift-fix: fiscal-year-based lags replace positional/pad-filled ones |
| `8dbd845` | 2026-07-12 | Re-run 07-13 under shift-fix; adopt (materiality rule not crossed) |
| `5e1df66` | 2026-07-12 | nb12: correct header pre-commitment claim (specs 1-3 pre-committed in 9ed24f0; falsification/sub-ratings pre-specified, committed with results in e7e493c) |
| `49c3c9e` | 2026-07-14 | Pre-commit D3: value-weighted spread alpha + Newey-West lag sensitivity + fig2 95% CI |
| `5d0a6af` | 2026-07-14 | Run D3: VW alpha marginal (3.53%/yr, t=1.76), EW null lag-insensitive; fig2 now 95% CI |
| `ac01a08` | 2026-07-22 | Pre-commit Tier 2 exports: sub-period loadings, quintile characteristics, FYE share |
| `292ee60` | 2026-07-22 | Run Tier 2 exports: gates passed, run record appended |
| `4fc1dfe` | 2026-07-23 | Add DOI lookup for reference list (Crossref-verified, 42/42) |
| `d7ea953` | 2026-08-13 | Commit value-weighted concentration diagnostic (post-hoc, written 2026-08-06) |
