#!/usr/bin/env python3
"""Pin, or check the pin of, the GHCR app image in the oke-provided overlays.

The app image is pinned twice — k8s/overlays/<overlay> (the Deployments) and
argo/overlays/<overlay> (the eval pods) — and the two must always name the
same build. Both carry one kustomize images: entry for financial-agent-app;
this script owns its newTag.

  --tag <sha>   rewrite newTag in both overlays (what `make oke-images` runs
                after pushing ghcr.io/...:<sha>)
  --check       exit non-zero unless both overlays carry the same full
                40-hex git sha — never the committed UNPINNED placeholder
                (what `make oke-up` and `make argo-deploy` run first)

Each overlay must contain the entry exactly once; anything else means the
overlay drifted from what this script expects, and it exits non-zero rather
than half-pin. Stdlib only, no newer-than-3.6 syntax: it runs on the
operator host, whose python3 may be old.
"""
import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE = "financial-agent-app"
PLACEHOLDER = "UNPINNED"
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_ENTRY_RE = re.compile(
    r"(- name: " + re.escape(IMAGE) + r"\r?\n[ \t]+newName: \S+\r?\n[ \t]+newTag: )(\S+)$",
    re.M)


def overlay_files(overlay):
    return [os.path.join(REPO, tree, "overlays", overlay, "kustomization.yaml")
            for tree in ("k8s", "argo")]


def _entry(path, text):
    hits = _ENTRY_RE.findall(text)
    if len(hits) != 1:
        raise SystemExit("pin_oke_image: expected exactly 1 %s images: entry "
                         "with newName + newTag in %s, found %d - overlay drifted"
                         % (IMAGE, path, len(hits)))
    return hits[0][1]


def read_tags(overlay):
    tags = {}
    for path in overlay_files(overlay):
        with open(path, encoding="utf-8") as f:
            tags[path] = _entry(path, f.read())
    return tags


def check(overlay):
    """Return the pinned sha, or raise SystemExit naming what is wrong."""
    tags = read_tags(overlay)
    values = set(tags.values())
    if len(values) != 1:
        raise SystemExit("pin_oke_image: the overlays pin different tags: %s - "
                         "re-run make oke-images" % tags)
    tag = values.pop()
    if tag == PLACEHOLDER:
        raise SystemExit("pin_oke_image: overlays still say %s - run make "
                         "oke-images on the laptop, commit the pin, push, and "
                         "pull it here first" % PLACEHOLDER)
    if not _SHA_RE.match(tag):
        raise SystemExit("pin_oke_image: pinned tag %r is not a full 40-hex git "
                         "sha - images are tagged with the commit they were "
                         "built from, never :latest" % tag)
    return tag


def pin(overlay, sha):
    if not _SHA_RE.match(sha):
        raise SystemExit("pin_oke_image: --tag must be a full 40-hex git sha, "
                         "got %r" % sha)
    texts = {}
    for path in overlay_files(overlay):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        _entry(path, text)  # validate every file before writing any
        texts[path] = text
    for path, text in texts.items():
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(_ENTRY_RE.sub(lambda m: m.group(1) + sha, text))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--overlay", default="oke-provided")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tag", help="full git sha to pin")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        print("pinned app image tag: %s" % check(args.overlay))
    else:
        pin(args.overlay, args.tag)
        print("pinned %s:%s in %s" % (IMAGE, args.tag,
                                     ", ".join(overlay_files(args.overlay))))


if __name__ == "__main__":
    sys.exit(main())
