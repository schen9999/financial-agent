#!/usr/bin/env python3
"""Rebuild an eval run's per-ticker results from its pods' logs, for the
aggregate step that never ran.

The 40-ticker hosted run 9jzmj (2026-10-04, image 1f51dad) finished all 40
eval pods and then errored at the aggregate: the controller could not create
the ConfigMap it offloads an oversized step template to (argo/base/rbac.yaml
has the story). The per-ticker results it would have aggregated were Argo
output parameters, which are not in the pod logs — but everything they were
computed from is. Each eval pod's log carries its findings dump (the judge's
findings, the judged context, the per-site LLM ledger in the metadata, the
RAG-faithfulness verdicts), its result line and its attempt record. This
script turns those back into the rows scripts/eval_aggregate.py reads, using
the same functions the harness used:

  supported / unsupported / inference / total   eval.label.count_labels_deduped
  numeric_claims                                eval.label.numeric_claim_counts
  stock_block_empty                             eval.stock_block.stock_block_empty
  llm (per site)                                the findings metadata's llm_by_site
  rag_faithfulness                              the pod's <ticker>_<arm>.ragf.json
  retrieval_s, pipeline_s                       the pod's result line (2 decimals)
  attempt                                       its EVAL_ATTEMPT record

Not reconstructable: est_cost (it needs the full brief text), so the
aggregate prints no estimated run cost for a rebuilt run.

It checks what it rebuilds instead of trusting it — and stops on:
  - a result line whose SUP/UNSUP/INF counts differ from the recount of
    that pod's findings
  - a pod whose EVAL_LLM_CALL lines (agent calls) disagree with its
    llm_by_site metadata in calls or tokens
  - a ticker that was skipped, failed its attempt, or appears twice
  - an arm that used more than one endpoint (per-endpoint sums would be a guess)

With --aggregate-out it then runs scripts/eval_aggregate.py on the rebuilt
rows (the unchanged aggregate code) and, when the log contains an aggregate
pod's own output, compares the two line by line — the validation run on
7c66k before 9jzmj was rebuilt.

  python scripts/results_from_pod_log.py --log eval/runs/raw/9jzmj.log \\
      --out eval/runs/9jzmj-results-rebuilt.json --aggregate-out eval/runs/9jzmj-aggregate.txt
"""
import argparse
import base64
import io
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from eval import attempts  # noqa: E402
from eval.label import count_labels_deduped, numeric_claim_counts, parse_findings_file  # noqa: E402
from eval.stock_block import stock_block_empty  # noqa: E402

EVAL_SITES = ("judge", "rag_judge")  # grounding_check._EVAL_SITES: not agent calls
_RESULT_LINE = re.compile(
    r"\[(?P<ticker>[A-Z.-]{1,6}) \| (?P<arm>[\w-]+)\]\s+(?P<sup>\d+) SUP\s+(?P<uns>\d+) UNSUP\s+"
    r"(?P<inf>\d+) INF\s+\((?P<tot>\d+) claims\)\s+retrieval=(?P<retr>[\d.]+)s\s+"
    r"pipeline=(?P<pipe>[\d.]+)s")
_TGZ = re.compile(r"===EVAL_FINDINGS_TGZ_BEGIN[^\n]*===\n(.*?)\n[^\n]*===EVAL_FINDINGS_TGZ_END===", re.S)
_SUMMED = ("calls", "prompt_tokens", "completion_tokens", "prompt_tokens_unrecorded",
           "completion_tokens_unrecorded", "truncated", "repeat_run", "retry", "parse_failure",
           "format_failure", "errors")


class RebuildError(SystemExit):
    pass


def findings_files(pod_log: str) -> dict:
    """{file name: bytes} from the pod's findings dump (empty if none)."""
    out = {}
    for body in _TGZ.findall(pod_log):
        b64 = "".join(line.strip() for line in body.splitlines())
        if not b64:
            continue
        with tarfile.open(fileobj=io.BytesIO(base64.b64decode(b64)), mode="r:gz") as tf:
            for m in tf.getmembers():
                if m.isfile():
                    out[Path(m.name).name] = tf.extractfile(m).read()
    return out


