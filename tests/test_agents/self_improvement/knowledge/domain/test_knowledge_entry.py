from src.agents.self_improvement.knowledge.domain.knowledge_entry import (
    KnowledgeEntry,
)

from src.agents.self_improvement.knowledge.domain.knowledge_type import (
    KnowledgeType,
)


def test_knowledge_entry_creation():

    entry = KnowledgeEntry(
        knowledge_type=KnowledgeType.INSIGHT,
        title="Execution improvement",
        description="Tool selection can be optimized",
        confidence=0.85,
    )

    assert entry.knowledge_type == KnowledgeType.INSIGHT
    assert entry.title == "Execution improvement"
    assert entry.description == "Tool selection can be optimized"
    assert entry.confidence == 0.85