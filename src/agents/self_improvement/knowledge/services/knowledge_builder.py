from src.agents.self_improvement.knowledge.domain.knowledge_entry import (
    KnowledgeEntry,
)


class KnowledgeBuilder:
    """
    Builds structured knowledge entries from learning signals.
    """

    def build(
        self,
        signal: dict,
    ) -> KnowledgeEntry:

        return KnowledgeEntry(
            knowledge_type=signal.get(
                "type",
                "pattern",
            ),
            title=signal.get(
                "title",
                signal.get("pattern"),
            ),
            description=signal.get(
                "description",
                signal.get("recommendation"),
            ),
            confidence=signal.get(
                "confidence",
                0.0,
            ),
        )