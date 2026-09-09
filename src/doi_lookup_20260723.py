#!/usr/bin/env python3
"""Look up authoritative DOIs for the 42 DOI-less journal articles in the thesis.
Rejects preprints/SSRN. Accepts only when title, first author, and journal agree."""
import json, time, urllib.parse, urllib.request
from difflib import SequenceMatcher

# (key, first_author_surname, year, journal, title)
REFS = [
 ("andrews1993","Andrews",1993,"Econometrica","Tests for parameter instability and structural change with unknown change point"),
 ("bebchuk2013","Bebchuk",2013,"Journal of Financial Economics","Learning and the disappearing association between governance and returns"),
 ("becker1996","Becker",1996,"Academy of Management Journal","The impact of human resource management on organizational performance: Progress and prospects"),
 ("benabou2010","Bénabou",2010,"Economica","Individual and corporate social responsibility"),
 ("boustanifar2022","Boustanifar",2022,"Financial Analysts Journal","Employee satisfaction and long-run stock returns, 1984-2020"),
 ("carhart1997","Carhart",1997,"The Journal of Finance","On persistence in mutual fund performance"),
 ("chen2023","Chen",2023,"Journal of Economic Dynamics and Control","Employee sentiment and stock returns"),
 ("chow1960","Chow",1960,"Econometrica","Tests of equality between sets of coefficients in two linear regressions"),
 ("combs2006","Combs",2006,"Personnel Psychology","How much do high-performance work practices matter? A meta-analysis of their effects on organizational performance"),
 ("core2006","Core",2006,"The Journal of Finance","Does weak governance cause weak stock returns? An examination of firm operating performance and investors expectations"),
 ("daniel1997b","Daniel",1997,"The Journal of Finance","Measuring mutual fund performance with characteristic-based benchmarks"),
 ("daniel1997a","Daniel",1997,"The Journal of Finance","Evidence on the characteristics of cross sectional variation in stock returns"),
 ("edmans2011","Edmans",2011,"Journal of Financial Economics","Does the stock market fully value intangibles? Employee satisfaction and equity prices"),
 ("edmans2012","Edmans",2012,"Academy of Management Perspectives","The link between job satisfaction and firm value, with implications for corporate social responsibility"),
 ("edmans2024","Edmans",2024,"Management Science","Employee satisfaction, labor market flexibility, and stock returns around the world"),
 ("eisfeldt2013","Eisfeldt",2013,"The Journal of Finance","Organization capital and the cross-section of expected returns"),
 ("faleye2006","Faleye",2006,"Journal of Financial and Quantitative Analysis","When labor has a voice in corporate governance"),
 ("faleye2011","Faleye",2011,"Journal of Business Ethics","Labor-friendly corporate practices: Is what is good for employees good for shareholders?"),
 ("famafrench2008","Fama",2008,"The Journal of Finance","Dissecting anomalies"),
 ("gompers2003","Gompers",2003,"The Quarterly Journal of Economics","Corporate governance and equity prices"),
 ("gorton2022","Gorton",2022,"Annual Review of Financial Economics","Corporate culture"),
 ("graham2022","Graham",2022,"Journal of Financial Economics","Corporate culture: Evidence from the field"),
 ("green2019","Green",2019,"Journal of Financial Economics","Crowdsourced employer reviews and stock returns"),
 ("guiso2015","Guiso",2015,"Journal of Financial Economics","The value of corporate culture"),
 ("hales2018","Hales",2018,"Accounting, Organizations and Society","A new era of voluntary disclosure? Empirical evidence on how employee postings on social media relate to future corporate disclosures"),
 ("hartzmark2019","Hartzmark",2019,"The Journal of Finance","Do investors value sustainability? A natural experiment examining ranking and fund flows"),
 ("harvey2016","Harvey",2016,"The Review of Financial Studies","and the cross-section of expected returns"),
 ("hong2009","Hong",2009,"Journal of Financial Economics","The price of sin: The effects of social norms on markets"),
 ("jiang2012","Jiang",2012,"Academy of Management Journal","How does human resource management influence organizational outcomes? A meta-analytic investigation of mediating mechanisms"),
 ("khan2016","Khan",2016,"The Accounting Review","Corporate sustainability: First evidence on materiality"),
 ("lins2017","Lins",2017,"The Journal of Finance","Social capital, trust, and firm performance: The value of corporate social responsibility during the financial crisis"),
 ("luca2016","Luca",2016,"Management Science","Fake it till you make it: Reputation, competition, and Yelp review fraud"),
 ("mayzlin2014","Mayzlin",2014,"American Economic Review","Promotional reviews: An empirical investigation of online review manipulation"),
 ("mclean2016","McLean",2016,"The Journal of Finance","Does academic research destroy stock return predictability?"),
 ("merton1987","Merton",1987,"The Journal of Finance","A simple model of capital market equilibrium with incomplete information"),
 ("newey1987","Newey",1987,"Econometrica","A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix"),
 ("pastor2022","Pástor",2022,"Journal of Financial Economics","Dissecting green returns"),
 ("pedersen2021","Pedersen",2021,"Journal of Financial Economics","Responsible investing: The ESG-efficient frontier"),
 ("posthuma2013","Posthuma",2013,"Journal of Management","A high performance work practices taxonomy: Integrating the literature and directing future research"),
 ("riedl2017","Riedl",2017,"The Journal of Finance","Why do investors hold socially responsible mutual funds?"),
 ("sheng2025","Sheng",2025,"The Review of Asset Pricing Studies","Asset pricing in the information age: Employee expectations and stock returns"),
 ("symitsi2021","Symitsi",2021,"European Journal of Operational Research","The informational value of employee online reviews"),
]

