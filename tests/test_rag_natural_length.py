"""scripts/rag_natural_length.py: rebuilding a smoke run's RAG requests from
its captured log, and the stdlib-only sender's statistics and prompt check."""
import base64
import io
import json
import sys
import tarfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import rag_natural_length as rnl  # noqa: E402


def _pod_log(ticker, by_site, chunks):
    files = {
        f"eval_findings/{ticker}_slm-full-cpu.ragf.json": json.dumps(
            {"ticker": ticker, "answers": {w: {"chunks": c, "answer": "a"} for w, c in chunks.items()}}),
        f"eval_findings/{ticker}_slm-full-cpu.md":
            f"# {ticker}\n\n## Metadata\n\nticker: {ticker}\nllm_by_site: {json.dumps(by_site)}\n",
    }
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for name, text in files.items():
            data = text.encode("utf-8")
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    b64 = base64.b64encode(buf.getvalue()).decode()
    pre = f"[pod/eval-{ticker}/main] "
    return "\n".join([f"{pre}===EVAL_FINDINGS_TGZ_BEGIN pod=eval-{ticker}===",
                      pre + b64[:60], pre + b64[60:],
                      f"{pre}===EVAL_FINDINGS_TGZ_END==="]) + "\n"


def _site(prompt, completion, truncated):
    return {"calls": 1, "prompt_tokens": prompt, "completion_tokens": completion,
            "truncated": truncated}


def test_read_smoke_recovers_chunks_and_ledger():
    log = _pod_log("AAPL", {"rag:highlights": _site(2306, 487, 0), "rag:risks": _site(2295, 512, 1)},
                   {"highlights": ["c1", "c2"], "risks": ["c3"]})
    smoke = rnl.read_smoke(log)
    assert smoke["AAPL"]["chunks"] == {"highlights": ["c1", "c2"], "risks": ["c3"]}
    assert smoke["AAPL"]["by_site"]["rag:risks"]["prompt_tokens"] == 2295


def test_rebuild_messages_is_one_call_with_indexed_metadata(monkeypatch):
    monkeypatch.setenv("SLM_FULL", "true")
    msgs = rnl.rebuild_messages("AAPL", "What are the primary risk factors disclosed?",
                                ["Chunk one text.", "Chunk two text."], "rag:risks")
    assert [m["role"] for m in msgs] == ["system", "user"]
    user = msgs[1]["content"]
    assert user.count("ticker: AAPL\nsource: SEC EDGAR\n\n") == 2
    assert user.index("Chunk one text.") < user.index("Chunk two text.")
    assert "Query: What are the primary risk factors disclosed?" in user


def test_build_keeps_rag_profile_and_replaces_only_max_tokens(tmp_path, monkeypatch):
    from agent.tools import slm
    monkeypatch.delenv("LOCAL_MODEL_THINKING", raising=False)
    sites = {"rag:highlights": _site(100, 50, 0), "rag:risks": _site(90, 512, 1)}
    log = tmp_path / "run.log"
    log.write_text(_pod_log("V", sites, {"highlights": ["h"], "risks": ["r"]}), encoding="utf-8")
    out = tmp_path / "req.json"
    assert rnl.main(["build", "--log", str(log), "--out", str(out), "--max-tokens", "4096"]) == 0
    doc = json.loads(out.read_text(encoding="utf-8"))
    assert [(r["ticker"], r["site"], r["smoke_prompt_tokens"], r["smoke_truncated"])
            for r in doc["requests"]] == [("V", "rag:highlights", 100, False),
                                          ("V", "rag:risks", 90, True)]
    body = dict(doc["requests"][0]["body"])
    body.pop("messages")
    assert body == {**slm.request_params("rag"), "max_tokens": 4096}
    assert body["chat_template_kwargs"] == {"enable_thinking": False}


def test_summarize_and_percentile():
    assert rnl.percentile([1, 2, 3, 4], 0.5) == 2.5
    rows = [{"site": "rag:risks", "completion_tokens": n, "finish_reason": f}
            for n, f in ((300, "stop"), (600, "stop"), (900, "stop"), (4096, "length"))]
    rows.append({"site": "rag:risks", "error": "URLError"})
    s = rnl.summarize(rows)
    assert s["rag:highlights"] is None
    assert s["rag:risks"] == {"n": 4, "min": 300, "median": 750.0, "p95": pytest.approx(3616.6),
                              "max": 4096, "hit_max_tokens": 1, "over_512": 3, "over_800": 2,
                              "over_1024": 1}
    assert s["both"]["n"] == 4


def _requests_file(tmp_path, prompt_tokens):
    doc = {"max_tokens": 4096, "sampling": {}, "source_log": "x.log",
           "requests": [{"ticker": "V", "site": "rag:risks", "smoke_prompt_tokens": prompt_tokens,
                         "smoke_completion_tokens": 512, "smoke_truncated": True,
                         "body": {"messages": [{"role": "user", "content": "q"}], "max_tokens": 4096}}]}
    p = tmp_path / "req.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def _fake_http(sent):
    def http(url, key, body, timeout):
        sent.append((url, key, body))
        if url.endswith("/v1/models"):
            return {"data": [{"id": "qwen"}]}
        if url.endswith("/props"):
            return {"build_info": "b11347"}
        return {"choices": [{"message": {"content": "answer"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 90, "completion_tokens": 700}}
    return http


def _run_args(tmp_path, req):
    return rnl.argparse.Namespace(requests=str(req), url="http://localhost:30880/",
                                  api_key_env="RNL_TEST_KEY", model=None, concurrency=2,
                                  timeout=5.0, out=str(tmp_path / "out.json"))


def test_run_sends_key_and_model_and_passes_on_exact_prompts(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("RNL_TEST_KEY", "k")
    sent = []
    assert rnl.run(_run_args(tmp_path, _requests_file(tmp_path, 90)), http=_fake_http(sent)) == 0
    url, key, body = sent[-1]
    assert (url, key) == ("http://localhost:30880/v1/chat/completions", "k")
    assert body["model"] == "qwen" and body["max_tokens"] == 4096
    out = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    assert out["prompt_check"] == "EXACT" and out["summary"]["rag:risks"]["max"] == 700
    assert "PROMPT CHECK: EXACT" in capsys.readouterr().out


def test_run_fails_when_a_prompt_is_not_token_identical(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("RNL_TEST_KEY", "k")
    assert rnl.run(_run_args(tmp_path, _requests_file(tmp_path, 95)), http=_fake_http([])) == 1
    assert "V rag:risks: server 90 vs smoke 95 (-5)" in capsys.readouterr().out


def test_run_refuses_an_empty_key(tmp_path, monkeypatch):
    monkeypatch.delenv("RNL_TEST_KEY", raising=False)
    with pytest.raises(SystemExit, match="RNL_TEST_KEY"):
        rnl.run(_run_args(tmp_path, _requests_file(tmp_path, 90)), http=_fake_http([]))
