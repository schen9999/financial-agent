#!/usr/bin/env python3
"""Poll an OpenAI-compatible server until /v1/models lists a model name.

`make vm-vllm` runs this right after `kubectl rollout status`: the rollout
can report ready before the NodePort answers (connection refused, hit on
2026-09-23 on two consecutive swaps), so a single check races the service.
Retries every --interval seconds until --timeout, then exits non-zero with
the last error. Each attempt is eval.runtime_guards.check_local_model_served,
the same check the eval harness runs before a local-model arm. Stdlib only:
it runs on the VM host.

Usage:
  python3 scripts/wait_for_model.py --url http://localhost:30880 --name financial-lora
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.runtime_guards import check_local_model_served  # noqa: E402


def wait_for_model(url: str, name: str, timeout: float = 120.0, interval: float = 5.0,
                   check=check_local_model_served, sleep=time.sleep,
                   clock=time.monotonic) -> list[str]:
    """Return the served ids once `name` is listed; SystemExit after `timeout`."""
    deadline = clock() + timeout
    attempt = 0
    while True:
        attempt += 1
        try:
            return check(url, name, timeout=10.0)
        except SystemExit as e:
            if clock() + interval > deadline:
                raise SystemExit(f"{e}\n  gave up after {attempt} attempt(s) "
                                 f"over {timeout:.0f}s")
            print(f"  /v1/models not ready (attempt {attempt}): "
                  f"{str(e).splitlines()[0]}", flush=True)
            sleep(interval)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--url", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--interval", type=float, default=5.0)
    args = ap.parse_args()
    ids = wait_for_model(args.url, args.name, args.timeout, args.interval)
    print(f"/v1/models: {ids}")


if __name__ == "__main__":
    main()
