#!/usr/bin/env python3
"""Semantic diff between two rendered Kubernetes manifest sets.

Written for the kustomize migration acceptance check (kind overlay renders
must equal the pre-kustomize manifests), but generic: each side is a YAML
file (multi-doc) or a directory of *.yaml files. Documents are keyed by
(apiVersion, kind, namespace, name), canonicalized with sorted keys, and
compared — so comments, formatting, field order, and resource order don't
count as differences; any real config change does.

Usage:
    python3 scripts/render_diff.py LEFT RIGHT
Exit 0: semantically identical. Exit 1: differences (printed as unified diff).
"""
import difflib
import pathlib
import sys

import yaml


def load_docs(path):
    p = pathlib.Path(path)
    files = sorted(p.glob("*.yaml")) if p.is_dir() else [p]
    docs = {}
    for f in files:
        for doc in yaml.safe_load_all(f.read_text()):
            if not doc:
                continue
            meta = doc.get("metadata", {})
            key = (
                doc.get("apiVersion", "?"),
                doc.get("kind", "?"),
                meta.get("namespace", ""),
                meta.get("name", "?"),
            )
            if key in docs:
                print(f"WARNING: duplicate resource in {path}: {'/'.join(key)}")
            docs[key] = doc
    return docs


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    left_path, right_path = sys.argv[1], sys.argv[2]
    left, right = load_docs(left_path), load_docs(right_path)
    identical = True
    for key in sorted(set(left) | set(right)):
        label = "/".join(k for k in key if k)
        if key not in left:
            print(f"ONLY IN {right_path}: {label}")
            identical = False
            continue
        if key not in right:
            print(f"ONLY IN {left_path}: {label}")
            identical = False
            continue
        a = yaml.safe_dump(left[key], sort_keys=True)
        b = yaml.safe_dump(right[key], sort_keys=True)
        if a != b:
            identical = False
            print(f"DIFF: {label}")
            sys.stdout.writelines(
                difflib.unified_diff(
                    a.splitlines(True),
                    b.splitlines(True),
                    fromfile=f"{left_path} {label}",
                    tofile=f"{right_path} {label}",
                )
            )
    if identical:
        print(f"IDENTICAL: {len(left)} resources match semantically")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
