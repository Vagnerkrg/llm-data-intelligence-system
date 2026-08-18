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
