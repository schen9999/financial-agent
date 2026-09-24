"""eval/build_fourarm_holdout.py must not overwrite the reserved sample's
method record, and a forced redraw must keep its provenance fields."""
import json

import pytest

from eval import build_fourarm_holdout as b


def test_refuses_when_method_file_exists(tmp_path):
    path = tmp_path / "fourarm_holdout_method.json"
    path.write_text('{"sample_size": 78}', encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        b.check_can_write(path, force=False)
    assert "refusing to overwrite" in str(exc.value)
    assert json.loads(path.read_text(encoding="utf-8")) == {"sample_size": 78}


def test_main_refuses_before_writing_anything(monkeypatch, tmp_path):
    path = tmp_path / "fourarm_holdout_method.json"
    path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(b, "METHOD_FILE", path)
    monkeypatch.setattr(b, "collect_claims",
                        lambda *a, **k: pytest.fail("must refuse before reading or drawing"))
    with pytest.raises(SystemExit):
        b.main([])


def test_force_keeps_provenance_fields(tmp_path):
    path = tmp_path / "fourarm_holdout_method.json"
    path.write_text(json.dumps({"sample_size": 78, "key_location": "outside the repo",
                                "key_exposure": "public 7053e1f..85b6693"}),
                    encoding="utf-8")
    out = b.write_method(path, {"sample_size": 80}, force=True)
    on_disk = json.loads(path.read_text(encoding="utf-8"))
    assert on_disk == out
    assert on_disk["sample_size"] == 80
    assert on_disk["key_location"] == "outside the repo"
    assert on_disk["key_exposure"] == "public 7053e1f..85b6693"


def test_writes_fresh_when_absent(tmp_path):
    path = tmp_path / "fourarm_holdout_method.json"
    b.write_method(path, {"sample_size": 78})
    assert json.loads(path.read_text(encoding="utf-8")) == {"sample_size": 78}
