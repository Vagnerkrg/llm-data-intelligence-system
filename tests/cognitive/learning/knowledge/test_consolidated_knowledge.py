from src.cognitive.learning.knowledge.consolidated_knowledge import (
    ConsolidatedKnowledge,
)


def test_consolidated_knowledge_creation():

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Melhor estratégia de execução",
        source_pattern="pattern-001",
        confidence=0.6,
    )

    assert knowledge.knowledge_id == "knowledge-001"
    assert knowledge.usage_count == 0


def test_consolidated_knowledge_reinforcement():

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Conhecimento",
        source_pattern="pattern-001",
        confidence=0.6,
    )

    knowledge.reinforce(0.2)

    assert knowledge.confidence == 0.8
    assert knowledge.is_valid()


def test_consolidated_knowledge_usage():

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Conhecimento",
        source_pattern="pattern-001",
        confidence=0.8,
    )

    knowledge.register_usage()

    assert knowledge.usage_count == 1
