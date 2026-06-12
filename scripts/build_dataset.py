#!/usr/bin/env python3
"""Stage B of the LoRA dataset pipeline: deterministic, Claude-free target builders.

Turns data/raw_research.jsonl (raw stock / news / filing text) into
data/sections_dataset.jsonl — instruction/target pairs for the 4 brief sections,
in ChatML-style `messages` format.

Every target is built deterministically from the raw data by the four builders
below — NO LLM is called, so the dataset is genuinely Claude-free:
  · Financial Health     — real figures slotted into rotating sentence templates
  · Recent Developments  — extractive summary of real news titles/sources
  · SEC Filing Highlights— top financial-signal sentences from the raw 10-K MD&A
  · Risk Factors         — leading risk sentences from the raw filing's risk region

The INPUT for each example is the same `_data_context(...)`-style string the live
pipeline feeds Haiku, except the SEC portion is the raw `_fetch_filing_text`
narrative (Claude-free) rather than RAG chunks — matching the training intent.

These functions are mirrored verbatim in fine_tune_financial.ipynb so the
notebook shows the construction inline; this module lets the same pipeline run
from the CLI and be unit-tested.
"""
import os
import re
import sys
import json
import html
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core import _SECTIONS  # the 4 (heading, instruction) pairs the live agent uses

DATA_DIR = Path(__file__).parent.parent / "data"
RAW_PATH = DATA_DIR / "raw_research.jsonl"
OUT_PATH = DATA_DIR / "sections_dataset.jsonl"

SEC_CONTEXT_CAP = 3500  # chars of raw filing text put into the input context


# ── number formatting ───────────────────────────────────────────────────────────

def _money(v) -> str | None:
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    a = abs(v)
    if a >= 1e12:
        return f"${v / 1e12:.2f} trillion"
    if a >= 1e9:
        return f"${v / 1e9:.1f} billion"
    if a >= 1e6:
        return f"${v / 1e6:.1f} million"
    return f"${v:,.0f}"


def _pct(v) -> str | None:
    """Format a fraction (0.27 -> '27.0%'). For ratios stored as fractions."""
    try:
        return f"{float(v) * 100:.1f}%"
    except (TypeError, ValueError):
        return None


def _yield_pct(v) -> str | None:
    """yfinance reports dividend_yield already in percent units (0.37 == 0.37%),
    so it must NOT be multiplied by 100 like profit_margin is."""
    try:
        return f"{float(v):.2f}%"
    except (TypeError, ValueError):
        return None


_PUNCT_MAP = {
    "’": "'", "‘": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...", " ": " ",
    "�": "",  # actual replacement char, if any
}


def _clean(text: str) -> str:
    """Normalize smart punctuation to ASCII and collapse whitespace so curly
    quotes / em-dashes / stray encodings don't leak into targets."""
    if not text:
        return ""
    text = html.unescape(text)  # decode &#160; &amp; etc. left over from filing HTML
    for bad, good in _PUNCT_MAP.items():
        text = text.replace(bad, good)
    return re.sub(r"\s+", " ", text).strip()


def _num(v, suffix="") -> str | None:
    try:
        return f"{float(v):.1f}{suffix}"
    except (TypeError, ValueError):
        return None


# ── Builder 1: Financial Health (templated from real figures) ───────────────────

def build_financial_health(stock: dict, company: str, ticker: str) -> str | None:
    price = stock.get("current_price")
    mcap = _money(stock.get("market_cap"))
    revenue = _money(stock.get("revenue"))
    net_income = _money(stock.get("net_income"))
    margin = _pct(stock.get("profit_margin"))
    pe = _num(stock.get("pe_ratio"), "x")
    fpe = _num(stock.get("forward_pe"), "x")
    sector = stock.get("sector")

    if price is None or (mcap is None and revenue is None):
        return None  # not enough to say anything grounded

    # Valuation phrasing keyed off the P/E level (deterministic, not invented).
    try:
        pe_val = float(stock.get("pe_ratio"))
        valuation = ("a premium valuation" if pe_val >= 30
                     else "a moderate valuation" if pe_val >= 15
                     else "a value-oriented multiple")
    except (TypeError, ValueError):
        valuation = None

    clauses = []
    trades = f"{company} trades at ${float(price):.2f} per share"
    if sector:
        trades += f" in the {sector.lower()} sector"
    clauses.append(trades + ".")

    if mcap:
        val = f"It carries a market capitalization of {mcap}"
        if pe:
            val += f" and a P/E ratio of {pe}"
            if fpe:
                val += f" ({fpe} forward)"
        if valuation:
            val += f", {valuation}"
        clauses.append(val + ".")

    if revenue or net_income or margin:
        parts = []
        if revenue:
            parts.append(f"{revenue} in annual revenue")
        if net_income:
            parts.append(f"{net_income} in net income")
        prof = "The company reports " + " and ".join(parts) if parts else "The company operates"
        if margin:
            prof += f", a net profit margin of {margin}"
        clauses.append(prof + ".")

    # Rotate the closing emphasis deterministically for surface variety.
    variant = sum(ord(c) for c in ticker) % 3
    hi, lo = stock.get("week_52_high"), stock.get("week_52_low")
    if variant == 0 and hi and lo:
        clauses.append(
            f"Over the past year the stock has ranged between ${float(lo):.2f} and ${float(hi):.2f}.")
    elif variant == 1 and stock.get("dividend_yield"):
        dy = _yield_pct(stock.get("dividend_yield"))
        if dy:
            clauses.append(f"It currently offers a dividend yield of {dy}.")

    return "### Financial Health\n" + " ".join(clauses)


