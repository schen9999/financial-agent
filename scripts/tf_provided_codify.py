#!/usr/bin/env python3
"""Turn terraform/oci-provided/generated-config.tf (gitignored: it holds
OCIDs) into committable, reviewable configuration for the PROVIDED cluster,
codified via terraform import. Plan only, never apply (CLAUDE.md, the
2026-10-07 exception). Operator only, after tf_provided_fixup.py; no cloud
call, no Terraform call.

What it does, and nothing else:
  - an OCID that is the import id of a codified resource becomes a reference
    (`oci_core_subnet.subnet_workers.id`);
  - every other OCID (compartment, node images, the Oracle services
    network), availability-domain names (tenancy-prefixed), ssh public keys
    and public CIDRs (an allowlisted address) become variables, valued in
    terraform.tfvars (written here, gitignored) with placeholders in
    terraform.tfvars.example (committed);
  - drops `defined_tags` and `freeform_tags` (Oracle-Tags record who created
    each resource; both are optional and computed, so leaving them out of
    the configuration changes nothing in the plan), `= null` attributes,
    and the generator's comments (they repeat each OCID);
  - splits the resources into network.tf (oci_core_*), cluster.tf and
    nodepool.tf, and rewrites variables.tf (region kept as it was);
  - refuses to write anything if an OCID, an email address, an AD name or a
    public address is left in a committable file.

The input is renamed generated-config.tf.orig (gitignored), so Terraform
does not load the resources twice; a re-run reads the .orig.

  python3 scripts/tf_provided_codify.py
  bash scripts/tf_provided.sh fmt
  bash scripts/tf_provided.sh plan -input=false -detailed-exitcode   # 0 = zero diff
"""
import ipaddress
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "terraform" / "oci-provided"
GEN = DIR / "generated-config.tf"
ORIG = DIR / "generated-config.tf.orig"
IMPORTS = DIR / "generated-imports.tf"
TFVARS = DIR / "terraform.tfvars"
TFVARS_HEAD = "# WRITTEN by scripts/tf_provided_codify.py"

HEADER = (
    "# The PROVIDED OKE cluster, codified via terraform import: plan only, NEVER\n"
    "# apply (CLAUDE.md, the 2026-10-07 exception); every command through\n"
    "# scripts/tf_provided.sh. Written by scripts/tf_provided_codify.py from the\n"
    "# generated configuration: OCIDs are references or variables (values in the\n"
    "# gitignored terraform.tfvars), tags and null attributes dropped.\n"
)
REGION = '''variable "region" {
  description = "Region of the provided cluster."
  type        = string
  default     = "us-ashburn-1"
}
'''

DROP_KEYS = {"defined_tags", "freeform_tags"}
VAR_KEYS = {"ssh_public_key"}
OCID = re.compile(r"^ocid1\.[a-z0-9_]+\.[^\s\"]+$")
AD = re.compile(r"^[A-Za-z0-9]+:[A-Z0-9]+(?:-[A-Z0-9]+)*-AD-(\d+)$")
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
RES = re.compile(r'^resource "([a-z0-9_]+)" "([A-Za-z0-9_-]+)" \{\s*$')
KEY = re.compile(r"^\s*([A-Za-z0-9_]+)\s*(?:=|\{)")
NULL = re.compile(r"^\s*[A-Za-z0-9_]+\s*=\s*null\s*$")
IPV4 = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?\b")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def target_file(rtype: str) -> str:
    if rtype == "oci_containerengine_cluster":
        return "cluster.tf"
    if rtype == "oci_containerengine_node_pool":
        return "nodepool.tf"
    if rtype.startswith("oci_core_"):
        return "network.tf"
    raise ValueError(f"no target file for resource type {rtype}")


def depth_delta(line: str) -> int:
    """Net brackets opened on the line, ignoring those inside strings."""
    d, in_str, esc = 0, False, False
    for ch in line:
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch in "{[(":
            d += 1
        elif ch in "}])":
            d -= 1
    return d


def is_public(value: str) -> bool:
    try:
        net = ipaddress.ip_network(value, strict=False)
    except ValueError:
        return False
    return net.prefixlen > 0 and net.network_address.is_global


def import_refs(text: str) -> dict[str, str]:
    """OCID -> `type.name.id`, for import blocks whose id is a plain OCID
    (NSG rules are imported by a path, and nothing references them)."""
    return {i: f"{to}.id" for to, i in re.findall(r'to = (\S+)\n  id = "([^"]+)"', text)
            if OCID.match(i)}


