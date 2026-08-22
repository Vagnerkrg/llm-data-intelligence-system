from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LearningOutcome:
    """Structured result produced by cognitive learning."""

    experience_id: str
    learned_pattern: str
    knowledge_candidate: str
    confidence: float
    recommendation: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.experience_id.strip():
            raise ValueError("experience_id must not be empty.")

        if not self.learned_pattern.strip():
            raise ValueError("learned_pattern must not be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "learned_pattern": self.learned_pattern,
            "knowledge_candidate": self.knowledge_candidate,
            "confidence": self.confidence,
            "recommendation": self.recommendation,
            "metadata": dict(self.metadata),
        }
