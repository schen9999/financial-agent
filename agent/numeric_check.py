"""Deterministic numeric check: do the stock-data figures a brief states match
the stock data the pipeline fetched?

No LLM, no network, stdlib only, pure functions. The grounding judge audits
only the Executive Summary and Outlook; this check reads every section, but
only for the nine fields of the STOCK DATA block (current_price, market_cap,
pe_ratio, forward_pe, week_52_high, week_52_low, revenue, net_income,
profit_margin), and only where the brief binds a number to one of those
field labels in the same clause ("market capitalization of $16.8 billion",
"$4.3 billion in annual revenue", "P/E of 31.0x", "**Revenue**: $96.6M").

Scope rules, chosen for precision over coverage:
  - A number with no recognized label is never assigned a field; it is
    counted as unchecked so coverage is reportable.
  - A labeled number is also left unchecked (with a reason) when the clause
    ties it to another period or quantity than the stock snapshot: a year,
    quarter, fiscal/prior-year wording, "since inception" and similar
    ("period"); a revenue line qualified by a segment word ("services
    revenue", "subline"); a bound instead of a value ("over $1 billion",
    "bound"); the wrong form for the field (a margin without %, a price
    with an x-suffix, "form"); or a field the stock dict does not have
    ("no_source"). News and filing numbers are out of scope by design.
  - Tolerance: relative (default 2%) plus the rounding the stated precision
    implies ("$16.8 billion" also covers 16.75-16.85B). A hedged figure
    ("approximately $400 million") treats integer trailing zeros as
    rounding too (+-50M there), an unhedged one does not.
  - profit_margin in the dict is a fraction; the text states percent.

Placeholders are flagged too: bracketed template tokens ([City Name],
[Company], [X]), {curly} template slots, literal "$X" figures, and "N/A"-style
fillers bound to a field the stock dict does have.

Wiring (agent/core.py): NUMERIC_CHECK=off|warn|block, default warn. warn
appends a short "Numeric check" note listing findings; block also replaces
every section holding a mismatch with a one-line notice; off skips the call.
"""
import os
import re

FIELDS = ("current_price", "market_cap", "pe_ratio", "forward_pe",
          "week_52_high", "week_52_low", "revenue", "net_income",
          "profit_margin")
MONEY_FIELDS = {"market_cap", "revenue", "net_income"}
PRICE_FIELDS = {"current_price", "week_52_high", "week_52_low"}
PE_FIELDS = {"pe_ratio", "forward_pe"}

DEFAULT_REL_TOL = 0.02
MODES = ("off", "warn", "block")
DEFAULT_MODE = "warn"

FIELD_NAMES = {
    "current_price": "price", "market_cap": "market cap", "pe_ratio": "P/E",
    "forward_pe": "forward P/E", "week_52_high": "52-week high",
    "week_52_low": "52-week low", "revenue": "revenue",
    "net_income": "net income", "profit_margin": "profit margin",
}

_UNIT_MULT = {
    "thousand": 1e3, "k": 1e3, "million": 1e6, "mn": 1e6, "m": 1e6,
    "mm": 1e6, "billion": 1e9, "bn": 1e9, "b": 1e9, "trillion": 1e12,
    "tn": 1e12, "t": 1e12,
}

_NUM = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+"
# One stated value: optional sign, currency, number, scale word or attached
# abbreviation (59.5M, 899.5B), percent or x/times suffix. The sign must not
# follow a word character, so "10-K" and "$4.06-$21.24" are not negatives.
_VALUE = (
    r"(?<![\w.$%])(?P<neg>[-−]\s?)?"
    r"(?P<cur>US\$|\$|USD\s?)?\s?(?P<neg2>[-−])?"
    r"(?P<num>" + _NUM + r")"
    r"(?:\s?(?P<unit>(?i:thousand|million|billion|trillion|mn|bn|tn))\b"
    r"|(?P<abbr>(?-i:MM|[KMBT]))\b)?"
    r"(?:\s?(?P<pct>%|percent\b)|(?P<x>[x×]\b|\s?times\b))?"
    r"(?:\s?USD\b)?"
)
_VALUE_RE = re.compile(_VALUE)

# Words allowed between a label and its value. Hedges mark rounding;
# bounds mark an inequality (checked never, counted as unchecked).
_HEDGES = ("approximately", "approx.", "about", "roughly", "around", "nearly",
           "almost", "some", "~", "close to", "just under", "just over")
