"""scripts/bench_table.py: rows come from the result JSON and its --metadata,
pre-metadata A10 files are labeled as such, and an incomplete run is refused."""
import importlib.util
import json
import pathlib

import pytest

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "bench_table.py"
_spec = importlib.util.spec_from_file_location("bench_table", _MOD_PATH)
bt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bt)

BASE = {
    "num_prompts": 50, "completed": 50, "max_concurrency": 1,
    "output_throughput": 12.345, "total_token_throughput": 61.2,
    "request_throughput": 0.0482,
    "mean_ttft_ms": 1500.4, "median_ttft_ms": 1490.0, "p99_ttft_ms": 1702.9,
    "mean_tpot_ms": 75.04, "median_tpot_ms": 74.96, "p99_tpot_ms": 80.0,
    "mean_e2el_ms": 20640.0, "median_e2el_ms": 20600.0, "p99_e2el_ms": 21000.0,
}


def _write(tmp_path, name, **extra):
    p = tmp_path / name
    p.write_text(json.dumps({**BASE, **extra}), encoding="utf-8")
    return p


def test_cpu_row_uses_metadata(tmp_path):
    p = _write(tmp_path, "lora-c1.json", device="cpu", backend="vllm-cpu",
               backend_version="0.10.2", dtype="bfloat16", pinned_cores="14",
               cpu_model="Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz")
    out = bt.table([f"{p}=CPU"])
    line = out.splitlines()[2]
    assert line.startswith("| CPU | Intel(R) Xeon(R) Platinum 8358")
    assert "| vllm-cpu 0.10.2 | bfloat16 | 14 | 1 | 50 |" in line
    assert "| 12.3 | 61.2 | 0.048 |" in line
    assert "1500 / 1490 / 1703" in line
    assert "75.0 / 75.0 / 80.0" in line


def test_gpu_and_pre_metadata_rows(tmp_path):
    new = _write(tmp_path, "a.json", device="gpu", backend="vllm",
                 backend_version="0.10.2", dtype="bfloat16", gpu_model="NVIDIA A10")
    old = _write(tmp_path, "financial-lora.json")
    lines = bt.table([str(new), str(old)]).splitlines()
    assert "| a | NVIDIA A10 | vllm 0.10.2 | bfloat16 | n/a |" in lines[2]
    assert "| financial-lora | A10 (pre-metadata) | vllm 0.10.2 | bfloat16 | n/a |" in lines[3]
    assert len(lines[0].split("|")) == len(lines[2].split("|"))


def test_prefix_cache_column(tmp_path):
    new = _write(tmp_path, "new.json", prefix_cache_hit_tokens=1008,
                 prefix_cache_query_tokens=52016)
    old = _write(tmp_path, "old.json")
    lines = bt.table([str(new), str(old)]).splitlines()
    assert lines[0].endswith("| Prefix-cache hits |")
    assert lines[2].endswith("| 1.9% |")
    assert lines[3].endswith("| not recorded |")


def test_incomplete_run_refused(tmp_path):
    p = _write(tmp_path, "short.json", completed=49)
    with pytest.raises(ValueError, match="completed 49 of 50"):
        bt.table([str(p)])


def test_section_time_only_for_concurrency_one(tmp_path):
    c1 = _write(tmp_path, "c1.json")
    c8 = _write(tmp_path, "c8.json", max_concurrency=8)
    # 2 x 1500.4 ms + 530 x 75.04 ms = 42.77 s; at 1024: 79.84 s
    assert bt.section_lines([f"{c1}=CPU", f"{c8}=CPU8"], [530, 1024]) == [
        "- CPU: 42.8 s at T = 530; 79.8 s at T = 1024"]


def test_committed_a10_file_renders():
    root = pathlib.Path(__file__).resolve().parents[1]
    out = bt.table([str(root / "eval/runs/bench/financial-lora.json")])
    assert "| 711.5 |" in out