def _sum_sites(by_site: dict) -> dict:
    tot = {k: sum(s[k] for s in by_site.values()) for k in _SUMMED}
    lat = [s["latency_s_total"] for s in by_site.values()]
    mx = [s["latency_s_max"] for s in by_site.values() if s["latency_s_max"] is not None]
    tot["latency_s_total"] = round(sum(lat), 3)
    tot["latency_s_max"] = round(max(mx), 3) if mx else None
    return tot


def rebuild_row(pod: str, pod_log: str, md_name: str, files: dict) -> dict:
    p = parse_findings_file(files[md_name].decode("utf-8"))
    if not p or "metadata" not in p:
        raise RebuildError(f"{pod}: {md_name} is not an extended-format findings file")
    meta = p["metadata"]
    ticker, arm = meta["ticker"], meta["arm"]
    where = f"{pod} ({ticker} | {arm})"

    counts = count_labels_deduped(p["findings"])
    counts.pop("duplicates_suppressed")
    line = next((m for m in _RESULT_LINE.finditer(pod_log)
                 if m["ticker"] == ticker and m["arm"] == arm), None)
    if line is None:
        raise RebuildError(f"{where}: no result line in the pod log — the ticker did not finish")
    printed = {"supported": int(line["sup"]), "unsupported": int(line["uns"]),
               "inference": int(line["inf"]), "total": int(line["tot"])}
    if printed != counts:
        raise RebuildError(f"{where}: result line says {printed}, the findings recount {counts}")

    parsed = attempts.parse_pod_log(pod_log)
    end = parsed["end"] or {}
    if end.get("outcome") != "ok":
        raise RebuildError(f"{where}: attempt record is {end or 'missing'} — not a finished attempt")

    by_site = json.loads(meta["llm_by_site"])
    endpoints = [e for e in meta.get("llm_endpoints", "").split(",") if e]
    if len(endpoints) != 1:
        raise RebuildError(f"{where}: agent calls on endpoints {endpoints}; per-endpoint sums "
                           f"cannot be rebuilt from per-site sums")
    agent_calls = [c for c in parsed["calls"] if c["site"] not in EVAL_SITES]
    logged = {"calls": len(agent_calls),
              "prompt_tokens": sum(c["prompt_tokens"] or 0 for c in agent_calls),
              "completion_tokens": sum(c["completion_tokens"] or 0 for c in agent_calls)}
    total = _sum_sites(by_site)
    if logged != {k: total[k] for k in logged} or {c["endpoint"] for c in agent_calls} - set(endpoints):
        raise RebuildError(f"{where}: EVAL_LLM_CALL lines {logged} disagree with llm_by_site "
                           f"{ {k: total[k] for k in logged} }")

    row = {"ticker": ticker, "arm": arm, "judge_version": meta.get("judge_prompt_version"),
           "attempt": end.get("attempt", 0),
           "numeric_claims": numeric_claim_counts(p["findings"]),
           "retrieval_s": float(line["retr"]), "pipeline_s": float(line["pipe"]),
           "stock_block_empty": stock_block_empty(p["context"]),
           **counts,
           "llm": {"total": total, "by_site": by_site, "by_endpoint": {endpoints[0]: total},
                   "endpoints": endpoints}}
    ragf_name = md_name[:-len(".md")] + ".ragf.json"
    if ragf_name in files:
        answers = json.loads(files[ragf_name].decode("utf-8"))["answers"]
        row["rag_faithfulness"] = {which: {k: a[k] for k in ("supported", "unsupported", "total")}
                                   for which, a in answers.items()}
    for prefix, key in (("slm_", "slm"), ("local_model_", "local_model")):
        prov = {k: v for k, v in meta.items() if k.startswith(prefix)}
        if prov:
            row[key] = prov
    return row


