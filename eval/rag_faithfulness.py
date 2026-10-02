"""RAG faithfulness: is each SEC RAG answer supported by the chunks it was
written from?

A separate metric, never folded into the grounding rate. The main judge
(agent/grounding.py, v2) audits the brief against a source context in which
the RAG answers ARE the source — so an unfaithful RAG answer reads as
"supported" there. This judges each RAG answer against exactly the retrieved
chunks the query engine handed its LLM, on every arm, so hosted and SLM RAG
answering are measured the same way. The main judge and its inputs are
untouched, so the v2 calibration still applies to the main rate.

Same model as the main judge (Sonnet, temperature 0, via get_judge_llm), its
own prompt, versioned. UNVALIDATED: no human labels exist for this prompt;
report its rates as judge-flagged, labelled with RAG_JUDGE_PROMPT_VERSION.
On only when EVAL_RAG_FAITHFULNESS=true (two extra Sonnet calls per ticker).
"""
import os
import re

from langchain_core.messages import HumanMessage, SystemMessage

from eval.label import count_labels_deduped

RAG_JUDGE_PROMPT_VERSION = "rf-v1"

RAG_JUDGE_SYSTEM = """\
You are auditing an answer that was written from retrieved SEC-filing \
passages. Judge it ONLY against the passages below — not against outside \
knowledge, and not against what you believe is true about the company.

For every factual claim in the answer (each figure, date, period, named \
product/segment/risk, and each statement attributed to the filing), output \
one entry in this exact format:

CLAIM: "<exact quoted text>"
LABEL: SUPPORTED | UNSUPPORTED
REASON: <one sentence citing the passage, or stating what is absent>

SUPPORTED   — stated in the passages; figures and periods must match exactly.
UNSUPPORTED — absent from the passages, contradicts them, or adds a figure, \
period or qualifier they do not contain.

Be exhaustive.\
"""

_PREFIX_RE = re.compile(r"^\[(From Pinecone cache|Indexed to Pinecone)\]\s*")


def enabled() -> bool:
    return os.getenv("EVAL_RAG_FAITHFULNESS", "false").strip().lower() == "true"


def strip_tool_prefix(answer: str) -> str:
    """query_sec_filing prefixes its answer with where the index came from."""
    return _PREFIX_RE.sub("", answer or "")


def user_prompt(chunks: list[str], answer: str) -> str:
    passages = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(chunks, 1))
    return (f"=== RETRIEVED PASSAGES ===\n{passages}\n\n"
            f"=== ANSWER TO AUDIT ===\n{strip_tool_prefix(answer)}\n")


def grade(chunks: list[str], answer: str, invoke) -> dict:
    """`invoke(messages) -> response with .content` (the harness passes its
    retry-wrapped judge). Returns counts plus the raw findings."""
    findings = invoke([SystemMessage(content=RAG_JUDGE_SYSTEM),
                       HumanMessage(content=user_prompt(chunks, answer))]).content
    c = count_labels_deduped(findings)
    total = c["supported"] + c["unsupported"]
    return {"supported": c["supported"], "unsupported": c["unsupported"], "total": total,
            "unparsed_inference": c["inference"], "findings": findings,
            "prompt_version": RAG_JUDGE_PROMPT_VERSION}