def _ident(s: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", s.lower()).strip("_")


class Codifier:
    def __init__(self, refs: dict[str, str]):
        self.refs = refs
        self.vars: dict[str, dict] = {}       # name -> {value, kind, res, key}
        self.by_value: dict[str, str] = {}
        self.n_refs = 0
        self.n_dropped = 0

    def _var(self, value: str, name: str, kind: str, res: str, key: str) -> str:
        if value in self.by_value:
            return "var." + self.by_value[value]
        base, n = _ident(name), 2
        name = base
        while name in self.vars:
            name, n = f"{base}_{n}", n + 1
        self.vars[name] = {"value": value, "kind": kind, "res": res, "key": key}
        self.by_value[value] = name
        return "var." + name

    def _literal(self, m: re.Match, res: str, key: str | None) -> str:
        v, key = m.group(1), key or "value"
        if OCID.match(v):
            if v in self.refs:
                self.n_refs += 1
                return self.refs[v]
            name = "compartment_ocid" if key == "compartment_id" else f"{res}_{key}"
            return self._var(v, name, "ocid", res, key)
        a = AD.match(v)
        if a:
            return self._var(v, f"availability_domain_{a.group(1)}", "ad", res, key)
        if key in VAR_KEYS:
            return self._var(v, f"{res}_{key}", "ssh", res, key)
        if is_public(v):
            return self._var(v, f"{res}_{key}", "cidr", res, key)
        return m.group(0)

    def _block(self, lines: list[str], i: int, res: str) -> tuple[list[str], int]:
        body, depth, keys, skip = [], 1, [], 0
        while i < len(lines):
            line = lines[i]
            i += 1
            d = depth_delta(line)
            if skip:
                skip, depth = skip + d, depth + d
                continue
            if depth + d == 0 and line.strip() == "}":
                return body, i
            km = KEY.match(line)
            key = km.group(1) if km else (keys[-1] if keys else None)
            if km and (km.group(1) in DROP_KEYS or NULL.match(line)):
                self.n_dropped += 1
                skip = max(d, 0)
                depth += d
                continue
            body.append(STR.sub(lambda m: self._literal(m, res, key), line))
            if d > 0:
                keys.extend([key] * d)
            elif d < 0:
                del keys[len(keys) + d:]
            depth += d
        raise ValueError(f"resource {res}: no closing brace")

    def codify(self, text: str) -> dict[str, list[str]]:
        """file name -> rendered resource blocks, in input order."""
        out: dict[str, list[str]] = {}
        lines, i = text.splitlines(), 0
        while i < len(lines):
            line = lines[i]
            m = RES.match(line)
            if not m:
                if line.strip() and not line.lstrip().startswith("#"):
                    raise ValueError(f"unexpected top-level line {i + 1}: {line[:80]}")
                i += 1
                continue
            rtype, name = m.groups()
            body, i = self._block(lines, i + 1, name)
            block = f'resource "{rtype}" "{name}" {{\n' + "".join(l + "\n" for l in body) + "}\n"
            out.setdefault(target_file(rtype), []).append(block)
        return out


DESCRIPTIONS = {
    "ocid": "OCID: {key} of {res} (not a codified resource, so a variable).",
    "ad": "Availability-domain name (tenancy-prefixed).",
    "ssh": "SSH public key set on {res}.",
    "cidr": "Public address in {key} of {res}.",
}


def placeholder(meta: dict) -> str:
    v = meta["value"]
    if meta["kind"] == "ocid":
        kind = v.split(".")[1]
        return f"ocid1.{kind}.oc1..<{kind}-ocid>"
    if meta["kind"] == "ad":
        return f"<tenancy-prefix>:US-ASHBURN-AD-{AD.match(v).group(1)}"
    if meta["kind"] == "ssh":
        return "ssh-rsa <public key>"
    return "<address>/32"


def render(c: Codifier, files: dict[str, list[str]]) -> dict[str, str]:
    """Committable files, name -> text."""
    out = {name: HEADER + "\n" + "\n".join(blocks) for name, blocks in sorted(files.items())}
    var_blocks = [REGION]
    example = ["# terraform/oci-provided: placeholders only. The real terraform.tfvars is\n"
               "# written beside it by scripts/tf_provided_codify.py on the operator\n"
               "# (gitignored: it holds the OCIDs).\n"]
    for name in sorted(c.vars):
        meta = c.vars[name]
        desc = DESCRIPTIONS[meta["kind"]].format(**meta)
        var_blocks.append(f'variable "{name}" {{\n  description = "{desc}"\n  type        = string\n}}\n')
        example.append(f'{name} = "{placeholder(meta)}"\n')
    out["variables.tf"] = HEADER + "\n" + "\n".join(var_blocks)
    out["terraform.tfvars.example"] = "".join(example)
    return out


def leaks(text: str) -> list[str]:
    """Identifying values left in a committable file."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        if "ocid1." in line and "<" not in line:
            hits.append(f"{n}: OCID")
        if EMAIL.search(line):
            hits.append(f"{n}: email")
        for s in STR.findall(line):
            if AD.match(s):
                hits.append(f"{n}: AD name")
        for ip in IPV4.findall(line):
            if is_public(ip if "/" in ip else ip + "/32"):
                hits.append(f"{n}: public address")
    return hits


def tfvars(c: Codifier) -> str:
    lines = [f"{TFVARS_HEAD} — gitignored, real values. Do not commit.\n"]
    lines += [f'{n} = "{c.vars[n]["value"]}"\n' for n in sorted(c.vars)]
    return "".join(lines)


def main() -> int:
    src = GEN if GEN.exists() else ORIG
    if not src.exists():
        print(f"neither {GEN.name} nor {ORIG.name} exists: run the generate step first")
        return 2
    if TFVARS.exists() and not TFVARS.read_text(encoding="utf-8").startswith(TFVARS_HEAD):
        print(f"{TFVARS.name} exists and was not written by this script: move it aside first")
        return 2
    c = Codifier(import_refs(IMPORTS.read_text(encoding="utf-8")))
    out = render(c, c.codify(src.read_text(encoding="utf-8")))
    bad = {name: h for name, text in out.items() if (h := leaks(text))}
    if bad:
        for name, h in bad.items():
            print(f"LEAK {name}: {', '.join(h[:10])}{' ...' if len(h) > 10 else ''}")
        print("nothing written")
        return 1
    for name, text in out.items():
        (DIR / name).write_text(text, encoding="utf-8")
    TFVARS.write_text(tfvars(c), encoding="utf-8")
    if src == GEN:
        GEN.rename(ORIG)
    for name, text in out.items():
        print(f"  {name:26} {text.count(chr(10)):5} lines")
    print(f"{c.n_refs} OCIDs -> references, {len(c.vars)} variables, "
          f"{c.n_dropped} attributes dropped; {src.name} -> {ORIG.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
