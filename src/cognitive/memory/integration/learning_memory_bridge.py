from typing import Dict, Any, Optional

from src.cognitive.memory.intelligence.learning_memory_manager import (
    LearningMemoryManager
)

from src.cognitive.learning.knowledge.consolidated_knowledge import (
    ConsolidatedKnowledge
)


class LearningMemoryBridge:
    """
    Ponte entre o sistema de aprendizagem
    e a memória cognitiva.

    Responsável por transformar conhecimento
    consolidado em memória persistente.
    """

    def __init__(
        self,
        memory_manager: LearningMemoryManager
    ):
        self.memory_manager = memory_manager

        self._knowledge_cache: Dict[
            str,
            ConsolidatedKnowledge
        ] = {}


    def store_learning(
        self,
        knowledge: ConsolidatedKnowledge
    ) -> Dict[str, Any]:
        """
        Armazena conhecimento aprendido na memória.
        """

        self.memory_manager.store(
            knowledge.knowledge_id,
            knowledge.content
        )

        self._knowledge_cache[
            knowledge.knowledge_id
        ] = knowledge


        return {
            "stored": True,
            "knowledge_id": knowledge.knowledge_id
        }



    def retrieve_learning(
        self,
        knowledge_id: str
    ) -> Optional[ConsolidatedKnowledge]:
        """
        Recupera conhecimento completo.
        """

        if not self.memory_manager.exists(
            knowledge_id
        ):
            return None


        return self._knowledge_cache.get(
            knowledge_id
        )



    def exists(
        self,
        knowledge_id: str
    ) -> bool:
        """
        Verifica existência.
        """

        return self.memory_manager.exists(
            knowledge_id
        )



    def count(self) -> int:
        """
        Quantidade de conhecimentos armazenados.
        """

        return self.memory_manager.count()