_BOUNDS = ("over", "more than", "above", "exceeding", "in excess of",
           "less than", "under", "below", "at least", "up to", "at most")
_LINKS = ("of", "at", "is", "was", "stands at", "stood at", "sits at",
          "sitting at", "currently at", "came in at", "comes in at",
          "totaled", "totaling", "totalled", "totalling", "reached",
          "amounted to", "equal to", "equals", "an", "a", "the", "just",
          "(ttm)", "(trailing)", ":", "=", "**", "*")
# The same words right before a number-first value ("over $30.2 billion in
# revenue").
_HEDGE_BEFORE_RE = re.compile(
    r"(?:" + "|".join(re.escape(t) for t in _HEDGES) + r")\s*$", re.I)
_BOUND_BEFORE_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(t) for t in _BOUNDS) + r")\s*$", re.I)
_CONNECT_TOKENS = sorted(_HEDGES + _BOUNDS + _LINKS, key=len, reverse=True)
_CONNECT_RE = re.compile(
    r"\s*(?:" + "|".join(
        re.escape(t) + (r"\b" if t[-1].isalnum() else "")
        for t in _CONNECT_TOKENS) + r")", re.I)

_PE = r"(?:P/?E(?![a-z])|price[- /]to[- ]earnings|price/earnings)(?:\s*\(P/?E\))?"
# Label-before patterns: (field, regex). The value follows via connectors.
_LABELS = [
    ("market_cap", r"market\s+cap(?:italization|italisation)?\b"),
    ("forward_pe", r"forward(?:\s+|-)(?:(?:twelve|12)[- ]month\s+)?" + _PE
     + r"(?:\s+(?:ratio|multiple))?"),
    ("pe_ratio", r"(?<!forward )(?<!forward-)(?:(?:trailing|ttm|current|"
     r"trailing[- ]twelve[- ]month)\s+)?\b" + _PE
     + r"(?:\s+(?:ratio|multiple))?"),
    ("week_52_high", r"52[- ]week\s+(?:trading\s+)?high"),
    ("week_52_low", r"52[- ]week\s+(?:trading\s+)?low"),
    ("current_price", r"(?:current\s+(?:share\s+|stock\s+|trading\s+)?price|"
     r"(?:share|stock|trading)\s+price|price\s+per\s+share)"),
    ("current_price~", r"\b(?:trades|trading|traded|trade)\s+at"),
    ("revenue", r"\brevenues?\b"),
    ("net_income", r"\bnet\s+(?:income|earnings|profit)\b(?!\s+margin)"),
    ("net_loss", r"\bnet\s+loss(?:es)?\b"),
    ("profit_margin", r"\b(?:net\s+profit|profit|net)\s+margins?\b"),
]
_LABEL_RES = [(f, re.compile(p, re.I)) for f, p in _LABELS]

# Number-before patterns: "<value> [in] [annual|total|...] <label>".
_POST_GAP = (r"\s+(?:in\s+)?(?:(?:annual|annualized|total|trailing|ttm|net|"
             r"reported|yearly|trailing[- ]twelve[- ]month)\s+)*")
_POST_LABELS = [
    ("market_cap", r"market\s+cap(?:italization|italisation)?\b"),
    ("forward_pe", r"forward\s+(?:" + _PE + r"|earnings)\b"),
    ("pe_ratio", r"(?:trailing\s+earnings\b|" + _PE + r"\b)"),
    ("revenue", r"revenues?\b"),
    ("net_income", r"(?:income|earnings|profit)\b(?!\s+margin)"),
    ("net_loss", r"loss(?:es)?\b"),
    ("profit_margin", r"(?:profit\s+)?margins?\b"),
]
_POST_RES = [(f, re.compile(_VALUE + _POST_GAP + r"(?:" + p + r")", re.I))
             for f, p in _POST_LABELS]
# The net_income/net_loss/profit_margin number-before labels need "net" or
# "profit" to be present (the gap may hold "net"); checked in code.

_RANGE_RE = re.compile(
    r"52[- ]week\s+(?:trading\s+|price\s+)?range\s*(?:of\s+|:\s*|\(\s*|is\s+|"
    r"between\s+)?(?P<a>" + _VALUE.replace("?P<", "?P<a_") + r")\s*"
    r"(?:-|–|—|to|and)\s*(?P<b>" + _VALUE.replace("?P<", "?P<b_") + r")", re.I)