# ── Builder 2: Recent Developments (extractive from real news) ───────────────────

def _first_sentence(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    m = re.split(r"(?<=[.!?])\s+", text)
    return m[0].strip()


def build_recent_developments(news: list) -> str | None:
    articles = [a for a in (news or []) if isinstance(a, dict) and a.get("title")][:3]
    if not articles:
        return None

    a0 = articles[0]
    lead = f'Recent coverage includes "{_clean(a0["title"])}"'
    if a0.get("source"):
        lead += f' ({_clean(a0["source"])})'
    lead += "."
    desc = _clean(_first_sentence(a0.get("description")))
    if desc:
        lead += f" {desc}{'' if desc.endswith(('.', '!', '?')) else '.'}"

    extra = []
    for a in articles[1:]:
        t = _clean(a["title"])
        extra.append(f'"{t}" ({_clean(a["source"])})' if a.get("source") else f'"{t}"')
    body = f" Additional headlines: {' and '.join(extra)}." if extra else ""

    return "### Recent Developments\n" + lead + body


# ── Builder 3 & 4: extractive helpers over raw filing text ──────────────────────

# Legal/disclaimer/exhibit boilerplate to drop before ranking, so the targets
# carry business content rather than filing scaffolding.
_BOILERPLATE = (
    "forward-looking statement", "forward looking statement", "private securities litigation",
    "securities act", "exchange act", "incorporated by reference", "table of contents",
    "see item", "see part", "pursuant to", "subsidiaries", "jurisdiction",
    "certificate of formation", "certificate of incorporation", "anti-takeover",
    "annual report on form", "quarterly report on form", "this report", "cautionary",
    "undue reliance", "as defined in", "the sec", "guidance issued",
    "unless otherwise stated", "all information presented", "fiscal calendar",
    "accompanying notes", "in conjunction with", "should be read", "refer to the",
    "is not an indication", "the discussion of", "set forth below", "described below",
    # Descriptive / non-analytical sentences (company profile, products, channels)
    # that score on financial terms but carry no analytical value.
    "fiscal year is", "week period", "founded in", "develop and support",
    "sells its products", "resells", "directly to customers", "retail and online",
    "distribution channels", "our products include", "wholly-owned",
)


def _is_boilerplate(s: str) -> bool:
    sl = s.lower()
    if any(b in sl for b in _BOILERPLATE):
        return True
    # Page furniture flattened into the text: pipes, running form headers, and
    # embedded "Item 7A." / "Item 8" header/footer fragments.
    if "|" in s:
        return True
    if re.search(r"\bform\s*10-[kq]\b", sl):
        return True
    if re.search(r"\bitem\s*\d+[a-z]?[\.\s]", sl):
        return True
    if "discussion and analysis of financial condition" in sl:
        return True
    # Drop header-like fragments that are mostly Capitalized Words (no real sentence).
    words = s.split()
    if words and sum(w[0].isupper() for w in words if w[0].isalpha()) / len(words) > 0.7:
        return True
    return False


def _sentences(text: str) -> list[str]:
    text = _clean(text)
    raw = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for s in raw:
        s = s.strip()
        # Strip leading page-number / "Part I" furniture (e.g. "1 Part I Supervision...").
        s = re.sub(r"^(\d+\s+)?(part\s+[ivx]+\s+)?", "", s, flags=re.I).strip()
        if not (60 <= len(s) <= 300):
            continue
        letters = sum(c.isalpha() for c in s)
        if letters / max(len(s), 1) < 0.6:   # skip tables / numeric noise
            continue
        if len(s.split()) < 8:
            continue
        if _is_boilerplate(s):
            continue
        out.append(s)
    return out


def clean_sentence_count(text: str | None, terms: set, min_score: int) -> int:
    """How many non-boilerplate sentences clear the term-score bar — the yield
    metric used to verify the filtering before scaling."""
    if not text:
        return 0
    return sum(1 for s in _sentences(text) if _score(s, terms) >= min_score)


_HIGHLIGHT_TERMS = {
    "revenue", "sales", "growth", "grew", "increased", "decreased", "margin",
    "operating", "income", "net", "billion", "million", "fiscal", "quarter",
    "segment", "demand", "products", "services", "customers", "cash", "earnings",
    "performance", "results", "year", "operations",
}

_RISK_TERMS = {
    "risk", "risks", "adversely", "adverse", "could", "decline", "fail",
    "failure", "competition", "competitive", "regulatory", "regulation",
    "litigation", "uncertain", "uncertainty", "volatility", "disrupt",
    "unable", "negative", "loss", "losses", "harm", "materially",
}


def _score(sentence: str, terms: set) -> int:
    words = re.findall(r"[a-z]+", sentence.lower())
    return sum(1 for w in words if w in terms)


def build_sec_highlights(sec_raw: dict) -> str | None:
    # Item 7 (MD&A) is where management discusses results; fall back to risk text.
    text = sec_raw.get("mda") or sec_raw.get("risk_factors")
    if not text:
        return None
    sents = _sentences(text)
    if not sents:
        return None
    # An analytical highlight is either rich in financial terms (>=3) or a
    # figure-bearing result sentence (a real $/% amount with >=1 term). A bare
    # year/count no longer counts: descriptive sentences (fiscal-year
    # definitions, founding statements, distribution channels, product listings)
    # carry few financial terms and no $/%, so they fail both gates — and the
    # named ones are also caught by _BOILERPLATE. NB: many 10-Ks keep figures in
    # tables (flattened to number-soup, dropped by _sentences), so a hard
    # figure-only gate would wrongly discard whole sections.
    def has_figure(s):
        return bool(re.search(r"\$\s?\d|\d+(?:\.\d+)?\s?%|\bpercent\b", s))

    def qualifies(s):
        sc = _score(s, _HIGHLIGHT_TERMS)
        return sc >= 3 or (has_figure(s) and sc >= 1)

    def rank(s):  # prefer figure-bearing, term-rich sentences
        return _score(s, _HIGHLIGHT_TERMS) + (2 if has_figure(s) else 0)

    cands = [(i, s) for i, s in enumerate(sents) if qualifies(s)]
    cands.sort(key=lambda p: rank(p[1]), reverse=True)
    top = cands[:4]
    if len(top) < 2:
        return None
    top.sort(key=lambda p: p[0])  # restore document order
    return "### SEC Filing Highlights\n" + " ".join(s for _, s in top)


# Modal/risk-framing words that mark a real risk statement (vs a product
# description). A sentence qualifies as a risk bullet if it is risk-term-dense
# (>=2) OR has >=1 risk term AND a modal — so declarative risks like "the
# markets are highly competitive" (score 2) stay, single-weak-term product
# descriptions like the AppleCare bullet ("...theft and loss...", score 1, no
# modal) are dropped, and single-term-with-modal risks recover coverage.
_RISK_MODALS = ("could", "may", "might", "would", "adversely", "adverse",
                "subject to", "risk", "uncertain", "materially", "fail")


def build_risk_factors(sec_raw: dict) -> str | None:
    # Item 1A (Risk Factors) region, already isolated during harvest.
    text = sec_raw.get("risk_factors")
    if not text:
        return None
    sents = _sentences(text)

    def is_risk(s):
        sc = _score(s, _RISK_TERMS)
        if sc >= 2:
            return True
        sl = s.lower()
        return sc >= 1 and any(m in sl for m in _RISK_MODALS)

    cands = [(i, s) for i, s in enumerate(sents) if is_risk(s)]
    cands.sort(key=lambda p: _score(p[1], _RISK_TERMS), reverse=True)
    top = cands[:3]
    if len(top) < 2:
        return None
    top.sort(key=lambda p: p[0])
    bullets = "\n".join(f"- {s}" for _, s in top)
    return "### Risk Factors\n" + bullets


_BUILDERS = {
    "### Financial Health":      lambda r: build_financial_health(r["stock"], r["company_name"], r["ticker"]),
    "### Recent Developments":   lambda r: build_recent_developments(r["news"]),
    "### SEC Filing Highlights": lambda r: build_sec_highlights(r["sec_raw"]),
    "### Risk Factors":          lambda r: build_risk_factors(r["sec_raw"]),
}

# Sections the fine-tuned local model is trained on and serves. Two sections are
# deliberately excluded and kept on Haiku because deterministic extraction can't
# build grounded targets for them:
#   - Recent Developments: NewsAPI coverage is too sparse (18%).
#   - SEC Filing Highlights: MD&A figures are table-bound (flatten to number-soup)
#     and the remaining prose is descriptive, not analytical.
# Keep this list in sync with LOCAL_SECTIONS in agent/tools/local_model.py.
LOCAL_SECTIONS = ["### Financial Health", "### Risk Factors"]


# ── input context (mirrors _data_context but with raw, Claude-free SEC text) ─────

def train_context(stock: dict, news: list, sec_raw: dict, cap: int = SEC_CONTEXT_CAP) -> str:
    # SEC portion = raw Item 7 (MD&A) + Item 1A (Risk Factors) excerpts, capped.
    # Claude-free and aligned with what the section builders draw from.
    sec = {}
    if sec_raw.get("mda"):
        sec["MD&A"] = sec_raw["mda"][:cap]
    if sec_raw.get("risk_factors"):
        sec["Risk Factors"] = sec_raw["risk_factors"][:cap]
    return f"Stock: {json.dumps(stock)}\nNews: {json.dumps(news)}\nSEC: {json.dumps(sec)}"


def section_prompt(heading: str, instruction: str, company: str, ticker: str, context: str) -> str:
    # Identical wording to agent.core._haiku_section so train/inference match.
    return (
        f"Write ONLY the '{heading}' section for a {company} ({ticker}) investment brief.\n"
        f"{instruction}\nStart with the markdown heading. Be concise.\n\nData:\n{context}"
    )


def build_examples(row: dict) -> list[dict]:
    context = train_context(row["stock"], row["news"], row["sec_raw"])
    instr = {h: i for h, i in _SECTIONS}
    examples = []
    for heading in LOCAL_SECTIONS:  # Recent Developments stays with Haiku
        target = _BUILDERS[heading](row)
        if not target:
            continue
        prompt = section_prompt(heading, instr[heading], row["company_name"], row["ticker"], context)
        examples.append({
            "ticker": row["ticker"],
            "section": heading,
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": target},
            ],
        })
    return examples


