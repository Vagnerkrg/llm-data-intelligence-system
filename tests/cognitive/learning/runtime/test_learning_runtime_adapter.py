from src.cognitive.learning.runtime.learning_runtime_adapter import (
    LearningRuntimeAdapter,
)


from src.cognitive.learning.integration.cognitive_learning_orchestrator import (
    CognitiveLearningOrchestrator,
)


from src.cognitive.learning.patterns.pattern_detector import PatternDetector


from src.cognitive.learning.consolidation.consolidation_engine import (
    ConsolidationEngine,
)


from src.cognitive.learning.knowledge.knowledge_store import KnowledgeStore


def create_adapter():

    store = KnowledgeStore()

    orchestrator = CognitiveLearningOrchestrator(
        pattern_detector=PatternDetector(),
        consolidation_engine=ConsolidationEngine(store),
        knowledge_store=store,
    )

    return LearningRuntimeAdapter(orchestrator)


def test_learning_runtime_adapter_process():

    adapter = create_adapter()

    context = adapter.process_feedback(
        "execution-001",
        {
            "type": "performance",
            "description": "Improved execution",
            "impact": "high",
            "confidence": 0.95,
        },
    )

    assert context.execution_id == ("execution-001")

    assert context.learned is True


def test_learning_runtime_adapter_invalid():

    adapter = create_adapter()

    context = adapter.process_feedback(
        "execution-002", {"type": "unknown", "description": "", "confidence": 0.1}
    )

    assert context.learned is False