_NA_RE = re.compile(r"(?:N/A|n/a|\bNA\b|not available|unavailable|"
                    r"not applicable|not disclosed|\bnull\b|\bnone\b)", re.I)

# Words before "revenue" that keep it the company total; anything else that
# looks like a noun ("services revenue", "advertising revenue") is a subline.
_REVENUE_OK_PREV = {
    "", "annual", "annualized", "total", "trailing", "ttm", "overall",
    "reported", "consolidated", "net", "its", "their", "the", "a", "an", "of",
    "in", "and", "with", "on", "against", "minimal", "modest", "strong",
    "robust", "solid", "limited", "generated", "generating", "reporting",
    "reports", "had", "has", "yearly", "current", "combined", "twelve-month",
    "12-month", "full-year", "whose", "while", "but", "to", "from", "by",
    "for", "gross",
}
_MARGIN_BAD_PREV = {"gross", "operating", "ebitda", "ebit", "adjusted",
                    "pre-tax", "pretax", "segment", "contribution", "fcf",
                    "cash", "interest", "services", "product"}

_PERIOD_RE = re.compile(
    r"(?<![$\d.,])\b(?:19|20)\d{2}\b(?![.,]\d|\s?%|x\b|\s?(?:million|billion|"
    r"trillion|thousand)\b)|\bQ[1-4]\b|\bFY\s?\d{0,4}\b|\bfiscal\b|"
    r"\bquarter(?:ly)?\b|\bprior[- ]year\b|\bprevious\s+year\b|"
    r"\blast\s+year\b|\ba\s+year\s+(?:ago|earlier)\b|"
    r"\byear[- ](?:over|on)[- ]year\b|\bsince\s+inception\b|\baccumulated\b|"
    r"\bcumulative(?:ly)?\b|\b(?:two|three|four|five|six|nine|ten|\d+)[- ]"
    r"(?:months?|years?)\b|\bdecade\b|\bhistorical(?:ly)?\b|\bpreviously\b|"
    r"\bpeak\b|\ball[- ]time\b|\bIPO\b|\bguidance\b|\bprojected\b|"
    r"\bforecast\b|\btarget\b|\bestimated?\b|\bpro\s+forma\b|\bsegment\b|"
    r"\byears?[- ]end(?:ed|ing)?\b|\bfor\s+the\s+(?:full\s+)?year\b",
    re.I)
_TTM_RE = re.compile(r"\b(?:trailing|past|last)\s+(?:12|twelve)[- ]months?\b|"
                     r"\bTTM\b", re.I)
_MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|"
           r"October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|"
           r"Oct|Nov|Dec)\.?")
# "as of <date>" names the snapshot date, not another period: stripped
# before the period test. "As of its most recent quarter" is not a date and
# stays (its "quarter" then marks the period).
_AS_OF_RE = re.compile(
    r"\bas\s+of\s+(?:(?:the\s+end\s+of\s+)?" + _MONTHS
    + r"(?:\s+\d{1,2})?(?:,?\s*(?:19|20)\d{2})?|(?:19|20)\d{2}|today|now|"
    r"this\s+writing|the\s+latest\s+(?:data|close|available\s+data))", re.I)
# Leading qualifiers that scope the whole sentence: a markdown bold lead-in
# ("- **Net Losses Since Inception:**") and an opening adverbial clause
# ("Over the past five years, ...", "In fiscal 2025, ...").
_LEAD_BOLD_RE = re.compile(r"^\s*(?:[-*]\s+)?\*\*[^*]{1,80}\*\*:?", re.I)
_LEAD_ADV_RE = re.compile(
    r"^\s*(?:over|in|for|during|since|through|throughout|between|across|"
    r"from|within|as\s+of|last|earlier|previously|historically|at\s+the\s+end"
    r"\s+of)\b[^;:]*?,\s(?!(?:19|20)\d{2}\b)", re.I)
# Possessives/nouns before a label that make it another entity's figure
# ("the S&P 500's P/E ratio", "the sector average P/E").
_OTHER_ENTITY = {"industry", "sector", "peer", "peers", "peers'", "average",
                 "median", "index", "benchmark", "competitor", "competitors",
                 "competitors'", "rival", "rivals", "rivals'", "market's",
                 "s&p", "nasdaq", "group's", "segment's"}
