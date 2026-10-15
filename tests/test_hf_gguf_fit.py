"""scripts/hf_gguf_fit.py: shard grouping and budget margins, offline."""
from scripts.hf_gguf_fit import fit_rows, group_quants, quant_label


FILES = [
    ("UD-Q4_K_M/Model-UD-Q4_K_M-00001-of-00002.gguf", 3 * 2**30),
    ("UD-Q4_K_M/Model-UD-Q4_K_M-00002-of-00002.gguf", 2 * 2**30),
    ("Model-Q8_0.gguf", 9 * 2**30),
    ("mmproj-Model-Q8_0.gguf", 2**29),
    ("mtp-Model-Q4_0.gguf", 2**29),
    ("README.md", 100),
]


def test_shards_sum_and_extras_drop():
    g = group_quants(FILES)
    assert g == {"Model-UD-Q4_K_M": (5 * 2**30, 2), "Model-Q8_0": (9 * 2**30, 1)}


def test_quant_label():
    assert quant_label("Qwen3.6-35B-A3B-Q4_K_M") == "Q4_K_M"
    assert quant_label("MiniMax-M2.7-UD-IQ1_M") == "UD-IQ1_M"
    assert quant_label("MiniMax-M2.5-UD-TQ1_0") == "UD-TQ1_0"
    assert quant_label("MiniMax-M3-BF16") == "BF16"
    assert quant_label("MiniMax-M3-MXFP4_MOE") == "MXFP4_MOE"


def test_fit_rows_margins_and_filter():
    rows = fit_rows(group_quants(FILES), {"gpu": 6.0}, None)
    assert [r[0] for r in rows] == ["UD-Q4_K_M", "Q8_0"]
    assert rows[0][4]["gpu"] == 1.0
    assert rows[1][4]["gpu"] == -3.0
    only = fit_rows(group_quants(FILES), {"gpu": 6.0}, ["Q8_0"])
    assert [r[0] for r in only] == ["Q8_0"]
