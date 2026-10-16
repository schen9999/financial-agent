"""scripts/kv_state_fit.py on config fragments of the models in the fit table."""
import pytest

from scripts.kv_state_fit import (GIB, kv_bytes_per_token, layer_counts,
                                  recurrent_bytes_per_seq, served_bytes, verdict)

# Qwen3.6-35B-A3B text_config fields (config.json @995ad96): 40 layers, every
# fourth full attention.
QWEN36_A3B = {"text_config": {
    "num_hidden_layers": 40, "num_attention_heads": 16, "num_key_value_heads": 2,
    "head_dim": 256, "hidden_size": 2048,
    "layer_types": (["linear_attention"] * 3 + ["full_attention"]) * 10,
    "linear_num_value_heads": 32, "linear_num_key_heads": 16,
    "linear_key_head_dim": 128, "linear_value_head_dim": 128, "linear_conv_kernel_dim": 4}}

MINIMAX_M2 = {"num_hidden_layers": 62, "num_attention_heads": 48, "num_key_value_heads": 8,
              "head_dim": 128, "hidden_size": 3072, "attn_type_list": [1] * 62}


def test_qwen36_a3b_kv_matches_the_recorded_20_kib_per_token():
    assert layer_counts(QWEN36_A3B) == (10, 30)
    # eval-methodology 2026-10-02: 10 full-attention layers x 2 KV heads x 256
    assert kv_bytes_per_token(QWEN36_A3B) == 20 * 1024


def test_qwen36_a3b_recurrent_state_per_sequence():
    per_layer = 32 * 128 * 128 * 4 + 3 * (2 * 16 * 128 + 32 * 128) * 4
    assert recurrent_bytes_per_seq(QWEN36_A3B) == 30 * per_layer


def test_minimax_full_attention_only():
    assert layer_counts(MINIMAX_M2) == (62, 0)
    assert kv_bytes_per_token(MINIMAX_M2) == 2 * 62 * 8 * 128 * 2
    assert recurrent_bytes_per_seq(MINIMAX_M2) == 0
    with pytest.raises(ValueError):
        layer_counts({**MINIMAX_M2, "attn_type_list": [0] + [1] * 61})


def test_verdicts():
    s = served_bytes(QWEN36_A3B, 19 * GIB, 8, 5120, 1.0)
    assert s["kv"] == 20 * 1024 * 8 * 5120
    assert verdict(19 * GIB, s["total"], 22.49) == "fits as served"
    assert verdict(19 * GIB, s["total"], 20.0) == "weights only"
    assert verdict(19 * GIB, s["total"], 18.0) == "no"
