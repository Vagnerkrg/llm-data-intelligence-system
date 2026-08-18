from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LearningSignal:
    """Normalized signal entering cognitive learning."""

    signal_id: str
    signal_type: str
    pattern: str
    confidence: float
    impact: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.signal_id.strip():
            raise ValueError("signal_id must not be empty.")

        if not self.signal_type.strip():
            raise ValueError("signal_type must not be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "signal_type": self.signal_type,
            "pattern": self.pattern,
            "confidence": self.confidence,
            "impact": self.impact,
            "metadata": dict(self.metadata),
        }

