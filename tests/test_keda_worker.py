"""KEDA ScaledObject for the Celery worker (k8s/keda) and its live test
(scripts/keda_scale_test.sh). Offline: reads the committed YAML, no cluster,
no Anthropic call.

Pins what the ScaledObject silently depends on: the Redis list it reads is
Celery's default queue in the DB REDIS_URL names, the address is the redis
Service, min stays 1, and the app overlays never need the KEDA CRDs. Pins
that the live test sends only Celery's builtin `celery.accumulate`, which
returns its arguments, so it spends no credit and cannot fail on the worker."""
import os
import pathlib
import re
from urllib.parse import urlparse

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
KEDA = ROOT / "k8s" / "keda"


def _docs(path):
    return [d for d in yaml.safe_load_all(path.read_text()) if d]


def _scaledobject():
    (so,) = _docs(KEDA / "base" / "scaledobject.yaml")
    return so


def _overlay_patches(name):
    k = yaml.safe_load((KEDA / "overlays" / name / "kustomization.yaml").read_text())
    assert k["resources"] == ["../../base"]
    return [yaml.safe_load(p["patch"]) for p in k.get("patches", [])]


def _effective(name):
    """Base ScaledObject with the overlay's strategic-merge spec patches applied
    (the overlays only set top-level spec scalars)."""
    so = _scaledobject()
    for p in _overlay_patches(name):
        assert p["kind"] == "ScaledObject" and p["metadata"]["name"] == "worker"
        so["spec"].update(p["spec"])
    return so


def _base(kind, name):
    for f in sorted((ROOT / "k8s" / "base").glob("*.yaml")):
        for d in _docs(f):
            if d["kind"] == kind and d["metadata"]["name"] == name:
                return d
    raise AssertionError(f"{kind}/{name} not in k8s/base")


def _celery_app():
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
    from celery_worker import celery_app
    celery_app.finalize()
    return celery_app


def test_targets_the_worker_deployment():
    so, worker = _scaledobject(), _base("Deployment", "worker")
    assert so["metadata"]["namespace"] == worker["metadata"]["namespace"] == "financial-agent"
    assert so["spec"]["scaleTargetRef"] == {"apiVersion": "apps/v1", "kind": "Deployment", "name": "worker"}


def test_min_is_one_everywhere():
    for overlay in ("kind", "oke-provided"):
        so = _effective(overlay)
        assert so["spec"]["minReplicaCount"] == 1, overlay
        assert so["spec"]["maxReplicaCount"] >= 2, overlay
    assert _effective("kind")["spec"]["maxReplicaCount"] == 2
    assert _effective("oke-provided")["spec"]["maxReplicaCount"] == 4


def test_overlays_differ_from_base_only_in_max():
    assert _overlay_patches("kind") == []
    (p,) = _overlay_patches("oke-provided")
    assert p["spec"] == {"maxReplicaCount": 4}


def test_reads_celerys_queue_in_redis_url_db():
    (trig,) = _scaledobject()["spec"]["triggers"]
    assert trig["type"] == "redis"
    md = trig["metadata"]
    assert md["listName"] == _celery_app().conf.task_default_queue == "celery"

    url = urlparse(_base("ConfigMap", "app-config")["data"]["REDIS_URL"])
    assert md["databaseIndex"] == url.path.lstrip("/") == "0"

    svc = _base("Service", "redis")
    host, port = md["address"].rsplit(":", 1)
    # KEDA runs in its own namespace: the address must be fully qualified
    assert host == f"{svc['metadata']['name']}.{svc['metadata']['namespace']}.svc.cluster.local"
    assert int(port) == svc["spec"]["ports"][0]["port"] == url.port
    assert int(md["listLength"]) >= 1


def test_app_overlays_do_not_need_keda():
    """kind, oke, k3s and the provided-cluster overlays apply without KEDA."""
    for k in (ROOT / "k8s" / "overlays").glob("*/kustomization.yaml"):
        text = k.read_text()
        assert "keda" not in text.lower() and "ScaledObject" not in text, k
    for f in (ROOT / "k8s" / "base").glob("*.yaml"):
        assert "keda.sh" not in f.read_text(), f


def test_accumulate_is_a_builtin_that_only_returns_its_args():
    app = _celery_app()
    assert "celery.accumulate" in app.tasks
    assert app.tasks["celery.accumulate"].__module__.startswith("celery.")
    assert app.tasks["celery.accumulate"](7) == (7,)


def test_scale_test_sends_only_accumulate():
    script = (ROOT / "scripts" / "keda_scale_test.sh").read_text()
    code = "\n".join(l for l in script.splitlines() if not l.lstrip().startswith("#"))
    assert re.findall(r"send_task\('([^']+)'", code) == ["celery.accumulate"]
    assert "research_task" not in code and ".delay(" not in code and "apply_async" not in code
    # the original worker's consumer is restored on every exit
    assert "trap restore EXIT" in code


def test_chart_is_pinned_by_version_and_digest():
    mk = (ROOT / "Makefile").read_text()
    assert re.search(r"^KEDA_CHART_VERSION \?= 2\.21\.0$", mk, re.M)
    assert re.search(r"^KEDA_CHART_SHA256  \?= [0-9a-f]{64}$", mk, re.M)
    assert "sha256sum -c" in mk
    values = yaml.safe_load((KEDA / "install" / "values.yaml").read_text())
    assert values == {"watchNamespace": "financial-agent"}
