"""Mock-only four-pillars adapter; values are fixtures, not a real chart."""

import json
from datetime import datetime
from typing import Any

RULESET = "mock-fixture-v1"


def calculate_birth_chart(birth_time: datetime) -> dict[str, Any]:
    """Return a deterministic, structured mock response.

    The timestamp is validated but deliberately not used to infer pillars.
    No LLM participates in or may modify this output. This fixture must not
    be presented as an actual calculation.
    """
    if not isinstance(birth_time, datetime):
        raise TypeError("birth_time must be datetime")
    return {
        "status": "mock_only",
        "ruleset": RULESET,
        "input_used": False,
        "pillars": {
            "year": {"stem": "甲", "branch": "子"},
            "month": {"stem": "丙", "branch": "寅"},
            "day": {"stem": "戊", "branch": "辰"},
            "hour": {"stem": "壬", "branch": "戌"},
        },
        "ten_gods": {
            "year_stem": "七杀",
            "month_stem": "偏印",
            "hour_stem": "偏财",
        },
        "notice": "固定测试样例，不代表依据输入时间计算的结果。",
    }


def calculate_birth_chart_json(birth_time: datetime) -> str:
    """Serialize the adapter output as stable JSON for an API boundary."""
    return json.dumps(
        calculate_birth_chart(birth_time), ensure_ascii=False, sort_keys=True
    )
