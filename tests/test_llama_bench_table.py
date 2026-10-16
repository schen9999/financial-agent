"""scripts/llama_bench_table.py against the committed 2026-10-08 E5 sweep."""
from scripts.llama_bench_table import markdown, rows

D = "eval/runs/llama-bench-cpu-2026-10-08/"


def test_reproduces_the_documented_e5_sweep():
    tests, out = rows([(D + "P4.json", "4"), (D + "P8.json", "8"), (D + "P15.json", "15")], 10.0)
    assert tests == ["pp512", "pp2048", "tg128"]
    cells = {o[0]: o[6] for o in out}
    assert cells["4"]["pp2048"].startswith("61.1 ")
    assert cells["8"]["pp2048"].startswith("109.8 ")
    assert cells["15"]["pp2048"].startswith("103.6 ")
    assert [cells[k]["tg128"][:4] for k in ("4", "8", "15")] == ["12.9", "13.3", "12.8"]
    # the cold first repetition of pp512 is flagged, the steady tests are not
    assert cells["8"]["pp512"].endswith("†")
    assert not cells["8"]["pp2048"].endswith("†")
    assert out[0][1] == "AMD EPYC 9J14 96-Core Processor"
    assert out[0][2] == "CPU" and out[0][3] == 4


def test_markdown_shape():
    text = markdown(*rows([(D + "P8.json", "E5")], 10.0))
    assert text.splitlines()[0].startswith("| Where | Device | Backend | Threads | GPU layers | pp512")
    assert "b11347" in text
