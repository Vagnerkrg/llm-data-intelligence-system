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

    def __post_init__(self) -> None:
        if not self.experience_id.strip():
            raise ValueError("experience_id must not be empty.")

        if not self.source.strip():
            raise ValueError("source must not be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "source": self.source,
            "signal_type": self.signal_type,
            "pattern": self.pattern,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "impact": self.impact,
            "metadata": dict(self.metadata),
        }

