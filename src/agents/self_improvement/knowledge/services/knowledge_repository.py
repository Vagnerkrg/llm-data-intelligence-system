from src.agents.self_improvement.knowledge.domain.knowledge_entry import (
    KnowledgeEntry,
)


class KnowledgeRepository:
    """
    Storage abstraction for learned knowledge.
    """

    def __init__(self):
        self._entries: list[KnowledgeEntry] = []

    def save(
        self,
        entry: KnowledgeEntry,
    ) -> None:

        self._entries.append(entry)

    def get_all(
        self,
    ) -> list[KnowledgeEntry]:

        return self._entries.copy()

    def count(
        self,
    ) -> int:

        return len(self._entries)