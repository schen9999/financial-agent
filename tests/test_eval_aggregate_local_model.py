"""scripts/eval_aggregate.py — the aggregate names the model that served the
local-model arm, so runs against different models can be told apart."""
import importlib.util
import json
import pathlib

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "eval_aggregate.py"
_spec = importlib.util.spec_from_file_location("eval_aggregate", _MOD_PATH)
eval_aggregate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eval_aggregate)

PROV = {"local_model_served_name": "qwen7b", "local_model_dir": "qwen2.5-7b-instruct",
        "local_model_backend": "openai", "local_model_url": "http://vllm.financial-agent.svc:8000"}


def _row(ticker, **extra):
    return {"ticker": ticker, "supported": 5, "unsupported": 0, "inference": 0,
            "total": 5, "retrieval_s": 1.0, "pipeline_s": 2.0, **extra}


def _run(monkeypatch, tmp_path, rows):
    f = tmp_path / "all.json"
    f.write_text(json.dumps([json.dumps({"results": rows, "skipped": []})]), encoding="utf-8")
    monkeypatch.delenv("EVAL_ARTIFACTS_PUT_URL", raising=False)
    monkeypatch.setattr(eval_aggregate.sys, "argv",
                        ["eval_aggregate.py", "--input", str(f), "--min-claims", "1"])
    eval_aggregate.main()


def test_local_model_line_printed(monkeypatch, tmp_path, capsys):
    _run(monkeypatch, tmp_path, [_row("AAPL", local_model=PROV), _row("NVDA", local_model=PROV)])
    out = capsys.readouterr().out
    assert out.count("local model       : qwen7b (dir qwen2.5-7b-instruct, openai @ ") == 1
    assert "mixes models" not in out


def test_baseline_rows_print_no_local_model(monkeypatch, tmp_path, capsys):
    _run(monkeypatch, tmp_path, [_row("AAPL"), _row("NVDA")])
    assert "local model" not in capsys.readouterr().out


def test_mixed_models_warn(monkeypatch, tmp_path, capsys):
    other = {**PROV, "local_model_served_name": "financial-lora", "local_model_dir": "qwen-ft"}
    _run(monkeypatch, tmp_path, [_row("AAPL", local_model=PROV), _row("NVDA", local_model=other)])
    out = capsys.readouterr().out
    assert "qwen7b" in out and "financial-lora" in out
    assert "WARNING: rows served by more than one local model" in out
