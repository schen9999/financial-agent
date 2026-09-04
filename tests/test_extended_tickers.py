"""eval/tickers_extended.txt and argo/eval-run-extended.yaml must not drift."""
import json
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]


def _txt_tickers():
    lines = (REPO / "eval" / "tickers_extended.txt").read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def _yaml_tickers():
    text = (REPO / "argo" / "eval-run-extended.yaml").read_text(encoding="utf-8")
    m = re.search(r"value:\s*'(\[.*?\])'", text, re.S)
    assert m, "tickers parameter array not found in eval-run-extended.yaml"
    return json.loads(m.group(1))


def test_forty_tickers_no_dups_uppercase():
    t = _txt_tickers()
    assert len(t) == 40
    assert len(set(t)) == 40
    assert all(x == x.upper() and re.fullmatch(r"[A-Z.-]{1,6}", x) for x in t)


def test_yaml_matches_txt_exactly():
    assert _yaml_tickers() == _txt_tickers()
