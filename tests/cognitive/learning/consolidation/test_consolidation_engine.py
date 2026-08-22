from src.cognitive.learning.consolidation.consolidation_engine import (
    ConsolidationEngine,
)

from src.cognitive.learning.knowledge.knowledge_store import KnowledgeStore

from src.cognitive.learning.patterns.learning_pattern import LearningPattern


def test_consolidation_engine_creates_knowledge():

    store = KnowledgeStore()

    engine = ConsolidationEngine(store)

    pattern = LearningPattern(
        pattern_id="pattern-001",
        description="Melhor estratégia encontrada",
        frequency=5,
        confidence=0.8,
        metadata={},
    )

    knowledge = engine.consolidate(pattern)

    assert knowledge is not None
    assert knowledge.source_pattern == "pattern-001"
    assert store.count() == 1


def test_consolidation_engine_rejects_low_confidence():

    store = KnowledgeStore()

    engine = ConsolidationEngine(store)

    pattern = LearningPattern(
        pattern_id="pattern-002",
        description="Padrão fraco",
        frequency=1,
        confidence=0.4,
        metadata={},
    )

    knowledge = engine.consolidate(pattern)

    assert knowledge is None
    assert store.count() == 0


def test_consolidation_engine_checks_existing():

    store = KnowledgeStore()

    engine = ConsolidationEngine(store)

    pattern = LearningPattern(
        pattern_id="pattern-003",
        description="Conhecimento válido",
        frequency=3,
        confidence=0.9,
        metadata={},
    )

    engine.consolidate(pattern)

    assert engine.exists("pattern-003")
