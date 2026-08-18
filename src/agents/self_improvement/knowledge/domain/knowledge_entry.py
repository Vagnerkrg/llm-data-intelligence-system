from dataclasses import dataclass, field
from typing import Any

from src.agents.self_improvement.knowledge.domain.knowledge_type import (
    KnowledgeType,
)


@dataclass
class KnowledgeEntry:
    """
    Represents consolidated knowledge generated
    from evaluation and learning experiences.
    """

    knowledge_type: KnowledgeType

    title: str

    description: str

    confidence: float

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty.")

        if not self.description.strip():
            raise ValueError("description must not be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "knowledge_type": self.knowledge_type.value,
            "title": self.title,
            "description": self.description,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }