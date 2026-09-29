"""scripts/quantize_w4a16.py: calibration rows are a fixed-seed draw that never
repeats, the vllm-crashing tokenizer layout is removed, and the saved scheme is
checked. The GPU path (llm-compressor, torch) runs only on the node."""
import importlib.util
import json
import pathlib

import pytest

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "quantize_w4a16.py"
_spec = importlib.util.spec_from_file_location("quantize_w4a16", _MOD_PATH)
qw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(qw)


def test_pick_rows_fixed_seed_and_no_repeats():
    rows = list(range(104))
    a, b = qw.pick_rows(rows, 104, 42), qw.pick_rows(rows, 104, 42)
    assert a == b and sorted(a) == rows
    assert qw.pick_rows(rows, 10, 42) != qw.pick_rows(rows, 10, 7)


def test_pick_rows_refuses_more_than_dataset():
    with pytest.raises(SystemExit, match="dataset has 104 rows"):
        qw.pick_rows(list(range(104)), 256, 42)


def test_strip_list_form_extra_special_tokens(tmp_path):
    p = tmp_path / "tokenizer_config.json"
    p.write_text(json.dumps({"eos_token": "<|im_end|>",
                             "extra_special_tokens": ["<|im_start|>"]}), encoding="utf-8")
    assert qw.strip_extra_special_tokens(p) is True
    assert json.loads(p.read_text(encoding="utf-8")) == {"eos_token": "<|im_end|>"}
    assert qw.strip_extra_special_tokens(p) is False


def test_dict_form_extra_special_tokens_kept(tmp_path):
    p = tmp_path / "tokenizer_config.json"
    cfg = {"extra_special_tokens": {"a": "<a>"}}
    p.write_text(json.dumps(cfg), encoding="utf-8")
    assert qw.strip_extra_special_tokens(p) is False
    assert json.loads(p.read_text(encoding="utf-8")) == cfg


def _config(tmp_path, bits, group):
    q = {"quant_method": "compressed-tensors", "format": "pack-quantized",
         "ignore": ["lm_head"],
         "config_groups": {"group_0": {"targets": ["Linear"],
                                       "weights": {"num_bits": bits, "group_size": group}}}}
    (tmp_path / "config.json").write_text(json.dumps({"quantization_config": q}),
                                          encoding="utf-8")


def test_saved_scheme_accepts_w4_g128(tmp_path):
    _config(tmp_path, 4, 128)
    assert qw.saved_scheme(tmp_path)["format"] == "pack-quantized"


def test_saved_scheme_rejects_other_group_size(tmp_path):
    _config(tmp_path, 4, 64)
    with pytest.raises(SystemExit, match="group size 128"):
        qw.saved_scheme(tmp_path)
