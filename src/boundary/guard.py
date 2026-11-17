"""Safety boundary for traditional-culture knowledge requests.

Call :func:`guard_request` before processing every request. This module does
not make decisions about real-world outcomes and does not provide remedies.
"""

from dataclasses import dataclass
import re

DISCLAIMER = (
    "以上内容为传统文化知识整理与古籍概念解释，不构成任何现实决策、"
    "医疗、法律、投资或人生建议。"
)

# Detect explicit requests for personal outcome judgments or interventions.
_PERSONAL_OUTCOME_PATTERNS = (
    re.compile(r"我.{0,8}(会不会|能不能|是否).{0,8}(发财|离婚|生病|出事|成功|富贵)"),
    re.compile(r"(算命|预测|断命|改运|转运|开运|化解|消灾|招财|保平安)"),
    re.compile(r"(哪个|什么).{0,8}(方位|方向).{0,8}(发财|招财|升职|姻缘)"),
    re.compile(r"(吉凶|命运|运势).{0,8}(如何|怎样|怎么样|好不好|会不会)"),
)
_SENSITIVE_TERMS = re.compile(r"(生辰|出生日期|出生时间|面部照片|住宅平面图)")


@dataclass(frozen=True)
class GuardResult:
    allowed: bool
    reason: str
    safe_alternative: str
    contains_sensitive_data: bool


def guard_request(text: str, *, personalized: bool = False) -> GuardResult:
    """Apply mandatory boundary checks before any retrieval or calculation.

    ``personalized`` is a caller-supplied indication that the request relates
    to an individual. It can add restrictions but cannot bypass text checks.
    Raw request text must not be logged or persisted by callers.
    """
    normalized = re.sub(r"\s+", "", text).lower()
    is_sensitive = bool(_SENSITIVE_TERMS.search(text))
    is_out_of_scope = any(p.search(normalized) for p in _PERSONAL_OUTCOME_PATTERNS)
    if is_out_of_scope or personalized or is_sensitive:
        return GuardResult(
            allowed=False,
            reason=(
                "请求包含敏感个人资料、涉及个人化现实结论，"
                "或超出知识整理范围。"
            ),
            safe_alternative="请移除个人资料；可以改为询问相关传统术语、概念或已收录古籍观点。",
            contains_sensitive_data=is_sensitive,
        )
    return GuardResult(
        allowed=True,
        reason="请求可进入传统文化知识检索。",
        safe_alternative="",
        contains_sensitive_data=is_sensitive,
    )


def append_disclaimer(output: str, *, personalized: bool) -> str:
    """Append the fixed disclaimer to personalized user-facing output."""
    if not personalized or output.rstrip().endswith(DISCLAIMER):
        return output
    return f"{output.rstrip()}\n\n{DISCLAIMER}"
