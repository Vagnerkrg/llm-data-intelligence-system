from src.cognitive.learning.services.learning_consolidation_service import (
    LearningConsolidationService
)

from src.cognitive.learning.consolidation.consolidation_engine import (
    ConsolidationEngine
)

from src.cognitive.learning.knowledge.knowledge_store import (
    KnowledgeStore
)

from src.cognitive.learning.patterns.learning_pattern import (
    LearningPattern
)


def test_learning_consolidation_service_process():

    store = KnowledgeStore()

    engine = ConsolidationEngine(
        store
    )

    service = LearningConsolidationService(
        engine
    )


    pattern = LearningPattern(
        pattern_id="pattern-service",
        description="Aprendizado consolidado",
        frequency=5,
        confidence=0.9,
        metadata={}
    )


    result = service.process(
        pattern
    )


    assert result is not None
    assert store.count() == 1



def test_learning_consolidation_service_rejects_pattern():

    store = KnowledgeStore()

    engine = ConsolidationEngine(
        store
    )

    service = LearningConsolidationService(
        engine
    )


    pattern = LearningPattern(
        pattern_id="weak-pattern",
        description="Baixa confiança",
        frequency=1,
        confidence=0.3,
        metadata={}
    )


    result = service.process(
        pattern
    )


    assert result is None
    assert store.count() == 0



def test_learning_service_can_consolidate():

    store = KnowledgeStore()

    engine = ConsolidationEngine(
        store
    )

    service = LearningConsolidationService(
        engine
    )


    pattern = LearningPattern(
        pattern_id="valid-pattern",
        description="Padrão válido",
        frequency=4,
        confidence=0.8,
        metadata={}
    )


    assert service.can_consolidate(
        pattern
    )