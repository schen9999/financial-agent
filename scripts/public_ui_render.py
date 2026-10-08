#!/usr/bin/env python3
"""Render the public Streamlit UI's gitignored files from the allowlist.

Reads k8s/overlays/oke-provided-public-ui/allowlist.txt (one IPv4 CIDR per
line, '#' comments; gitignored) and writes, into that overlay's generated/
(gitignored):

  allow.conf           nginx: one `allow <cidr>;` per entry, then `deny all;`
  service-patch.yaml   JSON 6902 patch turning Service streamlit into the
                       OCI load balancer: type LoadBalancer on 443 -> nginx,
                       loadBalancerSourceRanges = the allowlist, and the
                       annotations (flexible 10 Mbps, TLS from Secret
                       streamlit-tls, HTTP backends, NSG rule management with
                       the workers' NSG as the backend group, the LB subnet)

The subnet and NSG OCIDs are arguments, looked up on the operator
(scripts/public_ui_up.sh), so no OCID is committed. Both files come from the
one allowlist, so the OCI rule and nginx cannot drift apart.

Refuses an empty allowlist, anything that is not an IPv4 CIDR, and any
entry wider than /24 (0.0.0.0/0 above all).

  python3 scripts/public_ui_render.py --lb-subnet <ocid> --backend-nsg <ocid>
"""
import argparse
import ipaddress
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "k8s" / "overlays" / "oke-provided-public-ui"
MAX_PREFIX = 24
# Pinned inside 30000-32767, the range workers-tbhcuw admits from the LB
# subnets: left to the API server, the dry run drew 32769, outside it.
NODE_PORT = 30443


def read_allowlist(text: str) -> list[str]:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        entry = line.split("#", 1)[0].strip()
        if not entry:
            continue
        try:
            net = ipaddress.IPv4Network(entry, strict=True)
        except ValueError as e:
            raise SystemExit(f"allowlist line {n}: {entry!r} is not an IPv4 CIDR ({e})")
        if net.prefixlen < MAX_PREFIX:
            raise SystemExit(f"allowlist line {n}: {entry} is wider than /{MAX_PREFIX}; refusing")
        out.append(str(net))
    if not out:
        raise SystemExit("allowlist is empty: refusing to render (the LB would admit nobody or everybody)")
    return out


def allow_conf(cidrs: list[str]) -> str:
    return "".join(f"allow {c};\n" for c in cidrs) + "deny all;\n"


def service_patch(cidrs: list[str], lb_subnet: str, backend_nsg: str | None = None,
                  attach_nsg: str | None = None, security_list: bool = False) -> list[dict]:
    """Three ways to restrict the LB's source addresses at the OCI layer:

    security_list (the mode in use since 2026-10-08): security-list
        management mode All, no NSG. The controller adds an ingress rule to
        the LB subnet's security list for each loadBalancerSourceRanges entry
        on 443, plus the LB-to-node-port and health-check rules on the
        subnets' security lists (the workers' NSG admits only members of
        pub_lb-tbhcuw, which this LB is not). The controller may manage
        security lists; it may not create NSGs.
    backend_nsg (NSG mode): the controller creates a front-end NSG from
        loadBalancerSourceRanges — refused in this tenancy (404 on
        CreateNetworkSecurityGroup, 2026-10-07 and -08).
    attach_nsg: rule management None (loadBalancerSourceRanges ignored) and
        the LB joins an existing NSG the tenancy owner keeps to the allowlist.
    """
    if sum(bool(x) for x in (backend_nsg, attach_nsg, security_list)) != 1:
        raise SystemExit("give exactly one of --security-list, --backend-nsg (NSG mode) or --attach-nsg")
    ann = {
        "oci.oraclecloud.com/load-balancer-type": "lb",
        "service.beta.kubernetes.io/oci-load-balancer-shape": "flexible",
        "service.beta.kubernetes.io/oci-load-balancer-shape-flex-min": "10",
        "service.beta.kubernetes.io/oci-load-balancer-shape-flex-max": "10",
        "service.beta.kubernetes.io/oci-load-balancer-subnet1": lb_subnet,
        "service.beta.kubernetes.io/oci-load-balancer-ssl-ports": "443",
        "service.beta.kubernetes.io/oci-load-balancer-tls-secret": "streamlit-tls",
        "service.beta.kubernetes.io/oci-load-balancer-backend-protocol": "HTTP",
        "service.beta.kubernetes.io/oci-load-balancer-connection-idle-timeout": "300",
    }
    if security_list:
        ann["service.beta.kubernetes.io/oci-load-balancer-security-list-management-mode"] = "All"
    elif backend_nsg:
        ann["oci.oraclecloud.com/security-rule-management-mode"] = "NSG"
        ann["oci.oraclecloud.com/oci-backend-network-security-group"] = backend_nsg
    else:
        ann["oci.oraclecloud.com/security-rule-management-mode"] = "None"
        ann["oci.oraclecloud.com/oci-network-security-groups"] = attach_nsg
    return [
        {"op": "add", "path": "/metadata/annotations", "value": ann},
        {"op": "replace", "path": "/spec/ports",
         "value": [{"name": "https", "port": 443, "targetPort": "proxy", "protocol": "TCP",
                    "nodePort": NODE_PORT}]},
        {"op": "add", "path": "/spec/type", "value": "LoadBalancer"},
        {"op": "add", "path": "/spec/loadBalancerSourceRanges", "value": cidrs},
    ]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--allowlist", type=Path, default=OVERLAY / "allowlist.txt")
    ap.add_argument("--out", type=Path, default=OVERLAY / "generated")
    ap.add_argument("--lb-subnet", required=True)
    ap.add_argument("--backend-nsg", help="NSG mode: the workers' NSG")
    ap.add_argument("--attach-nsg", help="fallback: the existing LB NSG to join")
    ap.add_argument("--security-list", action="store_true",
                    help="security-list management mode All, no NSG (the mode in use)")
    args = ap.parse_args(argv)
    for name, v in (("--lb-subnet", args.lb_subnet), ("--backend-nsg", args.backend_nsg),
                    ("--attach-nsg", args.attach_nsg)):
        if v is not None and not v.startswith("ocid1."):
            raise SystemExit(f"{name} is not an OCID")
    cidrs = read_allowlist(args.allowlist.read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "allow.conf").write_text(allow_conf(cidrs), encoding="utf-8", newline="\n")
    (args.out / "service-patch.yaml").write_text(
        json.dumps(service_patch(cidrs, args.lb_subnet, args.backend_nsg, args.attach_nsg, args.security_list), indent=2) + "\n",
        encoding="utf-8", newline="\n")
    print(f"rendered {len(cidrs)} allowlist entr{'y' if len(cidrs) == 1 else 'ies'} into {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