def rebuild(log_text: str) -> list:
    """One payload per finished (ticker, arm), in ticker order."""
    if "SKIPPED after retries" in log_text:
        raise RebuildError("the log has a ticker 'SKIPPED after retries' — a handled failure's "
                           "record cannot be rebuilt from the log; not supported")
    rows = {}
    for pod, text in attempts.split_pod_logs(log_text).items():
        files = findings_files(text)
        for name in sorted(n for n in files if n.endswith(".md")):
            row = rebuild_row(pod, text, name, files)
            key = (row["ticker"], row["arm"])
            if key in rows:
                raise RebuildError(f"{key} has findings in two pods ({pod} and another)")
            rows[key] = row
    return [{"results": [rows[k]], "skipped": [], "failures": [],
             "rebuilt_from": "pod log (scripts/results_from_pod_log.py)"} for k in sorted(rows)]


def in_cluster_aggregate(log_text: str):
    """The aggregate pod's own printed report, or None if no aggregate ran."""
    for pod, text in attempts.split_pod_logs(log_text).items():
        if "-aggregate-" in pod and "NIGHTLY GROUNDING EVAL" in text:
            lines = text.splitlines()
            start = next(i for i, ln in enumerate(lines) if set(ln.strip()) == {"="})
            end = max(i for i, ln in enumerate(lines) if set(ln.strip()) == {"="})
            return [ln.rstrip() for ln in lines[start:end + 1]]
    return None


def compare(offline: list, cluster: list) -> list:
    """Lines that differ, as (side, line); the estimated-cost line is the one
    expected difference and is reported separately by the caller."""
    a = [ln for ln in offline if ln.strip()]
    b = [ln for ln in cluster if ln.strip()]
    return [("offline only", ln) for ln in a if ln not in b] + \
           [("in-cluster only", ln) for ln in b if ln not in a]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--log", required=True, help="every pod's log, --prefix form")
    ap.add_argument("--out", required=True, help="rebuilt results (the aggregate's --input)")
    ap.add_argument("--aggregate-out", default=None,
                    help="run the aggregate on the rebuilt rows and save its output here")
    ap.add_argument("--max-unsupported-pct", default="5")
    ap.add_argument("--min-claims", default="30")
    args = ap.parse_args(argv)
    log_text = Path(args.log).read_text(encoding="utf-8", errors="replace")
    payloads = rebuild(log_text)
    Path(args.out).write_text(json.dumps(payloads, indent=1, sort_keys=True) + "\n",
                              encoding="utf-8", newline="\n")
    print(f"rebuilt {len(payloads)} ticker result(s) from {args.log} -> {args.out}")
    print("  every result line matches its findings recount; every pod's EVAL_LLM_CALL lines "
          "match its llm_by_site; all attempts ended ok")
    if not args.aggregate_out:
        return 0
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "eval_aggregate.py"), "--input", args.out,
         "--max-unsupported-pct", args.max_unsupported_pct, "--min-claims", args.min_claims],
        capture_output=True, text=True, encoding="utf-8",
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "EVAL_ARTIFACTS_PUT_URL": ""})
    offline = [ln.rstrip() for ln in proc.stdout.splitlines()]
    Path(args.aggregate_out).write_text(
        "\n".join(offline) + f"\n(aggregate exit code {proc.returncode}; rebuilt offline from "
        f"{Path(args.log).name} by scripts/results_from_pod_log.py; est. run cost not "
        f"reconstructable)\n", encoding="utf-8", newline="\n")
    print(f"aggregate (scripts/eval_aggregate.py, exit {proc.returncode}) -> {args.aggregate_out}")
    if proc.stderr.strip():
        print("  aggregate stderr: " + proc.stderr.strip()[:500])
    cluster = in_cluster_aggregate(log_text)
    if cluster is None:
        print("no aggregate pod output in this log to compare with")
        return 0
    diffs = compare(offline, cluster)
    cost = [d for d in diffs if "est. run cost" in d[1]]
    other = [d for d in diffs if d not in cost]
    print(f"compared with the in-cluster aggregate ({len([ln for ln in cluster if ln.strip()])} "
          f"lines): {len(diffs)} differing line(s)")
    for side, ln in cost:
        print(f"  expected ({side}): {ln.strip()}")
    for side, ln in other:
        print(f"  DIFFERENT ({side}): {ln.strip()}")
    print("VALIDATION: " + ("EXACT apart from the estimated-cost line" if not other
                            else f"{len(other)} unexpected difference(s)"))
    return 0 if not other else 1


if __name__ == "__main__":
    sys.exit(main())
