"""scripts/tf_provided.sh: Terraform in terraform/oci-provided/ is import and
plan only — apply, destroy, CLI import, state writes, saved plans and
-auto-approve are refused before terraform runs."""
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "tf_provided.sh"
BASH = shutil.which("bash")


@pytest.mark.skipif(BASH is None, reason="bash not available")
@pytest.mark.parametrize("args", [["apply"], ["destroy"], ["import", "a.b", "ocid1.x"], ["refresh"],
                                  ["taint", "a.b"], ["state", "rm", "a.b"], ["state", "push", "x"],
                                  ["plan", "-out=p.tfplan"], ["plan", "-out", "p"], ["console"],
                                  ["plan", "-auto-approve"], ["force-unlock", "id"]])
def test_refused(args):
    r = subprocess.run([BASH, str(SCRIPT), *args], capture_output=True, text=True)
    assert r.returncode == 3 and "refused" in r.stdout


def test_allowed_commands_are_the_documented_ones():
    src = SCRIPT.read_text(encoding="utf-8")
    assert "init|fmt|validate|plan|show|providers) ;;" in src
    assert "list|show) ;;" in src
