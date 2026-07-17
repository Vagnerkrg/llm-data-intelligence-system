from src.agents.cognitive_improvement.services.cognitive_improvement_engine import (
    CognitiveImprovementEngine,
)


def test_should_create_cognitive_improvement_engine():
    engine = CognitiveImprovementEngine()

    assert engine is not None