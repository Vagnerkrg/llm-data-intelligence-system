from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LearningInsight:
    """Structured insight extracted from learning signals."""

    insight_id: str
    pattern: str
    explanation: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.insight_id.strip():
            raise ValueError("insight_id must not be empty.")

        if not self.pattern.strip():
            raise ValueError("pattern must not be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "insight_id": self.insight_id,
            "pattern": self.pattern,
            "explanation": self.explanation,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }
