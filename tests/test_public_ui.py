"""The public Streamlit UI overlay: the allowlist renderer refuses anything
wide or malformed, the OCI rule and nginx come from the same list, and the
committed files carry no allowlist entry or OCID."""
import json
import subprocess

import pytest

from scripts import public_ui_render as pr

OV = pr.OVERLAY


def test_allowlist_parsing_and_refusals():
    assert pr.read_allowlist("# home\n99.164.75.62/32\n\n198.51.100.0/24  # office\n") == \
        ["99.164.75.62/32", "198.51.100.0/24"]
    for bad, msg in (("", "empty"), ("# only a comment\n", "empty"), ("0.0.0.0/0", "wider"),
                     ("10.0.0.0/16", "wider"), ("99.164.75.62", None), ("not-an-ip", "not an IPv4"),
                     ("99.164.75.1/24", "not an IPv4")):
        if msg is None:
            assert pr.read_allowlist(bad) == ["99.164.75.62/32"]   # a bare address is a /32
            continue
        with pytest.raises(SystemExit, match=msg):
            pr.read_allowlist(bad)


def test_one_list_feeds_nginx_and_the_load_balancer():
    cidrs = ["192.0.2.7/32", "198.51.100.0/24"]
    assert pr.allow_conf(cidrs) == "allow 192.0.2.7/32;\nallow 198.51.100.0/24;\ndeny all;\n"
    ops = {o["path"]: o["value"] for o in pr.service_patch(cidrs, "ocid1.subnet.x", backend_nsg="ocid1.nsg.y")}
    assert ops["/spec/loadBalancerSourceRanges"] == cidrs and ops["/spec/type"] == "LoadBalancer"
    assert ops["/spec/ports"] == [{"name": "https", "port": 443, "targetPort": "proxy", "protocol": "TCP",
                                   "nodePort": 30443}]
    assert 30000 <= pr.NODE_PORT <= 32767
    ann = ops["/metadata/annotations"]
    assert ann["oci.oraclecloud.com/security-rule-management-mode"] == "NSG"
    assert ann["service.beta.kubernetes.io/oci-load-balancer-shape-flex-max"] == "10"
    assert ann["service.beta.kubernetes.io/oci-load-balancer-tls-secret"] == "streamlit-tls"
    assert ann["service.beta.kubernetes.io/oci-load-balancer-subnet1"] == "ocid1.subnet.x"


def test_renders_into_the_gitignored_dir(tmp_path):
    (tmp_path / "allow.txt").write_text("192.0.2.7/32\n")
    pr.main(["--allowlist", str(tmp_path / "allow.txt"), "--out", str(tmp_path / "g"),
             "--lb-subnet", "ocid1.subnet.x", "--backend-nsg", "ocid1.nsg.y"])
    assert (tmp_path / "g" / "allow.conf").read_text() == "allow 192.0.2.7/32;\ndeny all;\n"
    assert json.loads((tmp_path / "g" / "service-patch.yaml").read_text())[3]["value"] == ["192.0.2.7/32"]
    with pytest.raises(SystemExit, match="not an OCID"):
        pr.main(["--allowlist", str(tmp_path / "allow.txt"), "--out", str(tmp_path / "g"),
                 "--lb-subnet", "subnet", "--backend-nsg", "ocid1.nsg.y"])


def test_nginx_checks_the_allowlist_before_auth_and_proxies_websockets():
    conf = (OV / "nginx.conf").read_text(encoding="utf-8")
    loc = conf[conf.index("location / {"):]
    assert loc.index("include /etc/nginx/allow/allow.conf;") < loc.index("auth_basic ")
    assert "proxy_pass http://127.0.0.1:8501;" in loc and "proxy_set_header Upgrade" in loc


def test_nothing_identifying_is_committed():
    files = subprocess.run(["git", "ls-files", str(OV)], capture_output=True, text=True,
                           cwd=pr.ROOT).stdout.splitlines()
    assert not any("allowlist.txt" in f or "/generated/" in f for f in files)
    for name in ("kustomization.yaml", "nginx.conf"):
        text = (OV / name).read_text(encoding="utf-8")
        assert "ocid1." not in text and "99.164" not in text
    ignored = subprocess.run(["git", "check-ignore", str(OV / "allowlist.txt"), str(OV / "generated" / "x")],
                             capture_output=True, text=True, cwd=pr.ROOT).stdout.splitlines()
    assert len(ignored) == 2


def test_fallback_joins_an_existing_nsg_with_rule_management_off():
    ops = {o["path"]: o["value"] for o in pr.service_patch(["192.0.2.7/32"], "ocid1.subnet.x",
                                                             attach_nsg="ocid1.nsg.lb")}
    ann = ops["/metadata/annotations"]
    assert ann["oci.oraclecloud.com/security-rule-management-mode"] == "None"
    assert ann["oci.oraclecloud.com/oci-network-security-groups"] == "ocid1.nsg.lb"
    assert "oci.oraclecloud.com/oci-backend-network-security-group" not in ann
    for kw in ({}, {"backend_nsg": "ocid1.a", "attach_nsg": "ocid1.b"}):
        with pytest.raises(SystemExit, match="exactly one"):
            pr.service_patch(["192.0.2.7/32"], "ocid1.subnet.x", **kw)


def test_up_script_refuses_an_open_nsg_in_fallback():
    src = (pr.ROOT / "scripts" / "public_ui_up.sh").read_text(encoding="utf-8")
    assert "source=='0.0.0.0/0'" in src and "refusing:" in src
