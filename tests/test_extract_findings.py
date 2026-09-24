"""scripts/extract_findings.py against a synthetic kubectl-logs capture."""
import base64
import io
import tarfile

from scripts.extract_findings import extract_blocks, unpack


def _tgz(files: dict) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for name, content in files.items():
            data = content.encode("utf-8")
            info = tarfile.TarInfo(name=f"eval_findings/{name}")
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def _log_with(payloads: list[bytes]) -> str:
    lines = ["[pod/x-eval-one-1/main] some harness output",
             "[pod/x-eval-one-1/main]   [AAPL | baseline] 4 SUP  2 UNSUP  0 INF  (6 claims)"]
    for i, p in enumerate(payloads):
        lines += [f"[pod/x-eval-one-{i}/main] ===EVAL_FINDINGS_TGZ_BEGIN pod=x-eval-one-{i}===",
                  f"[pod/x-eval-one-{i}/main] {base64.b64encode(p).decode()}",
                  f"[pod/x-eval-one-{i}/main] ===EVAL_FINDINGS_TGZ_END==="]
    lines.append("[pod/x-agg/main] GATE PASSED")
    return "\n".join(lines)


def test_extract_and_unpack_multiple_blocks(tmp_path):
    log = _log_with([_tgz({"AAPL_baseline.md": "# AAPL findings"}),
                     _tgz({"NVDA_baseline.md": "# NVDA findings"})])
    blocks = extract_blocks(log)
    assert len(blocks) == 2
    total = sum(unpack(b, tmp_path) for b in blocks)
    assert total == 2
    assert (tmp_path / "AAPL_baseline.md").read_text() == "# AAPL findings"
    assert (tmp_path / "NVDA_baseline.md").read_text() == "# NVDA findings"


def test_no_markers_yields_nothing():
    assert extract_blocks("[pod/x/main] plain output\nno markers here") == []


def test_traversal_flattened(tmp_path):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        data = b"evil"
        info = tarfile.TarInfo(name="../../escape.md")
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
    unpack(buf.getvalue(), tmp_path)
    assert (tmp_path / "escape.md").exists()  # flattened inside out_dir
    assert not (tmp_path.parent / "escape.md").exists()
