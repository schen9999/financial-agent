"""eval/rag_refusals.py: the refusal rule fixed before the reranking A/B
reproduces its recorded counts and keeps limitation 2's tickers."""
from eval import rag_refusals as rr


def test_recorded_hosted_runs():
    for run in ("4hsn2", "9jzmj"):
        r = rr.run_refusals(run)
        assert len(r) == 35 and sum(r.values()) == 9
        assert {"AMZN", "JPM", "MSFT", "NVDA", "WMT"} <= {t for t, v in r.items() if v}


def test_rule():
    assert rr.is_refusal("[From Pinecone cache] I cannot provide a summary of the latest 10-K. The context only...")
    assert not rr.is_refusal("I cannot provide a summary of the 10-Q. From the 10-K, the key takeaways are: ...")
    assert not rr.is_refusal("Apple reported revenue of ... I cannot provide more.")
    assert rr.highlights("## Retrieved source context\nRAG — SEC HIGHLIGHTS:\n(not available)\n\nRAG — RISK FACTORS:\nx") is None
