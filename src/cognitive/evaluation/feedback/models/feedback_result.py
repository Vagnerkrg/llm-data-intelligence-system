from dataclasses import dataclass, field
from typing import Any

from .feedback_type import FeedbackType


@dataclass(frozen=True)
class FeedbackResult:
    """
    Final feedback produced by the
    Cognitive Feedback Engine.
    """

    feedback_id: str

    feedback_type: FeedbackType

    message: str

    confidence: float

    recommendation: str

    source: str

    metadata: dict[str, Any] = field(
        default_factory=dict
    )