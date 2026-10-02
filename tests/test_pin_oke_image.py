"""scripts/pin_oke_image.py — the oke-provided overlays pin one GHCR build,
by full git sha, in both the app and the Argo overlay."""
import importlib.util
import pathlib
import shutil

import pytest

_REPO = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "pin_oke_image", _REPO / "scripts" / "pin_oke_image.py")
pin_oke_image = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pin_oke_image)

SHA = "0123456789abcdef0123456789abcdef01234567"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A scratch repo holding copies of the committed oke-provided overlays."""
    for tree in ("k8s", "argo"):
        src = _REPO / tree / "overlays" / "oke-provided"
        shutil.copytree(src, tmp_path / tree / "overlays" / "oke-provided")
    monkeypatch.setattr(pin_oke_image, "REPO", str(tmp_path))
    return tmp_path


def _text(repo, tree):
    return (repo / tree / "overlays" / "oke-provided" / "kustomization.yaml").read_text(encoding="utf-8")


def test_committed_overlays_agree():
    # Holds before and after a pin commit: one entry each, same tag.
    tags = pin_oke_image.read_tags("oke-provided")
    assert len(tags) == 2
    assert len(set(tags.values())) == 1


def test_pin_then_check(repo):
    before = {t: _text(repo, t) for t in ("k8s", "argo")}
    pin_oke_image.pin("oke-provided", SHA)
    assert pin_oke_image.check("oke-provided") == SHA
    for t in ("k8s", "argo"):
        after = _text(repo, t)
        changed = [(a, b) for a, b in zip(before[t].splitlines(), after.splitlines()) if a != b]
        assert len(changed) == 1, changed  # only the newTag line moved
        assert changed[0][1].strip() == "newTag: " + SHA


def test_check_rejects_placeholder(repo):
    pin_oke_image.pin("oke-provided", SHA)
    for t in ("k8s", "argo"):
        p = repo / t / "overlays" / "oke-provided" / "kustomization.yaml"
        p.write_text(p.read_text(encoding="utf-8").replace(SHA, "UNPINNED"), encoding="utf-8")
    with pytest.raises(SystemExit, match="UNPINNED"):
        pin_oke_image.check("oke-provided")


def test_check_rejects_mismatch(repo):
    pin_oke_image.pin("oke-provided", SHA)
    p = repo / "argo" / "overlays" / "oke-provided" / "kustomization.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(SHA, "f" * 40), encoding="utf-8")
    with pytest.raises(SystemExit, match="different tags"):
        pin_oke_image.check("oke-provided")


@pytest.mark.parametrize("tag", ["latest", "0123abc", SHA.upper()])
def test_rejects_non_sha_tags(repo, tag):
    before = _text(repo, "k8s")
    with pytest.raises(SystemExit, match="40-hex"):
        pin_oke_image.pin("oke-provided", tag)
    assert _text(repo, "k8s") == before


def test_check_rejects_latest(repo):
    for t in ("k8s", "argo"):
        p = repo / t / "overlays" / "oke-provided" / "kustomization.yaml"
        text = p.read_text(encoding="utf-8")
        tag = pin_oke_image.read_tags("oke-provided")[str(p)]
        p.write_text(text.replace("newTag: " + tag, "newTag: latest"), encoding="utf-8")
    with pytest.raises(SystemExit, match="40-hex"):
        pin_oke_image.check("oke-provided")


def test_drifted_overlay_writes_nothing(repo):
    k8s = repo / "k8s" / "overlays" / "oke-provided" / "kustomization.yaml"
    argo_before = _text(repo, "argo")
    k8s.write_text(_text(repo, "k8s").replace("- name: financial-agent-app", "- name: other"),
                   encoding="utf-8")
    with pytest.raises(SystemExit, match="drifted"):
        pin_oke_image.pin("oke-provided", SHA)
    assert _text(repo, "argo") == argo_before


def test_crlf_overlay_still_pins(repo):
    for t in ("k8s", "argo"):
        p = repo / t / "overlays" / "oke-provided" / "kustomization.yaml"
        p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    pin_oke_image.pin("oke-provided", SHA)
    assert pin_oke_image.check("oke-provided") == SHA
