"""eval/claim_density.py: numeric vs qualitative judged claims and the size of
the audited text, per brief and per run."""
from eval import claim_density as cd
from eval.label import render_findings_md

AUDITED = """### Executive Summary
Visa earns a 50.8% profit margin on $22.4 billion in net income. The stock trades at a premium.

### Outlook
The outlook is cautiously constructive and depends on regulation in Europe.

---
*This brief is for informational purposes only and does not constitute financial advice.*"""

NUMBERS_ONLY = """CLAIM: "50.8% profit margin"
LABEL: SUPPORTED
REASON: matches.

CLAIM: "$22.4 billion in net income"
LABEL: SUPPORTED
REASON: matches.
"""

WITH_QUALITATIVE = NUMBERS_ONLY + """
CLAIM: "regulation in Europe"
LABEL: UNSUPPORTED
REASON: absent.
"""


def _file(tmp_path, ticker, findings):
    d = tmp_path / "run-findings"
    d.mkdir(exist_ok=True)
    (d / f"{ticker}_slm-full-cpu.md").write_text(
        render_findings_md(ticker, "slm-full-cpu", "v2", "ctx", "### Financial Health\nx",
                           AUDITED, findings), encoding="utf-8")
    return d


def test_brief_density_splits_numeric_and_qualitative_claims(tmp_path):
    d = _file(tmp_path, "V", WITH_QUALITATIVE)
    b = cd.run_density(d)["V"]
    assert (b["claims"], b["supported"], b["numeric"], b["qualitative"]) == (3, 2, 2, 1)
    assert b["numeric_unsupported"] == 0  # the unsupported claim is the qualitative one
    # headings, the rule and the disclaimer are not counted as audited text
    assert b["numbers"] == 2 and b["words"] == 29


def test_summarize_names_min_and_numbers_only_tickers(tmp_path):
    _file(tmp_path, "V", WITH_QUALITATIVE)
    d = _file(tmp_path, "AMZN", NUMBERS_ONLY)
    s = cd.summarize(cd.run_density(d))
    assert (s["tickers"], s["claims"], s["claims_mean"], s["claims_min"]) == (2, 5, 2.5, 2)
    assert s["claims_min_tickers"] == ["AMZN"] and s["zero_qualitative"] == ["AMZN"]
    assert (s["numeric_mean"], s["qualitative_mean"]) == (2.0, 0.5)
    assert (s["numeric"], s["numeric_unsupported"], s["numeric_min"]) == (4, 0, 2)


def test_main_prints_run_and_ticker_rows(tmp_path, capsys):
    d = _file(tmp_path, "V", NUMBERS_ONLY)
    assert cd.main(["--run", "r1", str(d), "--tickers", "V"]) == 0
    out = capsys.readouterr().out
    assert "r1: min claims at V; the judge audited numbers only for V" in out
    assert "r1             0/2 = 0.00%" in out
    assert "V       r1" in out


def test_numeric_claim_counts_keeps_labels_and_ignores_qualitative_claims():
    from eval.label import numeric_claim_counts
    findings = WITH_QUALITATIVE + """
CLAIM: "a 30.7x trailing multiple"
LABEL: UNSUPPORTED
REASON: absent.
"""
    assert numeric_claim_counts(findings) == {"total": 3, "supported": 2, "unsupported": 1,
                                              "inference": 0}
    assert numeric_claim_counts("no claims here")["total"] == 0


def test_strict_numeric_drops_claims_numeric_only_through_52_week(tmp_path):
    findings = NUMBERS_ONLY + """
CLAIM: "strong market sentiment near 52-week highs"
LABEL: UNSUPPORTED
REASON: positional.

CLAIM: "trades near the upper end of its 52-week range of $349.20 to $553.72"
LABEL: SUPPORTED
REASON: arithmetic holds.
"""
    assert cd.strict_numeric_counts(findings) == {"total": 3, "unsupported": 0}
    b = cd.run_density(_file(tmp_path, "META", findings))["META"]
    assert (b["numeric"], b["numeric_unsupported"]) == (4, 1)
    assert (b["numeric_strict"], b["numeric_strict_unsupported"]) == (3, 0)
    s = cd.summarize({"META": b})
    assert (s["numeric_strict"], s["numeric_strict_unsupported"], s["numeric_strict_mean"]) == (3, 0, 3.0)
