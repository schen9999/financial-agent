#!/usr/bin/env python3
"""Every result figure in the README must appear in docs/numbers-of-record.md.

Scans the README from "## Conclusions" to "## Tech Stack" (conclusions,
next steps, deployment, key results, decisions) for result figures —
percentages, dollar amounts, ratios (n/m), multipliers (1.8×), CI bounds and
decimals with a unit (tok/s, s) — and looks each up in numbers-of-record,
normalising the minus sign and thousands separators. Exit 1 lists any figure
the record does not hold. Counts that are not results (40 tickers, 20%
limits, 8 vCPU) and dates are not checked.

  python scripts/readme_numbers_check.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG = re.compile(
    r"\$\d+(?:\.\d+)?"                 # $0.0357
    r"|[−+-]?\d+(?:\.\d+)?%"           # 2.55%, −4.39%
    r"|\d+/\d+"                        # 1/565
    r"|\d+(?:\.\d+)?×"                 # 1.8×
    r"|[−+]\d+(?:\.\d+)?"              # +0.93, −4.39
    r"|\d+\.\d+")                      # 4.47, 1075.7
SKIP = {"4.5", "4.6", "3.7", "1.5", "0.10.2", "1.34", "3.6",   # model and tool versions
        "20.4"}                                                  # the GGUF's size in GB


def norm(s: str) -> str:
    return s.replace("−", "-").replace(",", "").replace("+", "")


def section(text: str) -> str:
    return text[text.index("## Conclusions"):text.index("## Tech Stack")]


def missing(readme: str, record: str) -> list[str]:
    rec = norm(record)
    out = []
    for f in sorted(set(FIG.findall(section(readme)))):
        n = norm(f)
        bare = n.rstrip("%×").lstrip("$")
        if f in SKIP or bare in SKIP or re.fullmatch(r"\d+/\d+", n) and n.split("/")[1] in ("10",):
            continue
        if n not in rec and bare not in rec:
            out.append(f)
    return out


def main() -> int:
    m = missing((ROOT / "README.md").read_text(encoding="utf-8"),
                (ROOT / "docs" / "numbers-of-record.md").read_text(encoding="utf-8"))
    for f in m:
        print(f"not in numbers-of-record: {f}")
    print("README figures: " + ("all in numbers-of-record" if not m else f"{len(m)} missing"))
    return 1 if m else 0


if __name__ == "__main__":
    sys.exit(main())
