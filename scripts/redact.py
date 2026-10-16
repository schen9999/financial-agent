#!/usr/bin/env python3
"""Keep IPv4 addresses out of committed files: redact captures at write time,
and check tracked files for any address outside the allowlist.

The repo is public. Real addresses live only in a gitignored address file,
`.addresses.env` at the repo root (or the path in $REDACT_ADDRESSES), one
shell assignment per line, e.g.

  NODE2_PUBLIC_IP=...      ->  <node2-public-ip>
  OKE_EGRESS_IP=...        ->  <oke-egress-ip>
  STREAMLIT_LB_IP=...      ->  <streamlit-lb-ip>   (the 2026-10-08 incident LB, deleted)
  PUBLIC_UI_LB_IP=...      ->  <public-ui-lb-ip>   (the live public-UI LB)
  OKE_API_PRIVATE_IP=...   ->  <oke-api-private-ip>
  OKE_NODE_1=...           ->  <oke-node-1>   (and so on per node)
  OKE_OPERATOR_HOST=...    ->  <oke-operator-host>   (hostnames too)
  OKE_VCN_DOMAIN=...       ->  <oke-vcn-domain>

The placeholder is the variable name in lower case with hyphens. Runbook
commands source the same file, so it is the one place the values are kept
(template: addresses.env.example). Any other address not on the allowlist
becomes <public-ip> or <private-ip>, so an unknown one is never written
out. Hostnames from the file are replaced as whole names (also as the end
of a longer FQDN); --check cannot find an unknown hostname, only an
address. Addresses inside base64 blobs (base64 gzip text, as in Argo's
status.compressedNodes, and base64 tar.gz, as in the eval pods' findings
dumps) are redacted inside and the blob re-encoded; base64 that is not
gzip is not opened.

Allowed: 0.0.0.0, loopback, link-local (169.254.0.0/16, the instance
metadata service), the documentation ranges (192.0.2.0/24, 198.51.100.0/24,
203.0.113.0/24), private network blocks written with a prefix shorter than
/32 (subnet CIDRs in Terraform and nginx config), and version strings
(`==1.1.1.2`, or more than four dotted parts).

  python3 scripts/redact.py < capture.log > capture.redacted.log   # filter
  python3 scripts/redact.py FILE...                                 # in place
  python3 scripts/redact.py --check FILE...                         # list, exit 1 on any
"""
import argparse
import base64
import binascii
import gzip
import io
import ipaddress
import os
import re
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# A plain pattern (lookarounds made the scan ~4x slower over eval/runs); the
# boundaries are checked in _is_candidate: not inside a longer dotted number,
# while an address right after a JSON escape (a "\n" then the address) or a letter is
# still found.
IPV4 = re.compile(r"(\d+\.\d+\.\d+\.\d+)(/\d+)?")
# base64 of gzip data starts "H4sI"; both blob kinds in captures are gzip
B64RUN = re.compile(r"H4sI[A-Za-z0-9+/]{196,}={0,2}")
VERSION_PREFIX = re.compile(r"(?:==|>=|<=|~=|!=|\bv)$")
ALWAYS = [ipaddress.ip_network(n) for n in (
    "0.0.0.0/32", "127.0.0.0/8", "169.254.0.0/16",
    "192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")]
PRIVATE = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
                                              "100.64.0.0/10")]
