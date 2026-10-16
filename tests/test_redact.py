"""scripts/redact.py: placeholders from the address file, the allowlist, and
redaction inside base64 gzip text and base64 tar.gz blobs. Real-looking
public addresses are assembled at run time so this file holds none."""
import base64
import gzip
import hashlib
import io
import tarfile

from scripts import redact as rd

PUB = ".".join(["8", "8", "8", "8"])        # a global address, built, not written
NODE = ".".join(["10", "140", "46", "187"])  # a private host address
PRIV = ".".join(["10", "9", "8", "7"])     # an unmapped private host address
MAP = {PUB: "<node2-public-ip>", NODE: "<oke-node-2>"}


def test_load_map_from_the_address_file(tmp_path):
    f = tmp_path / ".addresses.env"
    f.write_text(f"# comment\nNODE2_PUBLIC_IP={PUB}\nexport OKE_NODE_2='{NODE}'  # n2\nNOT_A_NAME=has spaces\n")
    assert rd.load_map(f) == MAP
    assert rd.load_map(tmp_path / "missing") == {}


def test_mapped_generic_and_allowed():
    other = ".".join(["1", "1", "1", "1"])
    text = (f"url http://{PUB}:30880 node {NODE} from {PUB}/32 x {other} y " + PRIV + " "
            "cidr 10.140.0.0/16 any 0.0.0.0/0 lo 127.0.0.1 md 169.254.169.254 "
            "doc 203.0.113.5 ver click-plugins==1.1.1.2 long 1.2.3.4.5 json \\n" + NODE)
    out = rd.redact(text, MAP)
    assert "http://<node2-public-ip>:30880" in out and "<node2-public-ip>/32" in out
    assert out.count("<oke-node-2>") == 2
    assert "x <public-ip> y <private-ip>" in out
    for kept in ("10.140.0.0/16", "0.0.0.0/0", "127.0.0.1", "169.254.169.254",
                 "203.0.113.5", "==1.1.1.2", "1.2.3.4.5"):
        assert kept in out
    assert rd.find(out) == []
    assert {a for _, a in rd.find(text)} == {PUB, NODE, f"{PUB}/32", other, PRIV}


def _b64gz(data: bytes) -> str:
    return base64.b64encode(gzip.compress(data, mtime=0)).decode()


def test_inside_gzip_text_blob():
    pad = "".join(hashlib.sha256(str(i).encode()).hexdigest() for i in range(8))  # incompressible
    blob = _b64gz(('{"hostNodeName": "%s", "pad": "%s"}' % (NODE, pad)).encode())
    line = f'"compressedNodes": "{blob}"'
    assert rd.find(line) == [(1, f"{NODE} (inside an encoded blob)")]
    out = rd.redact(line, MAP)
    assert rd.find(out) == []
    new_blob = out.split('"')[3]
    assert b"<oke-node-2>" in gzip.decompress(base64.b64decode(new_blob))


def test_inside_tar_gz_blob_members_survive():
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:") as tf:
        for name, body in (("eval_findings/AAPL.md", f"slm_url: http://{PUB}:30880\n" + "y" * 300),
                           ("eval_findings/notes.txt", "no address here")):
            data = body.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    line = "[pod/x/main] " + _b64gz(buf.getvalue())
    out = rd.redact(line, MAP)
    assert rd.find(out) == []
    raw = gzip.decompress(base64.b64decode(out.split("] ", 1)[1]))
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as tf:
        got = {m.name: tf.extractfile(m).read().decode() for m in tf.getmembers()}
    assert got["eval_findings/AAPL.md"].startswith("slm_url: http://<node2-public-ip>:30880")
    assert got["eval_findings/notes.txt"] == "no address here"


