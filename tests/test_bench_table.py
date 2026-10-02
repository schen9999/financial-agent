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


def _run(tmp_path, name, conc, **meta):
    extra = {"max_concurrency": conc, "output_throughput": 100.0 + conc,
             "mean_e2el_ms": 2500.0 * conc, "median_ttft_ms": 40.0 * conc,
             "median_tpot_ms": 9.0 + conc}
    return _write(tmp_path, name, **{**extra, **meta})


GPU = dict(device="gpu", backend="vllm", backend_version="0.10.2", dtype="bfloat16",
           gpu_model="NVIDIA A10")
LLAMA = dict(device="cpu", backend="llama.cpp", backend_version="b11223",
             cpu_model="Xeon", llamacpp_prompt_tokens_processed=1000)


def test_quantized_precision_cells(tmp_path):
    w4 = _write(tmp_path, "w4.json", **GPU, quantization="w4a16-g128")
    q4 = _write(tmp_path, "q4.json", **LLAMA, dtype="Q4_K_M", quantization="Q4_K_M",
                pinned_cores="14")
    bf = _write(tmp_path, "bf.json", **GPU, quantization="none")
    lines = bt.table([str(w4), str(q4), str(bf)]).splitlines()
    assert "| w4a16-g128 (bfloat16) |" in lines[2]
    assert "| llama.cpp b11223 | Q4_K_M | 14 |" in lines[3]
    assert lines[3].endswith("| n/a (llama.cpp) |")
    assert "| vllm 0.10.2 | bfloat16 |" in lines[4]


def test_directory_expands_to_its_json_files(tmp_path):
    _write(tmp_path, "b.json")
    _write(tmp_path, "a.json")
    (tmp_path / "load.log").write_text("x", encoding="utf-8")
    (tmp_path / "quant_meta.json").write_text('{"scheme": "W4A16"}', encoding="utf-8")
    assert [pathlib.Path(p).name for p in bt.expand([str(tmp_path)])] == ["a.json", "b.json"]


def test_matrix_rows_per_engine_precision_device(tmp_path):
    old = tmp_path / "old"
    old.mkdir()
    _run(old, "bf-c8.json", 8, **GPU)
    _run(old, "bf-c1.json", 1, **GPU)
    _run(tmp_path, "w4-c8.json", 8, **GPU, quantization="w4a16-g128", weights_bytes="1161000000")
    _run(tmp_path, "w4-c1.json", 1, **GPU, quantization="w4a16-g128", weights_bytes="1161000000")
    _run(tmp_path, "q4-c1.json", 1, **LLAMA, dtype="Q4_K_M", quantization="Q4_K_M")
    _run(tmp_path, "q4-c8.json", 8, **LLAMA, dtype="Q4_K_M", quantization="Q4_K_M")
    out = bt.matrix([str(old), str(tmp_path / "w4-c8.json"), str(tmp_path / "w4-c1.json"),
                     str(tmp_path / "q4-c1.json"), str(tmp_path / "q4-c8.json")],
                    {str(old): 3087466808})
    lines = out.splitlines()
    assert lines[0] == ("| Engine | Precision | Device | Output tok/s (c=8) | Mean E2E s (c=1) "
                        "| TTFT p50 ms (c=1) | Weights on disk (GB) |")
    assert lines[2] == "| vllm 0.10.2 | bfloat16 | NVIDIA A10 | 108.0 | 2.5 | 40 | 3.09 |"
    assert lines[3] == "| vllm 0.10.2 | w4a16-g128 | NVIDIA A10 | 108.0 | 2.5 | 40 | 1.16 |"
    assert lines[4] == "| llama.cpp b11223 | Q4_K_M | Xeon | 108.0 | 2.5 | 40 | not recorded |"


def test_matrix_needs_both_concurrencies(tmp_path):
    p = _run(tmp_path, "c8.json", 8, **GPU)
    with pytest.raises(ValueError, match=r"needs one concurrency-8 and one concurrency-1 file, got \[8\]"):
        bt.matrix([str(p)])


def test_sweep_concurrency_by_threads(tmp_path):
    cpu = dict(device="cpu", backend="vllm-cpu", backend_version="0.10.2",
               dtype="bfloat16", cpu_model="Xeon")
    for t in (7, 14):
        for c in (1, 16):
            _run(tmp_path, f"s-t{t}-c{c}.json", c, **cpu, pinned_cores=str(t))
    _run(tmp_path, "q-t14-c1.json", 1, **LLAMA, dtype="Q4_K_M", quantization="Q4_K_M",
         pinned_cores="14")
    blocks = bt.sweep([str(tmp_path)]).split("\n\n")
    assert blocks[0] == "llama.cpp b11223, Q4_K_M, Xeon: output tok/s / TTFT p50 ms / TPOT p50 ms"
    assert blocks[1].splitlines() == ["| Concurrency | 14 threads |", "|---|---|",
                                      "| 1 | 101.0 / 40 / 10.0 |"]
    assert blocks[3].splitlines()[0] == "| Concurrency | 7 threads | 14 threads |"
    assert blocks[3].splitlines()[3] == "| 16 | 116.0 / 640 / 25.0 | 116.0 / 640 / 25.0 |"


def test_sweep_refuses_duplicate_cell(tmp_path):
    for n in ("a.json", "b.json"):
        _run(tmp_path, n, 1, **GPU, pinned_cores="14")
    with pytest.raises(ValueError, match="second file for concurrency 1, 14 threads"):
        bt.sweep([str(tmp_path)])


def test_committed_cpu_table_unchanged():
    root = pathlib.Path(__file__).resolve().parents[1]
    out = bt.table([str(root / "eval/runs/bench/cpu-2026-09-28/financial-lora-c8.json") + "=CPU"])
    assert "| CPU | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | vllm-cpu 0.10.2 | bfloat16 | 14 | 8 | 200 | 22.9 |" in out


def test_recorded_transport_loss_shown_not_refused(tmp_path):
    p = _write(tmp_path, "lossy.json", completed=49, lost_requests=[8])
    assert "| 1 | 49 of 50 |" in bt.table([str(p)]).splitlines()[2]
    q = _write(tmp_path, "short.json", completed=48, lost_requests=[8])
    with pytest.raises(ValueError, match="completed 48 of 50"):
        bt.table([str(q)])
