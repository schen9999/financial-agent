#!/usr/bin/env python3
"""Repeated chunks in a RAG query's retrieved top-k, from committed
.ragf.json files (offline).

A query whose retrieved chunks contain the same text twice points at
duplicate vectors in the ticker's Pinecone namespace. Likely mechanism,
from reading the code (not reproduced): agent/core.py:122-131 runs the
highlights and risks queries in two threads, and agent/tools/rag.py:283-319
indexes the filing into the namespace whenever the cache query raises (bare
except, :295) or answers in 50 characters or fewer — so two threads on a
new ticker, or any failed query, can index the same filing twice.

Per run: queries with chunks, queries whose chunks contain a repeat, and
the queries whose chunks are all one text.

  python eval/rag_chunk_duplicates.py 4hsn2 nstp9 vks4c 2mzdd 9jzmj xgtxx
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_duplicates(run: str) -> dict:
    queries, repeated, single = 0, [], []
    for f in sorted((ROOT / "eval" / "runs" / "raw" / f"{run}-findings").glob("*.ragf.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for site, ans in sorted(d.get("answers", {}).items()):
            chunks = ans.get("chunks") or []
            if not chunks:
                continue
            queries += 1
            distinct = len(set(chunks))
            if distinct < len(chunks):
                repeated.append(f"{d['ticker']}:{site} ({distinct} distinct of {len(chunks)})")
            if len(chunks) > 1 and distinct == 1:
                single.append(f"{d['ticker']}:{site}")
    return {"run": run, "queries": queries, "repeated": repeated, "single": single}


def main(argv=None) -> int:
    runs = argv if argv is not None else sys.argv[1:]
    if not runs:
        print(__doc__)
        return 2
    for run in runs:
        r = run_duplicates(run)
        print(f"{r['run']}: {len(r['repeated'])}/{r['queries']} queries with a repeated chunk; "
              f"all one chunk: {', '.join(r['single']) or '-'}")
        print(f"  {'; '.join(r['repeated'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
