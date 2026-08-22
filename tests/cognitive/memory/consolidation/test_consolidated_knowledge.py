from src.cognitive.memory.consolidation.consolidated_knowledge import (
    ConsolidatedKnowledge,
)


def create_knowledge():

    return ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Improve query execution",
        source_pattern="pattern-001",
        confidence=0.95,
    )


def test_consolidated_knowledge_create():

    knowledge = create_knowledge()

    assert knowledge.knowledge_id == "knowledge-001"

    assert knowledge.content == ("Improve query execution")


def test_consolidated_knowledge_usage():

    knowledge = create_knowledge()

    assert knowledge.usage_count == 0

    knowledge.increase_usage()

    assert knowledge.usage_count == 1


def test_consolidated_knowledge_confidence():

    knowledge = create_knowledge()

    assert knowledge.is_reliable()

    knowledge.update_confidence(0.5)

    assert not knowledge.is_reliable()


def test_consolidated_knowledge_metadata():

    knowledge = create_knowledge()

    knowledge.add_metadata("domain", "memory")

    assert knowledge.metadata["domain"] == "memory"