_SELF_WORDS = {"company", "firm", "stock", "share", "its", "business",
               "corporation"}
_WHOLE_SENTENCE_RE = re.compile(
    r"\brespectively\b|\bcompared\s+(?:to|with)\b|\bversus\b|\bvs\.?\s|"
    r"\bsame\s+period\b", re.I)
_CLAUSE_BREAK = re.compile(
    r";|,\s(?!(?:19|20)\d{2}\b)|\(|\)|—|\s–\s|\s-\s|"
    r"\bcompared\s+(?:to|with)\b|\bversus\b|"
    r"\bvs\.?\s|\bagainst\b|\bwhile\b|\bwhereas\b|\bbut\b|\bdown\s+from\b|"
    r"\bup\s+from\b|\bfrom\b", re.I)

_SENT_RE = re.compile(r"[^\n]+?(?:(?<=[.!?])(?=\s)|$)", re.M)

_PLACEHOLDER_RES = [
    # [City Name], [Company], [X] — not links, citations or checkboxes.
    re.compile(r"(?<!\])\[(?!\d+\])(?!sic\])[A-Za-z][^\[\]\n]{0,40}\](?![(\[:])"),
    re.compile(r"\{\{?\s*[A-Za-z_][A-Za-z0-9_ ]{0,30}\}\}?"),
    re.compile(r"\$X{1,3}(?:\.X+)?\b|\bX{2,}(?:\.X+)?%"),
]
_CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]")

# Numeric tokens for the coverage denominator, minus obvious non-metrics.
_TOKEN_RE = re.compile(r"(?<![\w.])(?:" + _NUM + r")")
_NON_METRIC_RES = [
    re.compile(r"(?<![$\d.,])\b(?:19|20)\d{2}\b(?![\d.,]*\s?(?:%|million|"
               r"billion|trillion|x\b))"),
    re.compile(r"\b52(?=[- ]week)", re.I),
    re.compile(r"\b\d{1,2}(?=-[KQFk]\b)|\b(?:S|F)-(\d)\b"),
    re.compile(r"(?<=\bQ)[1-4]\b"),
    re.compile(r"(?<=\bItem )\d+[A-Z]?", re.I),
    re.compile(_MONTHS + r"\s+(\d{1,2})\b"),
    re.compile(r"^\s*(\d+)\.\s", re.M),
]


def numeric_check_mode() -> str:
    """NUMERIC_CHECK env (off|warn|block); unknown values fall back to warn."""
    mode = os.getenv("NUMERIC_CHECK", DEFAULT_MODE).strip().lower()
    return mode if mode in MODES else DEFAULT_MODE


# --- parsing -----------------------------------------------------------------

def _num(text: str) -> float:
    return float(text.replace(",", ""))


def _decimals(num_text: str) -> int:
    return len(num_text.split(".", 1)[1]) if "." in num_text else 0


def _trailing_zeros(num_text: str) -> int:
    if "." in num_text:
        return 0
    digits = num_text.replace(",", "")
    return len(digits) - len(digits.rstrip("0")) if digits.strip("0") else 0


def parse_value(m, prefix: str = "") -> dict:
    """A _VALUE match (group names optionally prefixed) -> parsed parts:
    number, multiplier, sign, currency/percent/x flags, and the half-ulp of
    the stated precision in the value's own units (before the multiplier)."""
    g = lambda k: m.group(prefix + k)  # noqa: E731
    num_text = g("num")
    unit = (g("unit") or g("abbr") or "").lower()
    mult = _UNIT_MULT.get(unit, 1.0)
    neg = bool(g("neg") or g("neg2"))
    value = _num(num_text) * (-1 if neg else 1)
    return {
        "num_text": num_text, "number": value, "mult": mult,
        "unit": unit, "neg": neg, "cur": bool(g("cur")),
        "pct": bool(g("pct")), "x": bool(g("x")),
        "half_ulp": 0.5 * 10 ** (-_decimals(num_text)),
        "half_ulp_hedged": 0.5 * 10 ** (-_decimals(num_text)
                                        or _trailing_zeros(num_text)),
    }


