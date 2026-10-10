#!/usr/bin/env python3
"""How much news reaches each brief, from committed findings (offline).

Per run: tickers whose NEWS ARTICLES block holds no article (an article is
a dict with a non-empty title; NewsAPI's null placeholder and the "No
articles found" message count as none), articles in total, and articles
that do not name the company.

Naming rule: an article names the company if its title or description
contains the company's short name (the first word of the stock block's
company_name with ".com" and trailing punctuation removed, case-insensitive)
OR the ticker (as a whole word, case-sensitive). A ticker without a
company_name ("N/A") is matched on the ticker only.

The query that fetches them: agent/tools/news.py:23-30 (five outlets via
`sources`, `"<name>" stock OR earnings OR investor` with no parentheses).

  python eval/news_coverage.py 4hsn2 nstp9 vks4c 2mzdd 9jzmj j4cnp kcf7s
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval.context_blocks import run_blocks  # noqa: E402

RULE = ("an article names the company if its title or description contains the short name "
        "(first word of company_name, '.com' and trailing punctuation removed, case-insensitive) "
        "or the ticker (whole word, case-sensitive)")


def short_name(company_name: str | None) -> str | None:
    if not company_name or company_name == "N/A":
        return None
    first = company_name.split()[0].replace(".com", "").rstrip(",.")
    return first or None


def names_company(article: dict, ticker: str, company_name: str | None) -> bool:
    text = f"{article.get('title') or ''} {article.get('description') or ''}"
    name = short_name(company_name)
    if name and name.lower() in text.lower():
        return True
    return re.search(rf"(?<![A-Za-z]){re.escape(ticker)}(?![A-Za-z])", text) is not None


def articles(news) -> list[dict]:
    return [a for a in (news if isinstance(news, list) else [])
            if isinstance(a, dict) and a.get("title")]


def run_coverage(run: str) -> dict:
    per = run_blocks(ROOT / "eval" / "runs" / "raw" / f"{run}-findings")
    zero, total, unnamed = [], 0, []
    for t, b in sorted(per.items()):
        arts = articles(b["news"])
        if not arts:
            zero.append(t)
        total += len(arts)
        company = (b["stock"] or {}).get("company_name")
        unnamed += [(t, a["title"]) for a in arts if not names_company(a, t, company)]
    return {"run": run, "tickers": len(per), "zero": zero, "articles": total, "unnamed": unnamed}


def main(argv=None) -> int:
    runs = argv if argv is not None else sys.argv[1:]
    if not runs:
        print(__doc__)
        return 2
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"Rule: {RULE}")
    for run in runs:
        r = run_coverage(run)
        print(f"{r['run']}: {len(r['zero'])}/{r['tickers']} tickers with zero articles; "
              f"{r['articles']} articles; {len(r['unnamed'])}/{r['articles']} do not name the company")
        print(f"  zero articles: {', '.join(r['zero'])}")
        for t, title in r["unnamed"]:
            print(f"  not named: {t}: {title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
