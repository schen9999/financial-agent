"""scripts/vllm_model_swap.py — the k3s-gpu model swap behind `make vm-vllm`.
Defaults must be the identity (the committed deployment, byte for byte);
overrides touch exactly the three values; drift or bad input exits."""
import importlib.util
import pathlib

import pytest

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "vllm_model_swap.py"
_spec = importlib.util.spec_from_file_location("vllm_model_swap", _MOD_PATH)
swap_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(swap_mod)

# Shape of `kubectl kustomize k8s/vllm/overlays/k3s-gpu` around the three values.
RENDER = """\
        args:
        - /models/financial-lora
        - --served-model-name=financial-lora
        - --dtype=bfloat16
        - --max-model-len=4096
        - --max-num-seqs=8
        volumeMounts:
        - mountPath: /models/financial-lora
          name: model
      volumes:
      - hostPath:
          path: /home/ubuntu/models/qwen-ft
          type: Directory
        name: model
"""


def test_defaults_are_identity():
    out = swap_mod.swap(RENDER, swap_mod.DEFAULT_MODEL_DIR,
                        swap_mod.DEFAULT_SERVED_NAME, swap_mod.DEFAULT_MAX_LEN)
    assert out == RENDER


def test_override_changes_exactly_three_lines():
    out = swap_mod.swap(RENDER, "qwen2.5-7b-instruct", "qwen7b", 8192)
    changed = [(a, b) for a, b in zip(RENDER.splitlines(), out.splitlines()) if a != b]
    assert changed == [
        ("        - --served-model-name=financial-lora", "        - --served-model-name=qwen7b"),
        ("        - --max-model-len=4096", "        - --max-model-len=8192"),
        ("          path: /home/ubuntu/models/qwen-ft",
         "          path: /home/ubuntu/models/qwen2.5-7b-instruct"),
    ]
    # the in-container mount path is an internal name and never changes
    assert "/models/financial-lora\n" in out


@pytest.mark.parametrize("model_dir,name", [
    ("../etc", "x"), ("a/b", "x"), ("", "x"), ("ok", "bad name"), ("ok", "-lead"),
])
def test_rejects_unsafe_names(model_dir, name):
    with pytest.raises(SystemExit):
        swap_mod.swap(RENDER, model_dir, name, 4096)


def test_rejects_nonpositive_max_len():
    with pytest.raises(SystemExit):
        swap_mod.swap(RENDER, "qwen-ft", "financial-lora", 0)


def test_drifted_render_exits_instead_of_half_swapping():
    drifted = RENDER.replace("--max-model-len=4096", "--max-model-len=2048")
    with pytest.raises(SystemExit) as exc:
        swap_mod.swap(drifted, "qwen7b-dir", "qwen7b", 8192)
    assert "overlay drifted" in str(exc.value)
