from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LearningExperience:
    """Structured experience entering the cognitive learning layer."""

    experience_id: str
    source: str
    signal_type: str
    pattern: str
    outcome: str
    confidence: float
    impact: str
    metadata: dict[str, Any] = field(default_factory=dict)
