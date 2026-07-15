from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvaluationContext:
    """
    Immutable context used during self evaluation.

    Represents the execution information
    that will be analyzed.
    """

    execution_id: str

    goal: str

    expected_result: Any

    actual_result: Any

    execution_metrics: dict[str, Any] = field(
        default_factory=dict
    )

    decisions: list[Any] = field(
        default_factory=list
    )

    tools_used: list[str] = field(
        default_factory=list
    )