from typing import Optional

from ..patterns.learning_pattern import LearningPattern
from ..knowledge.consolidated_knowledge import ConsolidatedKnowledge
from ..knowledge.knowledge_store import KnowledgeStore


class ConsolidationEngine:
    """
    Responsável por transformar padrões aprendidos
    em conhecimento consolidado reutilizável.
    """

    def __init__(self, knowledge_store: KnowledgeStore):
        self.knowledge_store = knowledge_store

    def consolidate(self, pattern: LearningPattern) -> Optional[ConsolidatedKnowledge]:
        """
        Consolida um padrão em conhecimento.

        Padrões com baixa confiança não são consolidados.
        """

        if not pattern.is_reliable():
            return None

        knowledge = ConsolidatedKnowledge(
            knowledge_id=f"knowledge-{pattern.pattern_id}",
            content=pattern.description,
            source_pattern=pattern.pattern_id,
            confidence=pattern.confidence,
            metadata=pattern.metadata,
        )

        self.knowledge_store.save(knowledge)

        return knowledge

    def exists(self, pattern_id: str) -> bool:
        """
        Verifica se um padrão já gerou conhecimento.
        """

        return self.knowledge_store.exists(f"knowledge-{pattern_id}")
