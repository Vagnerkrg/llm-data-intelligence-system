from typing import List, Dict, Any

from src.cognitive.memory.consolidation.consolidated_knowledge import (
    ConsolidatedKnowledge,
)


class KnowledgeConsolidator:
    """
    Consolida conhecimentos extraídos
    em conhecimento cognitivo reutilizável.
    """

    def __init__(self, confidence_threshold: float = 0.5):

        self.confidence_threshold = confidence_threshold

        self.knowledge_store = []

    def consolidate(
        self, candidates: List[Dict[str, Any]]
    ) -> List[ConsolidatedKnowledge]:
        """
        Consolida candidatos aprovados.

        Apenas conhecimentos acima do
        threshold são persistidos.
        """

        consolidated = []

        for candidate in candidates:
            confidence = candidate.get("confidence", 0.0)

            if confidence < self.confidence_threshold:
                continue

            knowledge = ConsolidatedKnowledge(
                knowledge_id=self._generate_id(candidate),
                content=candidate.get("content", ""),
                source_pattern=candidate.get("source_pattern", "unknown"),
                confidence=confidence,
                metadata=candidate.get("metadata", {}),
            )

            consolidated.append(knowledge)

        self.knowledge_store.extend(consolidated)

        return consolidated

    def _generate_id(self, candidate: Dict[str, Any]) -> str:
        """
        Gera identificador único lógico.
        """

        source = candidate.get("source_pattern", "unknown")

        return f"knowledge-{source}"

    def count(self) -> int:
        """
        Retorna quantidade de conhecimentos
        consolidados.
        """

        return len(self.knowledge_store)

    def get_all(self) -> List[ConsolidatedKnowledge]:
        """
        Retorna conhecimentos armazenados.
        """

        return self.knowledge_store
