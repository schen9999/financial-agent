#!/usr/bin/env python3
"""Clear and rebuild Pinecone namespaces with the fixed section anchor.

Why: until 627b760, skip_front_matter anchored on the TOC's "Item 1A" line,
so indexed windows carried TOC + exhibit boilerplate instead of risk-factor
prose. Already-indexed namespaces keep that bad text until reindexed.

Per ticker (idempotent — a rerun converges to the same state):
  1. delete the ticker's namespace (missing namespace is fine),
  2. fetch the filing text through the FIXED skip_front_matter
     (10-K, falling back to 10-Q) and index it,
  3. verify: retrieve top-3 for a risk-factors query and check the nodes
     carry risk prose and no exhibit/TOC boilerplate.

Tickers with no retrievable filing (e.g. ADRs file 20-F, which the fetcher
does not target) are REPORTED, not fixed — that coverage gap is a known,
deliberate property of the extended benchmark.

Usage:
  python scripts/reindex_filings.py --from-file eval/tickers_extended.txt --dry-run
  python scripts/reindex_filings.py --tickers AAPL MSFT
  python scripts/reindex_filings.py --from-file eval/tickers_extended.txt
  python scripts/reindex_filings.py --from-file ... --verify-only
"""
import argparse
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from dotenv import load_dotenv  # noqa: E402
load_dotenv(REPO / ".env")

from llama_index.core import Document, StorageContext, VectorStoreIndex  # noqa: E402
from llama_index.vector_stores.pinecone import PineconeVectorStore  # noqa: E402

from agent.tools.rag import (_ensure_settings, _fetch_filing_text,  # noqa: E402
                             _get_pinecone_index)

RISK_QUERY = "What are the main risk factors?"
BOILER_RE = re.compile(
    r"exhibit\s+\d|form of .{0,40}(rsu|restricted stock)|indenture|"
    r"bonus plan|incentive plan|table of contents", re.I)


def read_ticker_file(path: str) -> list[str]:
    out = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            out.append(ln.upper())
    return out


def verify(pinecone_index, namespace: str) -> tuple[bool, bool, int]:
    """(has_risk_prose, has_boilerplate, node_count) for top-3 retrieval."""
    index = VectorStoreIndex.from_vector_store(
        vector_store=PineconeVectorStore(pinecone_index=pinecone_index,
                                         namespace=namespace))
    nodes = index.as_retriever(similarity_top_k=3).retrieve(RISK_QUERY)
    text = " ".join(n.get_content() for n in nodes)
    return ("risk" in text.lower(), bool(BOILER_RE.search(text)), len(nodes))


def main():
    ap = argparse.ArgumentParser(description="Reindex SEC filing namespaces.")
    ap.add_argument("--tickers", nargs="*", default=[])
    ap.add_argument("--from-file", default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="report namespace stats; change nothing")
    ap.add_argument("--verify-only", action="store_true",
                    help="skip delete+ingest; just run the retrieval check")
    args = ap.parse_args()

    tickers = list(dict.fromkeys(
        [t.upper() for t in args.tickers]
        + (read_ticker_file(args.from_file) if args.from_file else [])))
    if not tickers:
        sys.exit("no tickers given (--tickers and/or --from-file)")

    pinecone_index = _get_pinecone_index("sec-filings")

    if args.dry_run:
        stats = pinecone_index.describe_index_stats()
        namespaces = stats.get("namespaces", {}) or {}
        for t in tickers:
            ns = t.lower()
            count = namespaces.get(ns, {}).get("vector_count", 0)
            print(f"  {t:<6} namespace {ns!r}: {count} vectors — would "
                  f"{'delete + reindex' if count else 'index fresh'}")
        print(f"DRY RUN — no changes. {len(tickers)} tickers.")
        return

    _ensure_settings()
    ok, failed_fetch, failed_verify = [], [], []
    for t in tickers:
        ns = t.lower()
        try:
            if not args.verify_only:
                try:
                    pinecone_index.delete(delete_all=True, namespace=ns)
                except Exception:
                    pass  # namespace may not exist yet
                text = _fetch_filing_text(t, "10-K") or _fetch_filing_text(t, "10-Q")
                if not text:
                    failed_fetch.append(t)
                    print(f"  {t:<6} FETCH-FAILED (no 10-K/10-Q retrievable)", flush=True)
                    time.sleep(0.6)
                    continue
                vs = PineconeVectorStore(pinecone_index=pinecone_index, namespace=ns)
                VectorStoreIndex.from_documents(
                    [Document(text=text, metadata={"ticker": t, "source": "SEC EDGAR"})],
                    storage_context=StorageContext.from_defaults(vector_store=vs))
                time.sleep(4)  # serverless upserts are eventually consistent

            has_risk, has_boiler, n = verify(pinecone_index, ns)
            if n == 0:
                time.sleep(5)
                has_risk, has_boiler, n = verify(pinecone_index, ns)
            status = "PASS" if (has_risk and not has_boiler and n) else "FAIL"
            (ok if status == "PASS" else failed_verify).append(t)
            print(f"  {t:<6} {status}  nodes={n} risk_prose={has_risk} "
                  f"boilerplate={has_boiler}", flush=True)
        except Exception as e:  # noqa: BLE001
            failed_verify.append(t)
            print(f"  {t:<6} ERROR {type(e).__name__}: {str(e)[:90]}", flush=True)
        time.sleep(0.6)

    print(f"\nPASS {len(ok)} | FETCH-FAILED {len(failed_fetch)} "
          f"{failed_fetch} | VERIFY-FAILED {len(failed_verify)} {failed_verify}")


if __name__ == "__main__":
    main()