def test_cli_filter_and_in_place(tmp_path, monkeypatch, capsys):
    addr = tmp_path / ".addresses.env"
    addr.write_text(f"NODE2_PUBLIC_IP={PUB}\n")
    monkeypatch.setenv("REDACT_ADDRESSES", str(addr))
    f = tmp_path / "capture.log"
    f.write_bytes(f"a {PUB}\r\nb\r\n".encode())
    assert rd.main([str(f)]) == 0
    assert f.read_bytes() == b"a <node2-public-ip>\r\nb\r\n"  # line endings kept
    assert rd.main(["--check", str(f)]) == 0
    f.write_text(f"c {PUB}\n")
    assert rd.main(["--check", str(f)]) == 1
    assert PUB in capsys.readouterr().out


def test_hostnames_from_the_address_file(tmp_path):
    f = tmp_path / ".addresses.env"
    f.write_text("OKE_OPERATOR_HOST=o-abcdef\nOKE_VCN_DOMAIN=abcdef.oraclevcn.com\nBAD=not a host\n")
    m = rd.load_map(f)
    assert m == {"o-abcdef": "<oke-operator-host>", "abcdef.oraclevcn.com": "<oke-vcn-domain>"}
    out = rd.redact("ubuntu@o-abcdef:~$ x; node-1.sub.abcdef.oraclevcn.com; no-abcdef; o-abcdefg", m)
    assert out == "ubuntu@<oke-operator-host>:~$ x; node-1.sub.<oke-vcn-domain>; no-abcdef; o-abcdefg"


EXAMPLE = rd.REPO / "addresses.env.example"
LIVE_LB = ".".join(["9", "9", "9", "9"])     # stands in for the live public-UI LB
INCIDENT_LB = ".".join(["1", "0", "0", "1"])  # stands in for the 2026-10-08 incident LB


def test_example_defines_both_load_balancers_apart():
    """STREAMLIT_LB_IP is the deleted 2026-10-08 incident LB; PUBLIC_UI_LB_IP
    is the live one public_ui_up.sh created. Two variables, two placeholders."""
    m = rd.load_map(EXAMPLE)
    assert m["203.0.113.30"] == "<streamlit-lb-ip>"
    assert m["203.0.113.40"] == "<public-ui-lb-ip>"


def test_live_lb_redacts_to_its_own_placeholder(tmp_path):
    line = f"external IP: {LIVE_LB}\npublic UI up at https://{LIVE_LB}/ (guards passed)\nincident {INCIDENT_LB}:8501"
    f = tmp_path / ".addresses.env"
    f.write_text(f"STREAMLIT_LB_IP={INCIDENT_LB}\nPUBLIC_UI_LB_IP={LIVE_LB}\n")
    assert rd.redact(line, rd.load_map(f)) == (
        "external IP: <public-ui-lb-ip>\npublic UI up at https://<public-ui-lb-ip>/ (guards passed)\n"
        "incident <streamlit-lb-ip>:8501")
    # without PUBLIC_UI_LB_IP (the state before 2026-10-16) it was only generic
    f.write_text(f"STREAMLIT_LB_IP={INCIDENT_LB}\n")
    assert "https://<public-ip>/" in rd.redact(line, rd.load_map(f))


def test_every_address_placeholder_in_the_repo_is_defined():
    """Each <...-ip> / <oke-node-N> placeholder in a tracked file comes from a
    variable in addresses.env.example, is redact.py's generic one, or is a
    hand-written stand-in for "whichever host" — so a misspelt or invented
    placeholder (as public-ui-ip and node-2-public-ip were) fails here."""
    import re
    import subprocess
    import pytest
    try:
        files = subprocess.run(["git", "ls-files", "-z"], cwd=rd.REPO, capture_output=True,
                               check=True).stdout.decode().split("\0")
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git not available")
    defined = set(rd.load_map(EXAMPLE).values()) | {"<public-ip>", "<private-ip>"}
    hand_written = {"<vm-ip>", "<node-ip>", "<allowlisted-ip>"}
    pat = re.compile(rb"<(?:[a-z0-9-]+-ip|oke-node-\d+)>")
    bad = {}
    for name in filter(None, files):
        try:
            data = (rd.REPO / name).read_bytes()
        except OSError:
            continue
        for p in set(pat.findall(data)):
            if p.decode() not in defined | hand_written:
                bad.setdefault(p.decode(), []).append(name)
    assert not bad, bad
