from src.cognitive.memory.integration.learning_memory_bridge import (
    LearningMemoryBridge
)

from src.cognitive.memory.intelligence.learning_memory_manager import (
    LearningMemoryManager
)

from src.cognitive.learning.knowledge.consolidated_knowledge import (
    ConsolidatedKnowledge
)


def create_bridge():

    manager = LearningMemoryManager()

    return LearningMemoryBridge(
        memory_manager=manager
    )


def create_knowledge():

    return ConsolidatedKnowledge(
        knowledge_id="knowledge-001",
        content="Improve query execution",
        source_pattern="pattern-001",
        confidence=0.95
    )


def test_learning_memory_bridge_store():

    bridge = create_bridge()

    knowledge = create_knowledge()


    result = bridge.store_learning(
        knowledge
    )


    assert result["stored"] is True
    assert result["knowledge_id"] == "knowledge-001"



def test_learning_memory_bridge_retrieve():

    bridge = create_bridge()

    knowledge = create_knowledge()


    bridge.store_learning(
        knowledge
    )


    result = bridge.retrieve_learning(
        "knowledge-001"
    )


    assert result is not None
    assert result.content == "Improve query execution"



def test_learning_memory_bridge_exists():

    bridge = create_bridge()

    knowledge = create_knowledge()


    bridge.store_learning(
        knowledge
    )


    assert bridge.exists(
        "knowledge-001"
    )



def test_learning_memory_bridge_count():

    bridge = create_bridge()

    knowledge = create_knowledge()


    bridge.store_learning(
        knowledge
    )


    assert bridge.count() == 1