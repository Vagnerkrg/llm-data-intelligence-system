from src.agents.memory.domain.cognitive_knowledge import (
    CognitiveKnowledge
)

from src.agents.memory.storage.in_memory_knowledge_store import (
    InMemoryKnowledgeStore
)



def test_save_knowledge():

    store = InMemoryKnowledgeStore()

    knowledge = CognitiveKnowledge(
        knowledge_id="knowledge_001",
        description="Repeated customer payment delays",
        source_patterns=[
            "pattern_001"
        ],
        confidence=0.8
    )


    store.save(
        knowledge
    )


    result = store.get(
        "knowledge_001"
    )


    assert result is not None

    assert result.description == (
        "Repeated customer payment delays"
    )



def test_list_all_knowledge():

    store = InMemoryKnowledgeStore()


    knowledge = CognitiveKnowledge(
        knowledge_id="knowledge_002",
        description="Recurring payment behavior"
    )


    store.save(
        knowledge
    )


    items = store.list_all()


    assert len(items) == 1

    assert items[0].knowledge_id == (
        "knowledge_002"
    )



def test_delete_knowledge():

    store = InMemoryKnowledgeStore()


    knowledge = CognitiveKnowledge(
        knowledge_id="knowledge_003",
        description="Test knowledge"
    )


    store.save(
        knowledge
    )


    deleted = store.delete(
        "knowledge_003"
    )


    assert deleted is True

    assert store.get(
        "knowledge_003"
    ) is None