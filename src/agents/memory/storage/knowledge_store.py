from abc import ABC, abstractmethod

from src.agents.memory.domain.cognitive_knowledge import CognitiveKnowledge


class KnowledgeStore(ABC):
    """
    Contract for cognitive knowledge persistence.
    """

    @abstractmethod
    def save(self, knowledge: CognitiveKnowledge):
        pass

    @abstractmethod
    def get(self, knowledge_id: str):
        pass

    @abstractmethod
    def delete(self, knowledge_id: str):
        pass

    @abstractmethod
    def list_all(self):
        pass
