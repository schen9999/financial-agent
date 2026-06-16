"""Display-only helpers for the Streamlit UI.

The synthesis model sometimes emits inline source citations — backtick-wrapped
raw source fields like `market_cap: 4342023192576.0` — which Markdown renders as
green monospace inline code, interrupting the prose. These helpers strip that
markup at render time only. They do NOT touch the generated/cached/stored brief
or the grounding eval, which run through separate code paths.
"""
import re

# Source citations are inline-code (backtick) spans the model appends to cite raw
# source data — e.g. `market_cap: 4342023192576.0` or `**$5.15 trillion**`. They
# render as green monospace, and their inner content can itself contain markdown.
# The whole span (delimiters AND content) must be removed; unwrapping would leave
# the inner markdown to render as stray bold/italic. Only backtick-delimited
# spans are touched, so legitimate **bold** risk headers and *italics* are safe.
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_INLINE_CODE_IN_BRACKETS = re.compile(r"[(\[]\s*`[^`\n]*`\s*[)\]]")


def strip_source_citations(text: str) -> str:
    """Remove inline source-citation spans (and their content) so a brief renders
    as clean prose. Display-only; does not alter the generated/cached brief."""
    if not text:
        return text

    text = _INLINE_CODE_IN_BRACKETS.sub("", text)   # drop "(`...`)" / "[`...`]" wholesale
    text = _INLINE_CODE.sub("", text)               # drop any remaining "`...`" span + content

    text = re.sub(r"[ \t]{2,}", " ", text)          # collapse runs of spaces
    text = re.sub(r" +([.,;:)])", r"\1", text)      # space before punctuation
    text = re.sub(r"\(\s*\)|\[\s*\]", "", text)     # emptied parens/brackets
    text = re.sub(r" +,", ",", text)                # space before comma
    text = re.sub(r"[ \t]+\n", "\n", text)          # trailing spaces per line
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
