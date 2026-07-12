from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ExecutionFeedback:
    """
    Represents the evaluation feedback
    generated after an execution analysis.
    """

    success: bool

    message: str

    issues: List[str] = field(
        default_factory=list
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )