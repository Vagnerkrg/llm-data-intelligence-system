from src.agents.self_improvement.knowledge.services.knowledge_builder import (
    KnowledgeBuilder,
)

from src.agents.self_improvement.knowledge.services.knowledge_repository import (
    KnowledgeRepository,
)


class KnowledgeManager:
    """
    Coordinates knowledge creation and storage.
    """

    def __init__(
        self,
        repository=None,
        builder=None,
    ):

        self.repository = (
            repository
            if repository
            else KnowledgeRepository()
        )

        self.builder = (
            builder
            if builder
            else KnowledgeBuilder()
        )

    def process(
        self,
        learning_signal: dict,
    ):

        knowledge = self.builder.build(
            learning_signal
        )

        self.repository.save(
            knowledge
        )

        return knowledge

    def list_knowledge(self):

        return self.repository.get_all()

    def size(self):

        return self.repository.count()