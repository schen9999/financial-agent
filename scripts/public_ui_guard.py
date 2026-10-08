#!/usr/bin/env python3
"""Guards for the public Streamlit UI in security-list mode (scripts/public_ui_up.sh).

  sl   (before and after the apply) the LB subnet's security list, as
       `oci network security-list get` JSON on stdin: every ingress rule that
       admits the LB port (443) — a TCP rule whose port range covers it, a
       TCP rule with no port range, or an all-protocols rule — must come from
       exactly one of the allowlist's CIDRs. A wider source (0.0.0.0/0, any
       CIDR not on the list) is a violation. After the apply, --require also
       demands a rule for every allowlist CIDR (the controller added them).
  lb   (after the apply) the load balancer, as `oci lb load-balancer get` JSON
       on stdin: no NSG attached, and its only listener is 443 with TLS.

Exit 0 when clean, 1 with every violation printed.
  oci network security-list get --security-list-id <id> | python3 scripts/public_ui_guard.py sl --port 443
  oci lb load-balancer get --load-balancer-id <id> | python3 scripts/public_ui_guard.py lb --port 443
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from public_ui_render import OVERLAY, read_allowlist  # noqa: E402

TCP = "6"


def admits_port(rule: dict, port: int) -> bool:
    proto = str(rule.get("protocol"))
    if proto == "all":
        return True
    if proto != TCP:
        return False
    rng = (rule.get("tcp-options") or {}).get("destination-port-range")
    return rng is None or rng["min"] <= port <= rng["max"]


def sl_violations(sl: dict, allow: list[str], port: int, require: bool = False) -> list[str]:
    data = sl.get("data", sl)
    rules = [r for r in data.get("ingress-security-rules", []) if admits_port(r, port)]
    out = [f"ingress from {r.get('source')} admits port {port} and is not on the allowlist"
           for r in rules if r.get("source") not in allow]
    if require:
        have = {r.get("source") for r in rules}
        out += [f"no ingress rule for allowlist entry {c} on port {port}" for c in allow if c not in have]
    return out


def lb_violations(lb: dict, port: int) -> list[str]:
    data = lb.get("data", lb)
    out = []
    if data.get("network-security-group-ids"):
        out.append(f"load balancer is attached to {len(data['network-security-group-ids'])} NSG(s)")
    for name, ls in (data.get("listeners") or {}).items():
        if ls.get("port") != port:
            out.append(f"listener {name} on port {ls.get('port')}")
        elif not ls.get("ssl-configuration"):
            out.append(f"listener {name} on {port} without TLS")
    if not data.get("listeners"):
        out.append("no listener")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("what", choices=["sl", "lb"])
    ap.add_argument("--port", type=int, default=443)
    ap.add_argument("--allowlist", type=Path, default=OVERLAY / "allowlist.txt")
    ap.add_argument("--require", action="store_true", help="sl: every allowlist entry must have its rule")
    args = ap.parse_args(argv)
    doc = json.load(sys.stdin)
    if args.what == "sl":
        v = sl_violations(doc, read_allowlist(args.allowlist.read_text(encoding="utf-8")), args.port, args.require)
    else:
        v = lb_violations(doc, args.port)
    for line in v:
        print(f"GUARD: {line}")
    print(f"GUARD {args.what}: {'FAIL' if v else 'ok'}")
    return 1 if v else 0


if __name__ == "__main__":
    sys.exit(main())
