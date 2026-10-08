"""eval/tickers_extended.txt and argo/eval-run-extended.yaml must not drift."""
import json
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]


def _txt_tickers():
    lines = (REPO / "eval" / "tickers_extended.txt").read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def _yaml_tickers(name="eval-run-extended.yaml"):
    text = (REPO / "argo" / name).read_text(encoding="utf-8")
    m = re.search(r"value:\s*'(\[.*?\])'", text, re.S)
    assert m, f"tickers parameter array not found in {name}"
    return json.loads(m.group(1))


def test_forty_tickers_no_dups_uppercase():
    t = _txt_tickers()
    assert len(t) == 40
    assert len(set(t)) == 40
    assert all(x == x.upper() and re.fullmatch(r"[A-Z.-]{1,6}", x) for x in t)


def test_yaml_matches_txt_exactly():
    assert _yaml_tickers() == _txt_tickers()


def test_local_arm_yaml_matches_txt_exactly():
    assert _yaml_tickers("eval-run-extended-local.yaml") == _txt_tickers()


def test_local_arm_yaml_sets_local_model_arm():
    text = (REPO / "argo" / "eval-run-extended-local.yaml").read_text(encoding="utf-8")
    assert re.search(r"name: arms\s+value: local-model", text)


def _spec_lines(name):
    """The file's YAML without comments (the manifest itself)."""
    text = (REPO / "argo" / name).read_text(encoding="utf-8")
    return [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def test_w4a16_arm_identical_to_local_arm_except_name_prefix():
    local = _spec_lines("eval-run-extended-local.yaml")
    w4 = _spec_lines("eval-run-extended-local-w4a16.yaml")
    diff = [(a, b) for a, b in zip(local, w4) if a != b]
    assert len(local) == len(w4)
    assert diff == [("  generateName: grounding-eval-extended-local-",
                     "  generateName: grounding-eval-extended-local-w4a16-")]


import pytest  # noqa: E402

_SLM_RUNS = [("eval-run-extended-slm-cpu.yaml", "slm-full-cpu", True),
             ("eval-run-extended-slm-gpu.yaml", "slm-full-gpu", True),
             ("eval-run-slm-cpu-smoke.yaml", "slm-full-cpu", False),
             ("eval-run-slm-gpu-smoke.yaml", "slm-full-gpu", False)]


@pytest.mark.parametrize("name,arm,extended", _SLM_RUNS)
def test_slm_run_files(name, arm, extended):
    spec = "\n".join(_spec_lines(name))
    assert re.search(rf"name: arms\s+value: {arm}\n", spec + "\n")
    assert "name: ticker-deadline-seconds" in spec  # CPU tickers outlast the 1200s default
    if extended:
        assert _yaml_tickers(name) == _txt_tickers()
    else:
        assert "name: tickers" not in spec  # smoke = the template's 10 default tickers
    assert "baseline" not in spec  # one arm per run; the baseline is eval-run-extended.yaml


def test_gpu_p4_run_differs_from_the_gpu_run_only_in_name_and_parallelism():
    base = _spec_lines("eval-run-extended-slm-gpu.yaml")
    p4 = _spec_lines("eval-run-extended-slm-gpu-p4.yaml")
    assert [ln for ln in p4 if ln not in base] == ["  generateName: grounding-eval-extended-slm-gpu-p4-",
                                                   "  parallelism: 4"]
    assert [ln for ln in base if ln not in p4] == ["  generateName: grounding-eval-extended-slm-gpu-"]


def test_rerank3_run_differs_from_the_baseline_run_only_in_name_and_arm():
    base = _spec_lines("eval-run-extended.yaml")
    rr = _spec_lines("eval-run-extended-rerank3.yaml")
    assert [ln for ln in rr if ln not in base] == ["  generateName: grounding-eval-extended-rerank3-",
                                                   "      - name: arms", "        value: rerank3"]
    assert [ln for ln in base if ln not in rr] == ["  generateName: grounding-eval-extended-"]
