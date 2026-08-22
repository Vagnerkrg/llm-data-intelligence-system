from src.cognitive.memory.integration.consolidation_memory_bridge import (
    ConsolidationMemoryBridge,
)


def test_consolidation_memory_bridge_create():

    bridge = ConsolidationMemoryBridge()

    assert bridge is not None


def test_consolidation_memory_bridge_consolidate():

    bridge = ConsolidationMemoryBridge()

    memories = [{"content": "agent improved reasoning", "confidence": 0.9}]

    result = bridge.consolidate(memories)

    assert isinstance(result, list)


def test_consolidation_memory_bridge_count():

    bridge = ConsolidationMemoryBridge()

    assert bridge.count() == 0