def norm(s):
    s = s.lower()
    for ch in '.,:;?!“”"\'()[]—–-…/&':
        s = s.replace(ch, ' ')
    return ' '.join(s.split())

def jtokens(s):
    return set(norm(s).split()) - {"the","of","and","a","journal"}

PREPRINT = ("ssrn","working paper","preprint","social science research network","review of finance conference")

def fetch(query):
    url = "https://api.crossref.org/works?rows=6&select=DOI,title,author,issued,container-title,type&query.bibliographic=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "thesis-refcheck/1.0 (mailto:refcheck@example.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]["items"]

results = {}
report = []
for key, author, year, journal, title in REFS:
    q = f"{title} {author} {journal} {year}"
    try:
        items = fetch(q)
    except Exception as e:
        report.append((key, "ERROR", str(e)[:60], "")); results[key] = None; time.sleep(0.4); continue
    best = None
    for it in items:
        ct = (it.get("container-title") or [""])[0]
        ctitle = (it.get("title") or [""])[0]
        if not ctitle: continue
        tsim = SequenceMatcher(None, norm(title), norm(ctitle)).ratio()
        fam = (it.get("author") or [{}])[0].get("family","")
        author_ok = norm(author).split()[-1] in norm(fam) if fam else False
        yr = (it.get("issued",{}).get("date-parts") or [[None]])[0][0]
        year_ok = yr in (year-1, year, year+1) if yr else False
        jt_ref, jt_cand = jtokens(journal), jtokens(ct)
        jsim = len(jt_ref & jt_cand)/max(1,len(jt_ref)) if jt_ref else 0
        is_pre = any(p in ct.lower() for p in PREPRINT) or it.get("type")=="posted-content"
        score = tsim + 0.5*author_ok + 0.3*year_ok + 0.5*jsim - (5 if is_pre else 0)
        cand = dict(doi=it.get("DOI"), tsim=tsim, author_ok=author_ok, year_ok=year_ok,
                    jsim=jsim, is_pre=is_pre, ct=ct, yr=yr, score=score)
        if best is None or score > best["score"]:
            best = cand
    # Accept rule: strong title, author agrees, journal agrees (or title near-exact), not a preprint
    ok = (best and not best["is_pre"] and best["author_ok"] and best["tsim"]>=0.80
          and (best["jsim"]>=0.5 or best["tsim"]>=0.92))
    if ok:
        results[key] = best["doi"]
        report.append((key, "OK", best["doi"], f"t={best['tsim']:.2f} j={best['jsim']:.2f} y={best['yr']} [{best['ct'][:30]}]"))
    else:
        results[key] = None
        d = best["doi"] if best else "-"
        why = "preprint-only" if (best and best["is_pre"]) else "weak"
        report.append((key, "FLAG", d or "-", (f"t={best['tsim']:.2f} j={best['jsim']:.2f} y={best['yr']} pre={best['is_pre']} [{best['ct'][:30]}]" if best else "no hits")))
    time.sleep(0.35)

json.dump(results, open("doi_map.json","w"), indent=0)
print(f"{'KEY':16} {'STATUS':5} {'DOI':34} DETAIL")
for k,s,d,det in report:
    print(f"{k:16} {s:5} {str(d):34} {det}")
ok = sum(1 for v in results.values() if v)
print(f"\nAccepted {ok}/{len(REFS)};  flagged {len(REFS)-ok}")