def _connect(text: str, pos: int) -> tuple[int, bool, bool, set[str]]:
    """Consume connector tokens after a label. Returns (value_pos, hedged,
    bounded, tokens)."""
    hedged = bounded = False
    toks = set()
    for _ in range(6):
        m = _CONNECT_RE.match(text, pos)
        if not m:
            break
        tok = m.group(0).strip().lower()
        hedged |= tok in _HEDGES
        bounded |= tok in _BOUNDS
        toks.add(tok)
        pos = m.end()
    while pos < len(text) and text[pos] in " \t":
        pos += 1
    return pos, hedged, bounded, toks


def _prev_word(text: str, pos: int) -> str:
    """The word right before pos (skipping spaces and markdown bold), or ""
    when punctuation sits there instead."""
    m = re.search(r"([\w'’&-]+)[ \t*]*$", text[:pos])
    return m.group(1).lower() if m and re.search(r"[A-Za-z]", m.group(1)) else ""


def _clause(sentence: str, start: int, end: int) -> str:
    """The clause of `sentence` around [start, end): bounded by the nearest
    clause break on each side (a break inside the span does not count)."""
    lo, hi = 0, len(sentence)
    for m in _CLAUSE_BREAK.finditer(sentence):
        if m.end() <= start:
            lo = m.end()
        elif m.start() >= end:
            hi = m.start()
            break
    return sentence[lo:hi]


def _form_ok(field: str, v: dict, trade_label: bool) -> bool:
    if field in MONEY_FIELDS:
        return (v["cur"] or v["mult"] != 1.0) and not v["pct"] and not v["x"]
    if field in PRICE_FIELDS:
        if v["pct"] or v["x"] or v["mult"] != 1.0:
            return False
        return v["cur"] or not trade_label
    if field in PE_FIELDS:
        return not (v["pct"] or v["cur"] or v["mult"] != 1.0)
    if field == "profit_margin":
        return v["pct"] and not v["cur"]
    return False


def _bindings_in_sentence(sentence: str) -> tuple[list[dict], list[dict]]:
    """Label-bound values and N/A fillers in one sentence."""
    out, nas, taken = [], [], []

    def overlaps(s, e):
        return any(s < te and ts < e for ts, te in taken)

    def add(field, label_span, value_span, v, hedged=False, bounded=False,
            negate=False, loss=False, trade=False, in_range=False):
        vs, ve = value_span
        if overlaps(vs, ve):
            return
        taken.append((vs, ve))
        out.append({"field": field, "label_span": label_span,
                    "value_span": (vs, ve), "value": v, "hedged": hedged,
                    "bounded": bounded, "negate": negate, "loss": loss,
                    "trade": trade, "in_range": in_range,
                    "stated": sentence[vs:ve].strip()})

    # 52-week ranges first: they bind two values at once.
    for m in _RANGE_RE.finditer(sentence):
        a, b = parse_value(m, "a_"), parse_value(m, "b_")
        lo_first = a["number"] * a["mult"] <= b["number"] * b["mult"]
        add("week_52_low" if lo_first else "week_52_high",
            (m.start(), m.start("a")), m.span("a"), a, in_range=True)
        add("week_52_high" if lo_first else "week_52_low",
            (m.start(), m.start("a")), m.span("b"), b, in_range=True)

    # Number-before next: "<value> [in] [annual|net|...] <label>" is the
    # tightest binding there is ("20.8x trailing earnings" must not be
    # claimed by a preceding "trades at").
    for field, rx in _POST_RES:
        for m in rx.finditer(sentence):
            tail = sentence[m.end("num"):m.end()].lower()
            if field in ("net_income", "net_loss") and not re.search(r"\bnet\b", tail):
                continue
            if field == "profit_margin" and not re.search(r"\b(?:net|profit)\b", tail):
                continue
            vm = _VALUE_RE.match(sentence, m.start())
            before = sentence[max(0, m.start() - 24):m.start()].lower()
            real = "net_income" if field == "net_loss" else field
            # "forward earnings expectations of 12.49x P/E" is forward.
            if real == "pe_ratio" and re.search(
                    r"\bforward\b", sentence[max(0, m.start() - 40):m.start()], re.I):
                real = "forward_pe"
            add(real,
                (vm.end(), m.end()), vm.span(), parse_value(vm),
                hedged=bool(_HEDGE_BEFORE_RE.search(before)),
                bounded=bool(_BOUND_BEFORE_RE.search(before)),
                negate="negative" in before[-12:], loss=field == "net_loss")

    # Label-before: label, connector words, value (or an N/A filler).
    for field, rx in _LABEL_RES:
        real = field.rstrip("~")
        real = "net_income" if real == "net_loss" else real
        for m in rx.finditer(sentence):
            if real == "profit_margin" and _prev_word(sentence, m.start()) in _MARGIN_BAD_PREV:
                continue
            pos, hedged, bounded, toks = _connect(sentence, m.end())
            # "below its 52-week high at $0.56": the value after "at" is
            # where the stock trades now, not the 52-week figure.
            if real in ("week_52_high", "week_52_low") and "at" in toks:
                continue
            vm = _VALUE_RE.match(sentence, pos)
            if not vm:
                na = _NA_RE.match(sentence, pos)
                if na:
                    nas.append({"field": real, "stated": na.group(0)})
                continue
            before = sentence[max(0, m.start() - 12):m.start()].lower()
            add(real, m.span(), vm.span(), parse_value(vm), hedged, bounded,
                negate="negative" in before, loss=field == "net_loss",
                trade=field.endswith("~"))
    return out, nas


