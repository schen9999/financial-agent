"""scripts/llamacpp_layout.py — the GPU endpoint's MoE layout behind
`make vm-llamacpp NCMOE=n`. 0 is the identity; n > 0 sets --n-cpu-moe AND
renames the served alias to ...-hybrid-ncmoe<n> in the same edit."""
import importlib.util
import pathlib

import pytest

_spec = importlib.util.spec_from_file_location(
    "llamacpp_layout", pathlib.Path(__file__).resolve().parents[1] / "scripts" / "llamacpp_layout.py")
layout = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(layout)

# Shape of `kubectl kustomize k8s/llamacpp/overlays/k3s-gpu` around the args.
RENDER = """\
      - args:
        - --model
        - /models/Qwen3.6-35B-A3B-Q4_K_M.gguf
        - --alias
        - qwen3.6-35b-a3b-q4km
        - --host
        - 0.0.0.0
        - --ctx-size
        - "32768"
        - --n-gpu-layers
        - all
        - --n-cpu-moe
        - "0"
        - --threads
        - "8"
        env:
"""


def test_zero_is_identity():
    assert layout.apply(RENDER, 0) == RENDER


def test_hybrid_sets_ncmoe_and_alias_together():
    out = layout.apply(RENDER, 4)
    assert '- --n-cpu-moe\n        - "4"' in out
    assert "- qwen3.6-35b-a3b-q4km-hybrid-ncmoe4\n" in out
    changed = [(a, b) for a, b in zip(RENDER.splitlines(), out.splitlines()) if a != b]
    assert len(changed) == 2


def test_alias_matches_what_the_eval_expects():
    assert layout.served_alias(0) == "qwen3.6-35b-a3b-q4km"
    assert layout.served_alias(12) == "qwen3.6-35b-a3b-q4km-hybrid-ncmoe12"


def test_drift_and_bad_input_exit():
    with pytest.raises(SystemExit, match="drifted"):
        layout.apply(RENDER.replace("--n-cpu-moe", "--n-cpu-x"), 2)
    with pytest.raises(SystemExit, match="drifted"):
        layout.apply(RENDER + RENDER, 2)
    with pytest.raises(SystemExit, match=">= 0"):
        layout.apply(RENDER, -1)


def test_committed_overlay_carries_the_defaults():
    # The committed k3s-gpu overlay and base must hold the values the
    # script edits (rendering needs kubectl, so check the sources).
    repo = pathlib.Path(__file__).resolve().parents[1]
    gpu = (repo / "k8s/llamacpp/overlays/k3s-gpu/kustomization.yaml").read_text(encoding="utf-8")
    base = (repo / "k8s/llamacpp/base/llamacpp.yaml").read_text(encoding="utf-8")
    assert "value: --n-cpu-moe\n      - op: add\n        path: /spec/template/spec/containers/0/args/-\n        value: \"0\"" in gpu
    assert "- --alias\n            - qwen3.6-35b-a3b-q4km\n" in base


def test_harness_config_matches_the_served_artifact():
    """app-config (oke-provided) restates what k8s/llamacpp pins: the served
    alias and the GGUF identity recorded in every run's provenance."""
    import re
    repo = pathlib.Path(__file__).resolve().parents[1]
    base = (repo / "k8s/llamacpp/base/llamacpp.yaml").read_text(encoding="utf-8")
    cfg = (repo / "k8s/overlays/oke-provided/kustomization.yaml").read_text(encoding="utf-8")
    url = re.search(r"value: (https://huggingface.co/\S+)", base).group(1)
    sha = re.search(r"name: GGUF_SHA256\n\s+value: ([0-9a-f]{64})", base).group(1)
    repo_id, rev, fname = re.match(r"https://huggingface.co/(.+?)/resolve/([0-9a-f]{40})/(.+)$", url).groups()
    artifact = re.search(r'SLM_ARTIFACT: "([^"]+)"', cfg).group(1)
    assert artifact == f"{repo_id}@{rev}:{fname} sha256:{sha}"
    assert f"--model\n            - /models/{fname}\n" in base
    assert re.search(r'SLM_MODEL_NAME: "([^"]+)"', cfg).group(1) == layout.ALIAS
