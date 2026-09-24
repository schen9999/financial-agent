"""eval/section_attribution.py: canonical names, attribution, bucketing."""
from eval.section_attribution import attribute, bucket, canonical_section


def _secs(**kw):
    import re

    from eval.section_attribution import _norm, _words
    return {k: (_norm(v), _words(v)) for k, v in kw.items()}


def test_canonical_section_tolerates_model_written_headings():
    assert canonical_section("Financial Health") == "financial-health"
    assert canonical_section("Primary Risk Factors Disclosed") == "risk-factors"
    assert canonical_section("Risk Factors Disclosed") == "risk-factors"
    assert canonical_section("Recent Developments") == "recent-developments"
    assert canonical_section("SEC Filing Highlights") == "sec-filing-highlights"


def test_attribute_containment_beats_overlap():
    secs = _secs(**{
        "financial-health": "Revenue was $4.3 billion with a 45.3% margin.",
        "recent-developments": "The company announced a new partnership.",
    })
    assert attribute("revenue was $4.3 billion", secs) == "financial-health"


def test_attribute_word_overlap_threshold():
    secs = _secs(**{
        "risk-factors": "Competition in cloud services is intense and pricing "
                        "pressure could reduce margins significantly.",
    })
    # Paraphrase with high word overlap attributes; unrelated text does not.
    assert attribute("intense competition and pricing pressure could reduce "
                     "margins", secs) == "risk-factors"
    assert attribute("astronaut training requires zero-gravity simulation",
                     secs) is None
    assert attribute(None, secs) is None


def test_bucket_partitions():
    assert bucket("financial-health") == "fine-tune-owned"
    assert bucket("risk-factors") == "fine-tune-owned"
    assert bucket("recent-developments") == "other-sections"
    assert bucket(None) == "unattributed"
