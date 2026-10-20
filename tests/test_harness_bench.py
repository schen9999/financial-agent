"""Harness benchmark: corpus builder, model stub, driver and report
(docs/harness-benchmark-plan.md). No network beyond localhost, no credit:
the stub runs in a thread and the app's own SLM client, synthesis guard and
llama_index RAG prompt are exercised against it."""
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from langchain_core.messages import HumanMessage

from scripts import build_stub_corpus as corpus_mod
from scripts import harness_bench as driver_mod
from scripts import harness_bench_report as report
from scripts import model_stub as stub_mod

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "k8s" / "model-stub" / "corpus.json"


# ── corpus ──────────────────────────────────────────────────────────────────

def test_calls_by_ticker_maps_pods_and_drops_judge_sites():
    log = "\n".join([
        "[pod/wf-eval-one-1/main] Arms: slm-full-gpu   Tickers: AAPL",
        '[pod/wf-eval-one-1/main] EVAL_LLM_CALL {"site": "rag:risks", "prompt_tokens": 10, "completion_tokens": 5}',
        '[pod/wf-eval-one-1/main] EVAL_LLM_CALL {"site": "judge", "prompt_tokens": 99, "completion_tokens": 9}',
        '[pod/wf-eval-one-1/main] EVAL_LLM_CALL {"site": "synthesis", "prompt_tokens": 7, "completion_tokens": 3, "retry": true}',
        '[pod/wf-eval-one-2/main] EVAL_LLM_CALL {"site": "synthesis", "prompt_tokens": 8, "completion_tokens": 4}',
        "[pod/wf-eval-one-2/main] Arms: slm-full-gpu   Tickers: TM",
    ])
    out = corpus_mod.calls_by_ticker(log)
    assert out == {"AAPL": {"rag:risks": {"prompt_tokens": 10, "completion_tokens": 5}},
                   "TM": {"synthesis": {"prompt_tokens": 8, "completion_tokens": 4}}}


def test_texts_for_reads_sections_audited_and_rag():
    md = ("# X\n\n## Pre-written sections (judge input)\n\n### Financial Health\n\nFH body\n\n"
          "### Risk Factors\n\nRF body\n\n## Audited (Exec Summary + Outlook)\n\n"
          "### Executive Summary\nES body\n\n### Outlook\nOL body\n\n---\n*disclaimer*\n\n"
          "## Judge findings\n\nstuff")
    ragf = {"answers": {"risks": {"answer": "risk answer"}, "highlights": {}}}
    t = corpus_mod.texts_for(md, ragf)
    assert t["section:financial_health"] == "### Financial Health\n\nFH body"
    assert t["section:risk_factors"] == "### Risk Factors\n\nRF body"
    assert t["synthesis"] == {"executive_summary": "ES body", "outlook": "OL body"}
    assert t["rag:risks"] == "risk answer" and "rag:highlights" not in t


def test_committed_corpus_matches_the_proof_call_count():
    """nstp9's traffic proof: 270 harness calls = 35 tickers x 7 + 5 foreign x 5."""
    c = json.loads(CORPUS.read_text())
    assert c["source"]["run"] == "nstp9"
    assert sum(len(s) for s in c["tickers"].values()) == 270
    assert all(r["completion_tokens"] for s in c["tickers"].values() for r in s.values())
    assert set(c["tickers"]) == set(driver_mod.TICKERS)


# ── stub, unit ──────────────────────────────────────────────────────────────

def test_delay_profiles():
    assert stub_mod.delay_s("L0", 2299, 110) == 0
    assert stub_mod.delay_s("L1", 2299.5, 110.4) == pytest.approx(2.0)
    assert stub_mod.delay_s("L2", 109.8, 13.3) == pytest.approx(2.0)


def test_stock_block_empty_rule():
    full = 'Data:\nSTOCK DATA:\n{\n  "ticker": "X"\n}\n\nNEWS ARTICLES:\n[]'
    empty = "Data:\nSTOCK DATA:\n{}\n\nNEWS ARTICLES:\n[]"
    assert stub_mod.stock_block_empty(full) is False
    assert stub_mod.stock_block_empty(empty) is True
    assert stub_mod.stock_block_empty("nothing") is None


