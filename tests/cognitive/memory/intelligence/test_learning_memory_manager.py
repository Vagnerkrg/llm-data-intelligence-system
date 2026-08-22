from src.cognitive.memory.intelligence.memory_index import MemoryIndex

from src.cognitive.memory.intelligence.learning_memory_manager import (
    LearningMemoryManager,
)


def create_manager():

    index = MemoryIndex()

    return LearningMemoryManager(index)


def test_learning_memory_manager_store():

    manager = create_manager()

    result = manager.store_learning(
        "memory-001", {"topic": "query optimization", "confidence": 0.95}
    )

    assert result["stored"] is True


def test_learning_memory_manager_retrieve():

    manager = create_manager()

    manager.store_learning("memory-001", {"topic": "optimization"})

    knowledge = manager.retrieve_learning("memory-001")

    assert knowledge is not None
    assert knowledge["topic"] == "optimization"


def test_learning_memory_manager_exists():

    manager = create_manager()

    manager.store_learning("memory-001", {"type": "learning"})

    assert manager.has_learning("memory-001")


def test_learning_memory_manager_count():

    manager = create_manager()

    manager.store_learning("memory-001", {})

    manager.store_learning("memory-002", {})

    assert manager.count() == 2