def _sentences(text: str):
    for m in _SENT_RE.finditer(text):
        s = m.group(0)
        if s.strip():
            yield m.start(), s


def _company_tokens(stock: dict) -> set[str]:
    words = re.findall(r"[a-z0-9&]+", f"{stock.get('company_name') or ''} "
                       f"{stock.get('ticker') or ''}".lower())
    return {w for w in words if len(w) >= 3} - {"inc", "corp", "ltd", "plc",
                                                "the", "and", "holdings"}


def _lead(sentence: str) -> str:
    """The sentence's leading qualifiers: bold lead-in plus opening
    adverbial clause (either may be absent)."""
    out, rest = "", sentence
    m = _LEAD_BOLD_RE.match(rest)
    if m:
        out, rest = m.group(0), rest[m.end():]
    m = _LEAD_ADV_RE.match(_AS_OF_RE.sub("as of now", rest))
    return out + " " + (m.group(0) if m else "")


def _scope(b: dict, sentence: str, stock: dict, company: set[str]) -> str | None:
    """None when the binding is checkable, else the out-of-scope reason."""
    field, v = b["field"], b["value"]
    if not _form_ok(field, v, b["trade"]):
        return "form"
    if b["bounded"]:
        return "bound"
    s = min(b["label_span"][0], b["value_span"][0])
    e = max(b["label_span"][1], b["value_span"][1])
    prev = _prev_word(sentence, s)
    base = re.sub(r"['’]s?$", "", prev)
    if prev in _OTHER_ENTITY or base in _OTHER_ENTITY or (
            prev.endswith(("'s", "’s", "s'")) and base not in company
            and base not in _SELF_WORDS):
        return "other_entity"
    if field == "revenue" and b["label_span"][0] < b["value_span"][0]:
        if prev and prev not in _REVENUE_OK_PREV and base not in company \
                and base not in _SELF_WORDS:
            return "subline"
    # "... of $80.0M, $376.7M and $132.5M for 2025, 2024 and 2023,
    # respectively" distributes the trailing periods over the whole list.
    # Comparative sentences ("... compared to $1.0 billion during the same
    # period in 2024") put both figures in the compared periods.
    whole = _WHOLE_SENTENCE_RE.search(sentence)
    scope_text = (sentence if whole else _clause(sentence, s, e)) + " " + _lead(sentence)
    vs, ve = b["value_span"]
    scope_text = scope_text.replace(sentence[vs:ve], " ")  # never its own year
    scope_text = _AS_OF_RE.sub(" ", _TTM_RE.sub(" ", scope_text))
    if _PERIOD_RE.search(scope_text):
        return "period"
    if stock.get(field) is None:
        return "no_source"
    return None


def _stated_value(b: dict) -> tuple[float, float]:
    """(value, tolerance slack from stated precision) in comparison units:
    dollars for money, the plain number for prices and P/E, percentage
    points for profit margin."""
    v = b["value"]
    val = v["number"] * v["mult"]
    if b["loss"] or b["negate"]:
        val = -abs(val)
    ulp = v["half_ulp_hedged"] if b["hedged"] else v["half_ulp"]
    return val, ulp * v["mult"]


def _source_value(field: str, stock: dict) -> float:
    src = float(stock[field])
    return src * 100.0 if field == "profit_margin" else src


