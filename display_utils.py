"""Display-only helpers for the Streamlit UI.

The synthesis model sometimes emits inline source citations — backtick-wrapped
raw source fields like `market_cap: 4342023192576.0` — which Markdown renders as
green monospace inline code, interrupting the prose. These helpers strip that
markup at render time only. They do NOT touch the generated/cached/stored brief
or the grounding eval, which run through separate code paths.
"""
import re

# A raw-source citation: an inline-code span quoting a source field, e.g.
# `market_cap: 4342023192576.0`, `pe_ratio: 35.8`, `filing_date: "2026-04-29"`.
_FIELD = r"`[^`\n]*?[A-Za-z][\w ]*:\s*[^`\n]*`"
_FIELD_IN_PARENS = re.compile(r"[(\[]\s*" + _FIELD + r"\s*[)\]]")
_FIELD_BARE = re.compile(_FIELD)
_INLINE_CODE = re.compile(r"`([^`\n]+)`")


def strip_source_citations(text: str) -> str:
    """Remove inline source-citation markup so a brief renders as clean prose.

    - `field: value` citations are removed outright (with any wrapping parens
      or brackets).
    - Any other stray inline-code is unwrapped to plain text, so nothing is left
      rendering as monospace.
    - Whitespace/punctuation left behind is tidied.
    """
    if not text:
        return text

    text = _FIELD_IN_PARENS.sub("", text)   # drop "(`field: value`)" / "[`field: value`]"
    text = _FIELD_BARE.sub("", text)        # drop bare "`field: value`"
    text = _INLINE_CODE.sub(r"\1", text)    # unwrap any remaining inline code

    text = re.sub(r"[ \t]{2,}", " ", text)              # collapse runs of spaces
    text = re.sub(r" +([.,;:)])", r"\1", text)          # space before punctuation
    text = re.sub(r"\(\s*\)|\[\s*\]", "", text)         # emptied parens/brackets
    text = re.sub(r" +,", ",", text)                    # space before comma
    text = re.sub(r"[ \t]+\n", "\n", text)              # trailing spaces per line
    return text


def strip_source_citations_stream(chunks):
    """Streaming wrapper for ``st.write_stream``. Buffers across chunks while a
    backtick span is still open, so a citation split across tokens is stripped
    rather than flashing on screen mid-render."""
    buffer = ""
    for chunk in chunks:
        buffer += chunk
        if buffer.count("`") % 2 == 0:
            # all backticks balanced — safe to sanitize and flush
            if buffer:
                yield strip_source_citations(buffer)
            buffer = ""
        else:
            # an inline-code span is still open — hold from the last backtick,
            # flush the sanitized text before it
            cut = buffer.rfind("`")
            prefix, buffer = buffer[:cut], buffer[cut:]
            if prefix:
                yield strip_source_citations(prefix)
    if buffer:
        yield strip_source_citations(buffer)
