from src.cognitive.learning.integration.learning_memory_integration import (
    LearningMemoryIntegration,
)

from src.cognitive.learning.knowledge.consolidated_knowledge import (
    ConsolidatedKnowledge,
)

from src.cognitive.learning.knowledge.knowledge_store import (
    KnowledgeStore,
)


def test_learning_memory_integration_store():

    store = KnowledgeStore()

    integration = LearningMemoryIntegration(knowledge_store=store)

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Improve query execution",
        source_pattern="pattern-001",
        confidence=0.95,
    )

    result = integration.store_learning(knowledge)

    assert result["stored"] is True
    assert result["knowledge_id"] == "knowledge-001"


def test_learning_memory_integration_retrieve():

    store = KnowledgeStore()

    integration = LearningMemoryIntegration(knowledge_store=store)

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-002",
        content="Improve decision process",
        source_pattern="pattern-002",
        confidence=0.90,
    )

    integration.store_learning(knowledge)

    recovered = integration.retrieve_learning("knowledge-002")

    assert recovered is not None
    assert recovered.knowledge_id == "knowledge-002"


def test_learning_memory_integration_exists():

    store = KnowledgeStore()

    integration = LearningMemoryIntegration(knowledge_store=store)

    knowledge = ConsolidatedKnowledge(
        knowledge_id="knowledge-003",
        content="Pattern detected",
        source_pattern="pattern-003",
        confidence=0.85,
    )

    integration.store_learning(knowledge)

    assert integration.has_learning("knowledge-003") is True