# ── stub, end to end through the app's own client ───────────────────────────

@pytest.fixture
def stub_server(monkeypatch):
    corpus = json.loads(CORPUS.read_text())
    stub = stub_mod.Stub(corpus, "model-stub", "k-test", "L0")
    srv = ThreadingHTTPServer(("127.0.0.1", 0), stub_mod.make_handler(stub))
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    for k, v in {"SLM_FULL": "true", "SLM_ENDPOINT": "cpu", "SLM_CPU_URL": url,
                 "SLM_CPU_API_KEY": "k-test", "SLM_MODEL_NAME": "model-stub",
                 "SLM_CPU_MODEL_NAME": "model-stub"}.items():
        monkeypatch.setenv(k, v)
    yield stub, url
    srv.shutdown()


def test_server_facts_and_key(stub_server):
    from agent.tools.slm import server_facts
    import requests
    stub, url = stub_server
    assert server_facts()["slm_served_name"] == "model-stub"
    assert requests.get(f"{url}/v1/models", timeout=5).status_code == 401


def test_section_and_synthesis_through_the_pipeline_code(stub_server):
    from agent import core
    from agent.grounding import missing_brief_sections
    stub, _ = stub_server
    ctx = 'STOCK DATA:\n{\n  "ticker": "AAPL"\n}\n\nNEWS ARTICLES:\n[]'
    sections = [core._haiku_section(h, ins, "Apple Inc.", "AAPL", ctx) for h, ins in core._SECTIONS]
    rec = json.loads(CORPUS.read_text())["tickers"]["AAPL"]
    for (h, _), text in zip(core._SECTIONS, sections):
        assert text == rec[core._section_site(h)]["text"]
    brief = core.synthesize("AAPL", "Apple Inc.", sections)
    assert missing_brief_sections(brief) == []
    for text in sections:                    # pre-written sections kept verbatim
        assert text in brief
    st = stub.stats()
    assert st["unmatched"] == 0 and st["requests"] == 5
    assert st["by_site"]["synthesis"] == 1 and st["stock_block_empty"] == 0


def test_rag_answer_through_llama_index(stub_server):
    """The real llama_index answer prompt: the ticker reaches the stub only
    through the chunk's metadata header."""
    from llama_index.core import Document, VectorStoreIndex
    from llama_index.core.embeddings import MockEmbedding
    from agent.tools.slm import llama_index_llm
    stub, _ = stub_server
    idx = VectorStoreIndex.from_documents(
        [Document(text="Risk text from a filing.", metadata={"ticker": "MSFT", "source": "SEC EDGAR"})],
        embed_model=MockEmbedding(embed_dim=8))
    eng = idx.as_query_engine(llm=llama_index_llm("rag:risks"), similarity_top_k=1)
    ans = str(eng.query("What are the primary risk factors disclosed?"))
    rec = json.loads(CORPUS.read_text())["tickers"]["MSFT"]["rag:risks"]
    assert ans == rec["text"]
    assert stub.stats()["by_site"] == {"rag:risks": 1} and stub.stats()["unmatched"] == 0


def test_unknown_ticker_gets_fallback_and_is_counted(stub_server):
    from agent import core
    stub, _ = stub_server
    out = core._haiku_section("### Financial Health", "x", "Nobody", "ZZZZ", "data")
    assert out.startswith("### Financial Health")
    assert stub.stats()["unmatched"] == 1


def test_profile_switch_and_reset(stub_server):
    import requests
    stub, url = stub_server
    assert requests.post(f"{url}/stats/profile", json={"profile": "L1"}, timeout=5).json() == {"profile": "L1"}
    assert requests.post(f"{url}/stats/profile", json={"profile": "L9"}, timeout=5).status_code == 400
    assert requests.post(f"{url}/stats/reset", timeout=5).json()["requests"] == 0
    assert stub.profile == "L1"


