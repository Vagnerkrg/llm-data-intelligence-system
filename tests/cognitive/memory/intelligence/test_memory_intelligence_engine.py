from src.cognitive.memory.intelligence.memory_intelligence_engine import (
    MemoryIntelligenceEngine,
)


def test_memory_intelligence_engine_create():

    engine = MemoryIntelligenceEngine()

    assert engine is not None


def test_memory_intelligence_engine_store():

    engine = MemoryIntelligenceEngine()

    result = engine.store("Agent learned successful pattern")

    assert result is not None


def test_memory_intelligence_engine_count():

    engine = MemoryIntelligenceEngine()

    engine.store("Pattern one")

    engine.store("Pattern two")

    assert engine.count() == 2


def test_memory_intelligence_engine_retrieve():

    engine = MemoryIntelligenceEngine()

    memory_id = engine.store("Decision improvement knowledge")

    result = engine.retrieve(memory_id)

    assert result is not None


def test_memory_intelligence_engine_search():

    engine = MemoryIntelligenceEngine()

    engine.store("Planning optimization pattern")

    result = engine.search("Planning")

    assert len(result) == 1
