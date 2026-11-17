"""Single request entry point; all request handling passes the boundary."""

from dataclasses import dataclass
from typing import Callable

from boundary.guard import DISCLAIMER, append_disclaimer, guard_request


@dataclass(frozen=True)
class Response:
    status: str
    text: str
    personalized: bool
    citations: tuple[str, ...] = ()


def handle_request(
    text: str,
    *,
    personalized: bool = False,
    knowledge_handler: Callable[[str], str] | None = None,
) -> Response:
    """Apply the non-optional safety gate before invoking knowledge handling.

    The handler receives only allowed requests. This minimal entry point does
    not call an LLM, perform retrieval, or persist request data.
    """
    decision = guard_request(text, personalized=personalized)
    if not decision.allowed:
        refusal = f"{decision.reason} {decision.safe_alternative}"
        return Response(
            status="refused",
            text=append_disclaimer(refusal, personalized=personalized),
            personalized=personalized,
        )

    answer = knowledge_handler(text) if knowledge_handler else "当前仅支持传统文化概念说明。"
    return Response(
        status="ok",
        text=append_disclaimer(answer, personalized=personalized),
        personalized=personalized,
    )


def validated_citation(chunk_id: str, known_chunk_ids: set[str]) -> str:
    """Return a citation id only when it exists in the loaded source set."""
    if not chunk_id or chunk_id not in known_chunk_ids:
        raise ValueError("引用缺少有效 chunk_id")
    return chunk_id
