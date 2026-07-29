from typing import Dict, List, Optional

from .consolidated_knowledge import ConsolidatedKnowledge


class KnowledgeStore:
    """
    Armazena conhecimentos consolidados
    gerados pelo ciclo de aprendizado.
    """

    def __init__(self):
        self._knowledge: Dict[str, ConsolidatedKnowledge] = {}


    def save(
        self,
        knowledge: ConsolidatedKnowledge
    ) -> None:
        """
        Persiste um conhecimento.
        """

        self._knowledge[
            knowledge.knowledge_id
        ] = knowledge


    def get(
        self,
        knowledge_id: str
    ) -> Optional[ConsolidatedKnowledge]:
        """
        Recupera conhecimento pelo identificador.
        """

        return self._knowledge.get(
            knowledge_id
        )


    def exists(
        self,
        knowledge_id: str
    ) -> bool:
        """
        Verifica existência do conhecimento.
        """

        return knowledge_id in self._knowledge


    def list_all(
        self
    ) -> List[ConsolidatedKnowledge]:
        """
        Retorna todos os conhecimentos armazenados.
        """

        return list(
            self._knowledge.values()
        )


    def count(self) -> int:
        """
        Retorna quantidade de conhecimentos.
        """

        return len(
            self._knowledge
        )