def compare(stated: float, source: float, slack: float,
            rel_tol: float = DEFAULT_REL_TOL) -> bool:
    """True when `stated` matches `source` within rel_tol of the source plus
    the stated-precision slack."""
    return abs(stated - source) <= rel_tol * abs(source) + slack + 1e-12


def _placeholders(sentence: str) -> list[str]:
    if _CHECKBOX_RE.match(sentence):
        sentence = _CHECKBOX_RE.sub("", sentence)
    found = []
    for rx in _PLACEHOLDER_RES:
        found.extend(m.group(0) for m in rx.finditer(sentence))
    return found


def _count_tokens(text: str, consumed: list[tuple[int, int]]) -> int:
    skip = set()
    for rx in _NON_METRIC_RES:
        for m in rx.finditer(text):
            s, e = (m.span(1) if m.re.groups and m.group(1) else m.span())
            skip.update(range(s, e))
    n = 0
    for m in _TOKEN_RE.finditer(text):
        s, e = m.span()
        if s in skip or any(cs <= s < ce for cs, ce in consumed):
            continue
        n += 1
    return n


# --- public API --------------------------------------------------------------

def check_section(section: str, text: str, stock: dict,
                  rel_tol: float = DEFAULT_REL_TOL) -> dict:
    """Check one section's text against the stock dict. Returns
    {findings, checked, unchecked, unchecked_reasons, bindings}."""
    findings, bindings = [], []
    reasons: dict[str, int] = {}
    checked = 0
    consumed = []
    company = _company_tokens(stock)
    for off, sent in _sentences(text):
        found, nas = _bindings_in_sentence(sent)
        for b in found:
            reason = _scope(b, sent, stock, company)
            vs, ve = b["value_span"]
            rec = {"section": section, "field": b["field"],
                   "stated": b["stated"], "sentence": sent.strip(),
                   "span": (off + vs, off + ve), "status": reason or "checked",
                   # The label fixes the sign ("net loss of", "negative"),
                   # so the number's own sign does not carry information.
                   "sign_fixed": b["loss"] or b["negate"],
                   # One end of a "52-week range ($A-$B)": the ends are
                   # assigned by size, so their order carries no claim.
                   "in_range": b["in_range"]}
            bindings.append(rec)
            if reason:
                reasons[reason] = reasons.get(reason, 0) + 1
                continue
            consumed.append((off + vs, off + ve))
            checked += 1
            stated, slack = _stated_value(b)
            source = _source_value(b["field"], stock)
            rec["stated_value"] = stated
            if not compare(stated, source, slack, rel_tol):
                findings.append({
                    "section": section, "field": b["field"],
                    "stated": b["stated"], "stated_value": stated,
                    "source": stock[b["field"]],
                    "ratio": (stated / source) if source else None,
                    "kind": "mismatch", "sentence": sent.strip(),
                })
        for na in nas:
            if stock.get(na["field"]) is not None:
                findings.append({
                    "section": section, "field": na["field"],
                    "stated": na["stated"], "stated_value": None,
                    "source": stock[na["field"]], "ratio": None,
                    "kind": "placeholder", "sentence": sent.strip(),
                })
        for tok in _placeholders(sent):
            findings.append({
                "section": section, "field": None, "stated": tok,
                "stated_value": None, "source": None, "ratio": None,
                "kind": "placeholder", "sentence": sent.strip(),
            })
    unchecked = _count_tokens(text, consumed)
    return {"findings": findings, "checked": checked, "unchecked": unchecked,
            "unchecked_reasons": reasons, "bindings": bindings}


def _section_spans(markdown: str) -> list[dict]:
    """Split a brief on `##`/`###` headings (deeper headings stay in their
    section). Text before the first heading is the "(preamble)" section."""
    heads = list(re.finditer(r"^#{2,3}[ \t]+(.+?)[ \t]*$", markdown, re.M))
    spans = []
    if not heads or heads[0].start() > 0:
        end = heads[0].start() if heads else len(markdown)
        if markdown[:end].strip():
            spans.append({"heading": "(preamble)", "body_start": 0,
                          "end": end})
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(markdown)
        spans.append({"heading": h.group(1).strip(), "body_start": h.end(),
                      "end": end})
    return spans


def split_sections(markdown: str) -> list[tuple[str, str]]:
    """(heading, body) pairs for a brief's sections."""
    return [(s["heading"], markdown[s["body_start"]:s["end"]])
            for s in _section_spans(markdown)]


