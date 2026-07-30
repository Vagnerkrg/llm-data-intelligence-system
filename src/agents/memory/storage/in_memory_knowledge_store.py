from typing import Dict, List


from src.agents.memory.domain.cognitive_knowledge import (
    CognitiveKnowledge
)


from src.agents.memory.storage.knowledge_store import (
    KnowledgeStore
)



class InMemoryKnowledgeStore(KnowledgeStore):
    """
    In-memory implementation
    for cognitive knowledge storage.
    """



    def __init__(self):

        self._knowledge: Dict[
            str,
            CognitiveKnowledge
        ] = {}



    def save(
        self,
        knowledge: CognitiveKnowledge
    ):

        self._knowledge[
            knowledge.knowledge_id
        ] = knowledge




    def get(
        self,
        knowledge_id: str
    ):

        return self._knowledge.get(
            knowledge_id
        )




    def delete(
        self,
        knowledge_id: str
    ):

        if knowledge_id in self._knowledge:

            del self._knowledge[
                knowledge_id
            ]

            return True


        return False




    def list_all(
        self
    ) -> List[CognitiveKnowledge]:

        return list(
            self._knowledge.values()
        )