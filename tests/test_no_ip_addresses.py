"""No IPv4 address in any tracked file outside the allowlist (CLAUDE.md
honesty rules, 2026-10-16; the repo is public). The allowlist is
scripts/redact.py's (loopback, 0.0.0.0, link-local, documentation ranges,
private subnet CIDRs, version strings) plus any per-file exceptions below
(none today). Addresses inside base64 gzip blobs count.
Fix a failure with `python3 scripts/redact.py <file>` (placeholders from
the gitignored .addresses.env), never by adding a real address here."""
import subprocess
from pathlib import Path

import pytest

from scripts.redact import find

REPO = Path(__file__).resolve().parents[1]

# file -> addresses allowed in it, and why (none today: fixtures build theirs
# at run time, so `scripts/redact.py --check` in CI needs no exceptions)
PER_FILE: dict[str, set[str]] = {}


def _tracked() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True,
                             check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    return [p for p in out.decode().split("\0") if p]


def test_no_ip_addresses_in_tracked_files():
    bad = []
    for rel in _tracked():
        try:
            text = (REPO / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        for line, addr in find(text):
            if addr.split(" ")[0] not in PER_FILE.get(rel, ()):
                bad.append(f"{rel}:{line}: {addr}")
    assert not bad, "IP addresses in tracked files (scripts/redact.py):\n" + "\n".join(bad[:50])