# ── driver ──────────────────────────────────────────────────────────────────

class FakeRedis:
    """Celery result backend stand-in: a task starts on its first poll after
    submission and finishes on the next."""
    def __init__(self):
        self.kv, self.polls = {}, {}

    def mget(self, keys):
        out = []
        for k in keys:
            n = self.polls[k] = self.polls.get(k, 0) + 1
            if n == 1:
                out.append(json.dumps({"status": "STARTED"}).encode())
            else:
                out.append(json.dumps({"status": "SUCCESS", "result": {
                    "brief": "### Executive Summary\na\n\n### Outlook\nb"}}).encode())
        return out

    def llen(self, _):
        return 0


def test_driver_closed_loop_counts_and_summary(monkeypatch, capsys):
    a = SimpleNamespace(cell="L0-r1-c2", repeat=1, profile="L0", replicas=1, concurrency=2,
                        briefs=6, warmup=1, queue_factor=3, api="http://api", stub="http://stub",
                        corpus=str(CORPUS), poll=0, queue_every=0, max_seconds=60)
    monkeypatch.setenv("REDIS_URL", "redis://unused")
    fake = FakeRedis()
    monkeypatch.setattr(driver_mod.redis.Redis, "from_url", staticmethod(lambda _: fake))
    d = driver_mod.Driver(a)
    n = {"i": 0}

    def post(url, json, timeout):
        n["i"] += 1
        r = MagicMock()
        r.json.return_value = {"job_id": f"j{n['i']}"}
        return r
    d.http.post = post
    stats = {"requests": 0, "errors": 0, "unmatched": 0, "max_in_flight": 0,
             "stock_block_empty": 0, "stock_block_unknown": 0}
    monkeypatch.setattr(d, "stub", lambda m, p, **kw: stats)
    s = d.run()
    assert s["warmup"] == 2                  # at least one per worker process
    assert s["measured"] == 6 and s["errors"] == 0 and s["bad_briefs"] == 0
    assert s["outstanding_target"] == 8
    assert s["completed"] >= 8               # warm-up + measured + drained tail
    assert s["stub_requests_expected"] == sum(
        driver_mod.expected_calls(json.loads(CORPUS.read_text()), t)
        for t in driver_mod.TICKERS[:s["completed"]])
    lines = capsys.readouterr().out.splitlines()
    assert sum(l.startswith("BENCH_BRIEF ") for l in lines) == s["completed"]


# ── report ──────────────────────────────────────────────────────────────────

def _write_repeat(root: Path, name: str, *, thr_window=360.0, capacity=1, cpu_after=30.0,
                  stub_req=None, restarts_after=0):
    d = root / name
    d.mkdir(parents=True)
    (d / "cell.log").write_text("x\n")
    briefs, t = [], 1000.0
    for i in range(1, 46):          # 5 warm-up + 40 measured, serial, 9 s each
        phase = "warmup" if i <= 5 else "measured"
        briefs.append({"n": i, "ticker": "AAPL", "submit": t - 1, "start": t, "finish": t + 9,
                       "state": "SUCCESS", "phase": phase})
        t += 9
    ms, me = briefs[4]["finish"], briefs[-1]["finish"]
    summary = {"replicas": 1, "concurrency": 1, "capacity": capacity, "briefs": 40,
               "completed": 45, "measured": 40, "errors": 0, "bad_briefs": 0,
               "measure_start": ms, "measure_end": me, "queue_samples": [{"t": 0, "llen": 3}],
               "stub_requests_expected": 45 * 7,
               "stub_after": {"requests": stub_req if stub_req is not None else 45 * 7,
                              "errors": 0, "unmatched": 0, "max_in_flight": 4,
                              "stock_block_empty": 0, "stock_block_unknown": 0}}
    (d / "driver.log").write_text("\n".join(
        [f"BENCH_BRIEF {json.dumps(b)}" for b in briefs] + [f"BENCH_SUMMARY {json.dumps(summary)}"]))
    for which, cpu in (("before", 0.0), ("after", cpu_after)):
        (d / f"cgroup-{which}.txt").write_text(
            f"=== pod worker-abc-1 t=1\ncgroup v2\nusage_usec {int(cpu * 1e6)}\n"
            f"nr_periods {200 if which == 'after' else 100}\n"
            f"nr_throttled {10 if which == 'after' else 0}\nthrottled_usec 0\n"
            f"memory.peak {1024 * 2**20}\n"
            f"=== pod api-x-1 t=1\ncgroup v2\nusage_usec {int(cpu * 1e5)}\n")
        rc = restarts_after if which == "after" else 0
        (d / f"pods-{which}.json").write_text(json.dumps({"items": [{
            "metadata": {"name": "worker-abc-1"},
            "status": {"containerStatuses": [{"restartCount": rc, "lastState": (
                {"terminated": {"reason": "OOMKilled"}} if rc else {})}]}}]}))
    (d / "events.json").write_text(json.dumps({"items": []}))
    return d


