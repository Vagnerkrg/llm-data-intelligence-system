from src.cognitive.learning.knowledge.knowledge_store import (
    KnowledgeStore
)

from src.cognitive.learning.knowledge.consolidated_knowledge import (
    ConsolidatedKnowledge
)


def test_knowledge_store_save():

    store = KnowledgeStore()

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Estratégia otimizada",
        source_pattern="pattern-001",
        confidence=0.8
    )

    store.save(knowledge)

    assert store.count() == 1



def test_knowledge_store_get():

    store = KnowledgeStore()

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Conhecimento",
        source_pattern="pattern-001",
        confidence=0.8
    )

    store.save(knowledge)

    result = store.get(
        "knowledge-001"
    )

    assert result is not None
    assert result.content == "Conhecimento"



def test_knowledge_store_list():

    store = KnowledgeStore()

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Conhecimento",
        source_pattern="pattern-001",
        confidence=0.8
    )

    store.save(knowledge)

    items = store.list_all()

    assert len(items) == 1
    assert items[0].knowledge_id == "knowledge-001"



def test_knowledge_store_exists():

    store = KnowledgeStore()

    assert not store.exists(
        "missing"
    )

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Conhecimento",
        source_pattern="pattern-001",
        confidence=0.8
    )

    store.save(knowledge)

    assert store.exists(
        "knowledge-001"
    )