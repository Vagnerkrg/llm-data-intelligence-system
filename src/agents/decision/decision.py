from dataclasses import dataclass, field
from datetime import datetime, UTC

from .decision_status import DecisionStatus
from .decision_trace import DecisionTrace


@dataclass(slots=True)
class Decision:
    """
    Represents a cognitive decision produced by an agent.

    A Decision stores the selected strategy,
    execution state and explainability trace.
    """

    decision_id: str
    status: DecisionStatus
    strategy: str
    trace: DecisionTrace

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )