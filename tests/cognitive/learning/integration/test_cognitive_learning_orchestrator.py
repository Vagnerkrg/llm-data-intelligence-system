from src.cognitive.learning.integration.cognitive_learning_orchestrator import (
    CognitiveLearningOrchestrator,
)

from src.cognitive.learning.patterns.pattern_detector import PatternDetector

from src.cognitive.learning.consolidation.consolidation_engine import (
    ConsolidationEngine,
)

from src.cognitive.learning.knowledge.knowledge_store import KnowledgeStore


def create_orchestrator():

    knowledge_store = KnowledgeStore()

    return CognitiveLearningOrchestrator(
        pattern_detector=PatternDetector(),
        consolidation_engine=ConsolidationEngine(knowledge_store=knowledge_store),
        knowledge_store=knowledge_store,
    )


def test_cognitive_learning_orchestrator_learns():

    orchestrator = create_orchestrator()

    feedback = {
        "type": "performance",
        "description": "Query execution improved",
        "impact": "high",
        "confidence": 0.95,
    }

    result = orchestrator.process_learning(feedback)

    assert result["learned"] is True
    assert "knowledge_id" in result


def test_cognitive_learning_orchestrator_rejects_invalid_learning():

    orchestrator = create_orchestrator()

    feedback = {
        "type": "unknown",
        "description": "",
        "impact": "low",
        "confidence": 0.1,
    }

    result = orchestrator.process_learning(feedback)

    assert result["learned"] is False