ASSIGN = re.compile(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=\s*['\"]?([A-Za-z0-9.-]+)['\"]?\s*(?:#.*)?$")
HOSTNAME = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*$")


def placeholder_for(var: str) -> str:
    return "<" + var.lower().replace("_", "-") + ">"


def address_file() -> Path:
    return Path(os.environ.get("REDACT_ADDRESSES") or REPO / ".addresses.env")


def load_map(path: Path | None = None) -> dict[str, str]:
    """{address or hostname: placeholder} from the address file; {} if it is
    absent."""
    path = path or address_file()
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ASSIGN.match(line)
        if m:
            try:
                ipaddress.ip_address(m.group(2))
            except ValueError:
                if not HOSTNAME.match(m.group(2)):
                    continue
            out[m.group(2)] = placeholder_for(m.group(1))
    return out


def _is_candidate(text: str, m: re.Match) -> bool:
    """A dotted quad that could be an address: four octets of 1-3 digits,
    each <= 255, a prefix <= 32, and not part of a longer dotted number."""
    s, e = m.start(), m.end()
    if s and (text[s - 1].isdigit() or text[s - 1] == "."):
        return False
    if e < len(text) and (text[e].isdigit() or (text[e] == "." and e + 1 < len(text)
                                                and text[e + 1].isdigit())):
        return False
    octets = m.group(1).split(".")
    if any(len(o) > 3 or int(o) > 255 for o in octets):
        return False
    return not (m.group(2) and int(m.group(2)[1:]) > 32)


def allowed(addr: str, prefix: str | None, before: str) -> bool:
    """True for an address the allowlist admits (see the module docstring)."""
    if VERSION_PREFIX.search(before):
        return True
    try:
        ip = ipaddress.ip_address(addr)
    except ValueError:
        return True  # not an address (e.g. 999.1.1.1)
    if any(ip in n for n in ALWAYS):
        return True
    if prefix and int(prefix[1:]) < 32 and any(ip in n for n in PRIVATE):
        return True
    if prefix == "/0":
        return True
    return False


def _generic(addr: str) -> str:
    ip = ipaddress.ip_address(addr)
    return "<public-ip>" if ip.is_global else "<private-ip>"


def _sub_hosts(text: str, mapping: dict[str, str]) -> str:
    names = sorted((k for k in mapping if HOSTNAME.match(k)), key=len, reverse=True)
    if not names:
        return text
    pat = re.compile(r"(?<![A-Za-z0-9-])(?:" + "|".join(map(re.escape, names)) + r")(?![A-Za-z0-9-])")
    return pat.sub(lambda m: mapping[m.group(0)], text)


def _sub_text(text: str, mapping: dict[str, str]) -> str:
    text = _sub_hosts(text, mapping)

    def rep(m: re.Match) -> str:
        addr, prefix = m.group(1), m.group(2) or ""
        if not _is_candidate(text, m):
            return m.group(0)
        if addr in mapping:
            return mapping[addr] + prefix
        if allowed(addr, m.group(2), text[max(0, m.start() - 3):m.start()]):
            return m.group(0)
        return _generic(addr) + prefix
    return IPV4.sub(rep, text)


def _decode_blob(s: str):
    """(kind, payload) for a base64 run that holds a gzip tar ("tgz") or gzip
    text ("gz"); None otherwise."""
    try:
        raw = base64.b64decode(s + "=" * (-len(s) % 4), validate=True)
    except (binascii.Error, ValueError):
        return None
    if raw[:2] == b"\x1f\x8b":
        try:
            data = gzip.decompress(raw)
        except (OSError, EOFError):
            return None
        try:
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as tf:
                tf.getmembers()
            return "tgz", data
        except tarfile.TarError:
            pass
        try:
            return "gz", data.decode("utf-8")
        except UnicodeDecodeError:
            return None
    return None


def _redact_tar(data: bytes, mapping: dict[str, str]) -> bytes | None:
    src = tarfile.open(fileobj=io.BytesIO(data), mode="r:")
    out = io.BytesIO()
    changed = False
    with tarfile.open(fileobj=out, mode="w:", format=src.format) as dst:
        for m in src.getmembers():
            body = src.extractfile(m).read() if m.isfile() else None
            if body is not None:
                try:
                    new = _sub_text(body.decode("utf-8"), mapping).encode("utf-8")
                except UnicodeDecodeError:
                    new = body
                if new != body:
                    changed = True
                    body = new
                info = tarfile.TarInfo(m.name)
                for attr in ("mode", "uid", "gid", "uname", "gname", "mtime", "type"):
                    setattr(info, attr, getattr(m, attr))
                info.size = len(body)
                dst.addfile(info, io.BytesIO(body))
            else:
                dst.addfile(m)
    return out.getvalue() if changed else None


def _sub_blobs(text: str, mapping: dict[str, str]) -> str:
    def rep(m: re.Match) -> str:
        dec = _decode_blob(m.group(0))
        if not dec:
            return m.group(0)
        kind, payload = dec
        if kind == "tgz":
            new = _redact_tar(payload, mapping)
            return (base64.b64encode(gzip.compress(new, mtime=0)).decode("ascii")
                    if new is not None else m.group(0))
        new_text = _sub_text(payload, mapping)
        if new_text == payload:
            return m.group(0)
        raw = new_text.encode("utf-8")
        if kind == "gz":
            raw = gzip.compress(raw, mtime=0)
        return base64.b64encode(raw).decode("ascii")
    return B64RUN.sub(rep, text)


def redact(text: str, mapping: dict[str, str] | None = None) -> str:
    """The text with every non-allowlisted address replaced, inside blobs too."""
    mapping = load_map() if mapping is None else mapping
    return _sub_text(_sub_blobs(text, mapping), mapping)


def find(text: str) -> list[tuple[int, str]]:
    """(line, address) for every non-allowlisted address, blobs included."""
    hits = []
    line_of = lambda pos: text.count("\n", 0, pos) + 1  # noqa: E731 (only on a hit)
    for m in IPV4.finditer(text):
        if _is_candidate(text, m) and not allowed(m.group(1), m.group(2), text[max(0, m.start() - 3):m.start()]):
            hits.append((line_of(m.start()), m.group(0)))
    for b in B64RUN.finditer(text):
        dec = _decode_blob(b.group(0))
        if not dec:
            continue
        kind, payload = dec
        if kind == "tgz":
            with tarfile.open(fileobj=io.BytesIO(payload), mode="r:") as tf:
                texts = [tf.extractfile(x).read().decode("utf-8", "replace")
                         for x in tf.getmembers() if x.isfile()]
        else:
            texts = [payload]
        n = line_of(b.start())
        for t in texts:
            hits += [(n, f"{a} (inside an encoded blob)") for _, a in find(t)]
    return sorted(hits)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--check", action="store_true", help="report addresses, change nothing")
    args = ap.parse_args(argv)
    if not args.files:
        if args.check:
            hits = find(sys.stdin.read())
            for n, a in hits:
                print(f"<stdin>:{n}: {a}")
            return 1 if hits else 0
        sys.stdout.write(redact(sys.stdin.read()))
        return 0
    mapping = None if args.check else load_map()
    bad = 0
    for f in args.files:
        try:
            with open(f, encoding="utf-8", newline="") as fh:  # keep line endings as they are
                text = fh.read()
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
            continue
        if args.check:
            for n, a in find(text):
                print(f"{f}:{n}: {a}")
                bad += 1
        else:
            new = redact(text, mapping)
            if new != text:
                f.write_text(new, encoding="utf-8", newline="")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