def test_report_metrics_and_rules(tmp_path):
    _write_repeat(tmp_path, "L1-r1-c1-r1", cpu_after=45.0)   # 1 CPU-s per brief
    _write_repeat(tmp_path, "L1-r1-c1-r2", cpu_after=45.0)
    _write_repeat(tmp_path, "L0-r1-c1-r1", cpu_after=45.0)
    assert report.main([str(tmp_path)]) == 0
    res = json.loads((tmp_path / "results.json").read_text())
    r = next(x for x in res["repeats"] if x["dir"] == "L1-r1-c1-r1")
    assert r["valid"], r["reasons"]
    assert r["throughput_per_h"] == pytest.approx(400.0)      # 40 briefs / 360 s
    assert r["latency_p50"] == pytest.approx(9.0)
    assert r["cpu_s_per_brief"]["worker"] == pytest.approx(1.0)
    assert r["worker_cpu_over_wall"] == pytest.approx(1 / 9)
    assert r["throttled_frac"] == pytest.approx(0.1)
    assert r["little_gap"] == pytest.approx(0.0)
    assert r["mem_peak_per_process_mib"] == pytest.approx(1024)
    rules = res["reading_rules"]
    assert rules["Q2_wait_vs_work"]["(1,1)"]["reading"].startswith("waiting")
    assert rules["Q1_overhead"]["latency_p50_s"] == pytest.approx(9.0)
    assert rules["Q4_sizing"]["(1,1)"]["worker_vcpu"] == pytest.approx(400 / 3600)


def test_report_invalidates_on_missing_calls_and_restarts(tmp_path):
    _write_repeat(tmp_path, "L0-r4-c4-r1", stub_req=300, restarts_after=1)
    report.main([str(tmp_path)])
    r = json.loads((tmp_path / "results.json").read_text())["repeats"][0]
    assert not r["valid"]
    assert any("stub requests 300" in x for x in r["reasons"])
    assert any("OOMKilled" in x for x in r["reasons"])


def test_saturation_rule():
    def cell(p, r, c, thr):
        return {"cell": f"{p}-r{r}-c{c}", "profile": p, "keda": False, "replicas": r,
                "concurrency": c, "valid_repeats": 2, "throughput_per_h": thr,
                "latency_p50": 1, "worker_cpu_s_per_brief": 1, "worker_cpu_over_wall": 0.5,
                "mem_peak_per_process_mib": 1}
    agg = {x["cell"]: x for x in [cell("L1", 1, 1, 100), cell("L1", 2, 1, 195),
                                   cell("L1", 1, 2, 190), cell("L1", 2, 2, 205),
                                   cell("L1", 4, 1, 200), cell("L1", 4, 2, 210),
                                   cell("L1", 1, 4, 200), cell("L1", 2, 4, 206)]}
    q3 = report.reading_rules(agg)["Q3_saturation"]["L1"]
    assert q3["saturation_at"] == ["(1,2)", "(2,1)"]
    assert q3["doubling_gains"]["(1,1)"]["2x replicas"] == pytest.approx(0.95)
