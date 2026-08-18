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
        if not isinstance(entry, KnowledgeEntry):
            raise ValueError(
                "entry must be a KnowledgeEntry."
            )

        if self._contains(entry):
            return

        self._entries.append(entry)

    def replace(
        self,
        existing: KnowledgeEntry,
        replacement: KnowledgeEntry,
    ) -> None:
        if not isinstance(existing, KnowledgeEntry):
            raise ValueError(
                "existing must be a KnowledgeEntry."
            )

        if not isinstance(replacement, KnowledgeEntry):
            raise ValueError(
                "replacement must be a KnowledgeEntry."
            )

        for index, entry in enumerate(self._entries):
            if entry is existing:
                self._entries[index] = replacement
                return

        raise ValueError(
            "existing knowledge entry was not found."
        )

    def get_all(
        self,
    ) -> list[KnowledgeEntry]:
        return self._entries.copy()

    def count(
        self,
    ) -> int:
        return len(self._entries)

    def _contains(
        self,
        candidate: KnowledgeEntry,
    ) -> bool:
        return any(
            self._same_entry(entry, candidate)
            for entry in self._entries
        )

    @staticmethod
    def _same_entry(
        first: KnowledgeEntry,
        second: KnowledgeEntry,
    ) -> bool:
        return (
            first.knowledge_type == second.knowledge_type
            and first.title.strip().casefold()
            == second.title.strip().casefold()
            and first.description.strip().casefold()
            == second.description.strip().casefold()
        )