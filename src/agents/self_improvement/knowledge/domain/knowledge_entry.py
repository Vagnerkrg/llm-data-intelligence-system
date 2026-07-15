from dataclasses import dataclass

from src.agents.self_improvement.knowledge.domain.knowledge_type import (
    KnowledgeType,
)


@dataclass
class KnowledgeEntry:
    """
    Represents consolidated knowledge generated
    from evaluation experiences.
    """

    knowledge_type: KnowledgeType

    title: str

    description: str

    confidence: float