"""eval/compare_runs.py: context block split, filing dates, raw vs deduped
counts, pooled Fisher."""
import json

from eval.compare_runs import (NOT_AVAILABLE, cmd_pooled, filings, raw_counts,
                               split_blocks)
from eval.label import count_labels_deduped

CONTEXT = ("STOCK DATA:\n{\"price\": 1}\n\nNEWS ARTICLES:\n[]\n\n"
           "SEC FILING SUMMARIES:\n{\"10-K\": {\"form_type\": \"10-K\", \"filing_date\": \"2025-10-31\"}}\n\n"
           "RAG — SEC HIGHLIGHTS:\nrevenue grew\n\nRAG — RISK FACTORS:\n(not available)")


def test_split_blocks_and_filings():
    b = split_blocks(CONTEXT)
    assert list(b) == ["STOCK DATA", "NEWS ARTICLES", "SEC FILING SUMMARIES",
                       "RAG — SEC HIGHLIGHTS", "RAG — RISK FACTORS"]
    assert b["RAG — RISK FACTORS"] == NOT_AVAILABLE
    assert filings(b["SEC FILING SUMMARIES"]) == {"10-K": "2025-10-31"}
    assert filings("{}") == {} and filings("not json") == {}


def test_raw_counts_every_line_deduped_once_per_block():
    findings = ("CLAIM: \"a\"\nLABEL: SUPPORTED\nREASON: x\nLABEL: SUPPORTED\nREASON: x\n"
                "**CLAIM:** \"b\"\n**LABEL:** UNSUPPORTED\n")
    assert raw_counts(findings) == {"supported": 2, "unsupported": 1, "inference": 0}
    d = count_labels_deduped(findings)
    assert (d["supported"], d["unsupported"]) == (1, 1)


def test_pooled_fisher(tmp_path, capsys):
    def write(name, u, n):
        p = tmp_path / f"{name}-claims.jsonl"
        p.write_text("".join(json.dumps({"judge_label": "UNSUPPORTED" if i < u else "SUPPORTED"}) + "\n"
                             for i in range(n)), encoding="utf-8")
        return str(p)
    cmd_pooled([["old", write("a", 12, 387 - 1), write("b", 12, 392)],
                ["new", write("c", 4, 383), write("d", 7, 389)]])
    out = capsys.readouterr().out
    assert "24/778" in out and "11/772" in out and "p = 0.0388" in out


def test_news_changed_flags_only_differing_news(tmp_path):
    from eval.compare_runs import news_changed

    def write(run, ticker, news):
        d = tmp_path / run
        d.mkdir(exist_ok=True)
        ctx = CONTEXT.replace("NEWS ARTICLES:\n[]", f"NEWS ARTICLES:\n{news}")
        (d / f"{ticker}_baseline.md").write_text(
            f"# {ticker}\n\n## Retrieved source context\n\n{ctx}\n\n"
            "## Audited (Exec Summary + Outlook)\n\ntext\n\n## Judge findings\n\nnone\n",
            encoding="utf-8")
    write("a", "AAA", "[1]"); write("b", "AAA", "[2]")
    write("a", "BBB", "[3]"); write("b", "BBB", "[3]")
    assert news_changed(tmp_path / "a", tmp_path / "b") == {"AAA"}
