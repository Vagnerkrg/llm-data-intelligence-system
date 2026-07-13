from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(slots=True)
class Observation:
    """
    Represents an operational observation produced during
    or after an agent execution.

    Stores execution signals that can later be analyzed
    by the reflection layer.
    """

    observation_id: str
    context_id: str
    execution_id: str

    observation_type: str
    state: str

    metrics: dict[str, float] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )