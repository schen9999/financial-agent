#!/usr/bin/env python3
"""Fix up terraform/oci-provided/generated-config.tf (gitignored; written by
`plan -generate-config-out`) where the generated configuration cannot be
planned as written. Each rule names the resource type, the attribute it
drops and why; nothing else in the file changes.

  oci_containerengine_node_pool  quantity_per_subnet, subnet_ids
      legacy placement fields, generated beside node_config_details, which
      the provider rejects as conflicting ("node_config_details conflicts
      with quantity_per_subnet"); the pools are placed by
      node_config_details.placement_configs

  python3 scripts/tf_provided_fixup.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "terraform" / "oci-provided" / "generated-config.tf"
DROP = {
    "oci_containerengine_node_pool": {"quantity_per_subnet", "subnet_ids"},
}
RES = re.compile(r'^resource "([a-z0-9_]+)" "[^"]+" \{')
ATTR = re.compile(r"^  ([a-z0-9_]+)\s+=\s*(.*)$")


def fixup(text: str) -> tuple[str, int]:
    out, rtype, dropped, skip_depth = [], None, 0, 0
    for line in text.splitlines():
        if skip_depth:
            skip_depth += line.count("[") + line.count("{") - line.count("]") - line.count("}")
            continue
        m = RES.match(line)
        if m:
            rtype = m.group(1)
        elif line == "}":
            rtype = None
        a = ATTR.match(line)
        if rtype and a and a.group(1) in DROP.get(rtype, ()):
            dropped += 1
            depth = a.group(2).count("[") + a.group(2).count("{") - a.group(2).count("]") - a.group(2).count("}")
            skip_depth = max(depth, 0)
            continue
        out.append(line)
    return "\n".join(out) + "\n", dropped


def main() -> int:
    text, n = fixup(GEN.read_text(encoding="utf-8"))
    GEN.write_text(text, encoding="utf-8")
    print(f"dropped {n} attribute(s) from {GEN.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
