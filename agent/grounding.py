"""Shared LLM-as-judge grounding logic — the single source of truth.

Both the offline eval harness (`grounding_check.py`) and the inline
grounding-critic node (`agent/graph.py`) import from here, so there is exactly
one definition of the judge prompt, the claim parsing, and the scoring. This
module is intentionally pure: it does NOT import `agent.core`, so the critic can
live inside the graph without a circular import.

The judge audits ONLY the Executive Summary and Outlook of a brief, labelling
every quantitative / forward-looking claim SUPPORTED / UNSUPPORTED / INFERENCE
against the source context the brief was generated from.
"""
import os
import re
from dataclasses import dataclass

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# ── Judge prompt ────────────────────────────────────────────────────────────────

JUDGE_SYSTEM = """\
You are a financial accuracy auditor. Your task is to verify whether specific \
claims in an AI-generated investment brief are grounded in the source data the \
model was given.

Evaluate ONLY the Executive Summary and Outlook sections. For every specific \
quantitative figure, price target, threshold, ratio, metric, percentage, named \
product milestone, or forward-looking number in those sections, output one entry \
in this exact format:

CLAIM: "<exact quoted text>"
LABEL: SUPPORTED | UNSUPPORTED | INFERENCE
REASON: <one sentence — if SUPPORTED, cite the source figure; if UNSUPPORTED, \
state it does not appear in the context; if INFERENCE, explain the derivation>

Definitions:
  SUPPORTED   — the exact number or fact is explicitly present in the source \
data or pre-written sections below.
  UNSUPPORTED — a specific number, price target, threshold, or named milestone \
that does NOT appear in the source data and cannot be derived from it.
  INFERENCE   — a directional conclusion, rounded/scaled figure, or reasonable \
extrapolation that follows logically from the data but is not verbatim in it.

Be exhaustive — do not skip any quantitative or forward-looking claim.\
"""


def judge_user_prompt(source_context: str, section_block: str, exec_and_outlook: str) -> str:
    """Build the judge's user message. `section_block` is the four pre-written
    sections (direct synthesis input); `exec_and_outlook` is the text to audit."""
    return f"""BACKGROUND: An AI wrote the Executive Summary and Outlook using the \
four pre-written sections as its primary input. The raw source data below is what \
those sections were originally generated from.

=== RAW SOURCE DATA ===
{source_context}

=== PRE-WRITTEN SECTIONS (direct input to the synthesis model) ===
{section_block}

=== EXECUTIVE SUMMARY AND OUTLOOK TO AUDIT ===
{exec_and_outlook}
"""


# ── Brief / findings parsing ─────────────────────────────────────────────────────

def extract_exec_and_outlook(brief: str) -> str:
    """Pull only the Executive Summary and Outlook text from the full brief."""
    target_headings = {"Executive Summary", "Outlook"}
    result, current, buf = [], None, []

    for line in brief.split("\n"):
        if line.startswith("### "):
            if current in target_headings:
                result.append(f"### {current}\n" + "\n".join(buf).strip())
            current = line[4:].strip()
            buf = []
        else:
            if current in target_headings:
                buf.append(line)

    if current in target_headings:
        result.append(f"### {current}\n" + "\n".join(buf).strip())

    return "\n\n".join(result)


def count_labels(text: str) -> dict[str, int]:
    """Count SUPPORTED / UNSUPPORTED / INFERENCE labels in judge findings.
    Matches both plain "LABEL: X" and bold "**LABEL:** X" judge formatting."""
    return {
        "supported":   len(re.findall(r"\*{0,2}LABEL:\*{0,2}\s+SUPPORTED\b",   text, re.I)),
        "unsupported": len(re.findall(r"\*{0,2}LABEL:\*{0,2}\s+UNSUPPORTED\b", text, re.I)),
        "inference":   len(re.findall(r"\*{0,2}LABEL:\*{0,2}\s+INFERENCE\b",   text, re.I)),
    }


def extract_claims(findings: str, label: str) -> list[str]:
    """Pull the quoted CLAIM text for every entry the judge gave `label`.
    Tolerates both plain and bold (**...**) judge formatting."""
    out = []
    for block in re.split(r"\*{0,2}CLAIM:\*{0,2}", findings)[1:]:
        m = re.search(r"\*{0,2}LABEL:\*{0,2}\s*([A-Za-z]+)", block)
        if m and m.group(1).upper() == label.upper():
            claim = block.split("\n", 1)[0].strip().strip('"').strip()
            if claim:
                out.append(claim)
    return out


# ── Judge LLM (lazy, patchable) ──────────────────────────────────────────────────

_judge_llm = None


def get_judge_llm() -> ChatAnthropic:
    """Lazily build and cache the temperature-0 Sonnet judge. Built on first use
    so importing this module stays cheap and tests can patch it before any call."""
    global _judge_llm
    if _judge_llm is None:
        _judge_llm = ChatAnthropic(
            model="claude-sonnet-4-6",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0,
            streaming=False,
        )
    return _judge_llm


# ── Scoring ──────────────────────────────────────────────────────────────────────

@dataclass
class GradeResult:
    """Outcome of grading one brief's Exec Summary + Outlook."""
    findings: str
    supported: int
    unsupported: int
    inference: int
    total: int
    unsupported_pct: float
    inference_claims: list[str]
    unsupported_claims: list[str]


def grade_brief(source_context: str, section_block: str, exec_and_outlook: str,
                *, invoker=None) -> GradeResult:
    """Run the judge over one brief and return structured grounding scores.

    `invoker` is an optional callable `(messages) -> response` with a `.content`
    attribute; it defaults to the shared judge LLM's `.invoke`. The offline
    harness passes a retry-wrapped invoker so a transient API error doesn't waste
    a long A/B run; the inline critic uses the default.
    """
    invoke = invoker or (lambda messages: get_judge_llm().invoke(messages))
    findings = invoke([
        SystemMessage(content=JUDGE_SYSTEM),
        HumanMessage(content=judge_user_prompt(source_context, section_block, exec_and_outlook)),
    ]).content

    counts = count_labels(findings)
    total = counts["supported"] + counts["unsupported"] + counts["inference"]
    return GradeResult(
        findings=findings,
        supported=counts["supported"],
        unsupported=counts["unsupported"],
        inference=counts["inference"],
        total=total,
        unsupported_pct=(counts["unsupported"] / total * 100) if total else 0.0,
        inference_claims=extract_claims(findings, "INFERENCE"),
        unsupported_claims=extract_claims(findings, "UNSUPPORTED"),
    )
