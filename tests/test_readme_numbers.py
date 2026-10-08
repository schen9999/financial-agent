"""The README's result figures all appear in docs/numbers-of-record.md
(scripts/readme_numbers_check.py), and the check catches one that does not."""
from scripts import readme_numbers_check as rc


def test_readme_figures_are_on_record():
    readme = (rc.ROOT / "README.md").read_text(encoding="utf-8")
    record = (rc.ROOT / "docs" / "numbers-of-record.md").read_text(encoding="utf-8")
    assert rc.missing(readme, record) == []


def test_an_unrecorded_figure_is_caught():
    readme = "## Conclusions\nhosted 9.99% vs 1/565, CI −4.39 to +1.78\n## Tech Stack\n"
    assert rc.missing(readme, "1/565 and -4.39 to 1.78") == ["9.99%"]