def main():
    parser = argparse.ArgumentParser(description="Build the LoRA section dataset (deterministic).")
    parser.add_argument("--raw", default=str(RAW_PATH))
    parser.add_argument("--out", default=str(OUT_PATH))
    parser.add_argument("--samples", type=int, default=5, help="How many sample rows to print.")
    args = parser.parse_args()

    rows = [json.loads(l) for l in open(args.raw, encoding="utf-8") if l.strip()]
    examples = [ex for row in rows for ex in build_examples(row)]

    with open(args.out, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    # ── coverage report ──
    by_section = {}
    for ex in examples:
        by_section[ex["section"]] = by_section.get(ex["section"], 0) + 1
    n = len(rows)
    print(f"Built {len(examples)} examples from {n} tickers -> {args.out}")
    print(f"(Recent Developments + SEC Filing Highlights excluded - Haiku keeps those.)")
    print(f"\nPer-section coverage (tickers producing an example / {n}):")
    for h in LOCAL_SECTIONS:
        c = by_section.get(h, 0)
        print(f"  {h:<28} {c:>3}/{n}  ({c/n*100:.0f}%)")

    # ── yield report: clean candidate sentences per SEC section per ticker ──
    print(f"\nFiltered-sentence yield for the two extractive sections "
          f"(clean candidates after boilerplate removal):")
    print(f"  {'Ticker':<8} {'MD&A(>=2)':>10} {'Risk(>=2)':>10}")
    print(f"  {'-'*8} {'-'*10} {'-'*10}")
    mda_counts, risk_counts = [], []
    for row in rows:
        s = row["sec_raw"]
        mc = clean_sentence_count(s.get("mda"), _HIGHLIGHT_TERMS, 2)
        rc = clean_sentence_count(s.get("risk_factors"), _RISK_TERMS, 2)
        mda_counts.append(mc)
        risk_counts.append(rc)
        print(f"  {row['ticker']:<8} {mc:>10} {rc:>10}")
    def _stat(xs):
        nz = [x for x in xs if x > 0]
        return f"min={min(xs)} max={max(xs)} mean={sum(xs)/len(xs):.1f} nonzero={len(nz)}/{len(xs)}"
    print(f"  MD&A  candidates:  {_stat(mda_counts)}")
    print(f"  Risk  candidates:  {_stat(risk_counts)}")
    print(f"\nSuggested split: {int(len(examples)*0.9)} train / {len(examples) - int(len(examples)*0.9)} val\n")

    print("=" * 80)
    print(f"  SCHEMA: {{ticker, section, messages:[{{role:user, content}}, {{role:assistant, content}}]}}")
    print("=" * 80)
    for ex in examples[: args.samples]:
        print(f"\n----- {ex['ticker']}  |  {ex['section']} -----")
        print("USER (input):")
        print(ex["messages"][0]["content"][:700] + (" ...[truncated]" if len(ex["messages"][0]["content"]) > 700 else ""))
        print("\nASSISTANT (deterministic target):")
        print(ex["messages"][1]["content"])


if __name__ == "__main__":
    main()
