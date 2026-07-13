from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(slots=True)
class AutonomyDecision:
    """
    Represents the decision that controls whether
    a behavioral adaptation should be applied.

    Provides governance, confidence and traceability
    for autonomous changes.
    """

    decision_id: str

    context_id: str

    strategy_id: str

    reason: str

    confidence: float = 0.0

    approval_required: bool = False

    status: str = "PENDING"

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )