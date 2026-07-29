from typing import Dict, Any

from ..knowledge.consolidated_knowledge import ConsolidatedKnowledge
from ..knowledge.knowledge_store import KnowledgeStore


class LearningMemoryIntegration:
    """
    Integration layer between cognitive learning
    and persistent knowledge memory.
    """

    def __init__(
        self,
        knowledge_store: KnowledgeStore
    ):
        self.knowledge_store = knowledge_store


    def store_learning(
        self,
        knowledge: ConsolidatedKnowledge
    ) -> Dict[str, Any]:
        """
        Stores consolidated learning into memory.
        """

        self.knowledge_store.save(
            knowledge
        )

        return {
            "stored": True,
            "knowledge_id": knowledge.knowledge_id,
            "source_pattern": knowledge.source_pattern
        }


    def retrieve_learning(
        self,
        knowledge_id: str
    ) -> ConsolidatedKnowledge | None:
        """
        Retrieves consolidated knowledge.
        """

        return self.knowledge_store.get(
            knowledge_id
        )


    def has_learning(
        self,
        knowledge_id: str
    ) -> bool:
        """
        Checks if learning exists.
        """

        return self.knowledge_store.exists(
            knowledge_id
        )