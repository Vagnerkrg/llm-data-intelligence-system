from src.agents.self_improvement.knowledge.services.knowledge_repository import (
    KnowledgeRepository,
)

from src.agents.self_improvement.knowledge.domain.knowledge_entry import (
    KnowledgeEntry,
)

from src.agents.self_improvement.knowledge.domain.knowledge_type import (
    KnowledgeType,
)


def test_repository_stores_knowledge():

    repository = KnowledgeRepository()

    entry = KnowledgeEntry(
        knowledge_type=KnowledgeType.INSIGHT,
        title="Optimization",
        description="Improve planning strategy",
        confidence=0.9,
    )

    repository.save(entry)

    result = repository.get_all()

    assert len(result) == 1
    assert result[0].title == "Optimization"