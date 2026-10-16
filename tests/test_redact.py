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
    f.write_text(f"# comment\nNODE2_PUBLIC_IP={PUB}\nexport OKE_NODE_2='{NODE}'  # n2\nNOT_AN_IP=abc\n")
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