def check_sections(sections, stock: dict,
                   rel_tol: float = DEFAULT_REL_TOL) -> dict:
    """Check (heading, text) pairs. Returns the report: findings, counts
    checked/unchecked (with out-of-scope reasons), mismatches, placeholders."""
    report = {"findings": [], "checked": 0, "unchecked": 0,
              "unchecked_reasons": {}, "bindings": []}
    stock = stock or {}
    for i, (heading, text) in enumerate(sections):
        r = check_section(heading, text, stock, rel_tol)
        for rec in r["findings"] + r["bindings"]:
            rec["section_index"] = i
        report["findings"].extend(r["findings"])
        report["bindings"].extend(r["bindings"])
        report["checked"] += r["checked"]
        report["unchecked"] += r["unchecked"]
        for k, n in r["unchecked_reasons"].items():
            report["unchecked_reasons"][k] = report["unchecked_reasons"].get(k, 0) + n
    report["mismatches"] = sum(f["kind"] == "mismatch" for f in report["findings"])
    report["placeholders"] = sum(f["kind"] == "placeholder" for f in report["findings"])
    return report


def check_brief(markdown: str, stock: dict,
                rel_tol: float = DEFAULT_REL_TOL) -> dict:
    return check_sections(split_sections(markdown), stock, rel_tol)


def _fmt(field: str | None, value) -> str:
    if value is None:
        return "n/a"
    value = float(value)
    if field == "profit_margin":
        return f"{value * 100:.1f}%"
    if field in PE_FIELDS:
        return f"{value:.1f}x"
    if field in MONEY_FIELDS:
        sign = "-" if value < 0 else ""
        a = abs(value)
        for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
            if a >= div:
                return f"{sign}${a / div:.1f}{suf}"
        return f"{sign}${a:,.0f}"
    return f"${value:,.2f}"


def render_note(findings: list[dict]) -> str:
    """The short warn-mode note appended to a brief."""
    lines = ["", "---", "**Numeric check** (deterministic; stock data only): "
             f"{len(findings)} issue(s)."]
    for f in findings:
        if f["kind"] == "mismatch":
            ratio = f" ({f['ratio']:.3g}x)" if f["ratio"] is not None else ""
            lines.append(f"- {f['section']}: {FIELD_NAMES[f['field']]} stated "
                         f"{f['stated']}, stock data {_fmt(f['field'], f['source'])}"
                         f"{ratio}")
        elif f["field"]:
            lines.append(f"- {f['section']}: {FIELD_NAMES[f['field']]} stated "
                         f"\"{f['stated']}\", stock data "
                         f"{_fmt(f['field'], f['source'])}")
        else:
            lines.append(f"- {f['section']}: unfilled placeholder \"{f['stated']}\"")
    return "\n".join(lines) + "\n"


BLOCK_NOTICE = ("*This section was withheld: the numeric check found a figure "
                "that does not match the fetched stock data.*")


def apply_numeric_check(brief: str, stock: dict, mode: str | None = None,
                        rel_tol: float = DEFAULT_REL_TOL) -> tuple[str, dict | None]:
    """Run the check in `mode` (default: NUMERIC_CHECK env). Returns
    (brief_to_render, report); report is None when mode is off. warn leaves
    the brief unchanged apart from an appended note; block additionally
    replaces each section with a mismatch by a one-line notice."""
    mode = mode or numeric_check_mode()
    if mode == "off":
        return brief, None
    spans = _section_spans(brief)
    report = check_sections(
        [(s["heading"], brief[s["body_start"]:s["end"]]) for s in spans],
        stock, rel_tol)
    report["mode"] = mode
    report.pop("bindings", None)
    out = brief
    if mode == "block":
        bad = {f["section"] for f in report["findings"] if f["kind"] == "mismatch"}
        for s in reversed(spans):
            if s["heading"] in bad:
                out = (out[:s["body_start"]] + "\n\n" + BLOCK_NOTICE + "\n\n"
                       + out[s["end"]:].lstrip("\n"))
        report["blocked_sections"] = sorted(bad)
    if report["findings"]:
        # Appended, never interleaved: in warn mode the result extends the
        # brief as a prefix, so a streaming caller can emit just the tail.
        out = out + ("" if out.endswith("\n") else "\n") + render_note(report["findings"])
    return out, report
