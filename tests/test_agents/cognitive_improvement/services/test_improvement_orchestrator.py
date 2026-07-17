from src.agents.cognitive_improvement.services.improvement_orchestrator import (
    ImprovementOrchestrator,
)


def test_should_create_improvement_orchestrator():
    orchestrator = ImprovementOrchestrator()

    assert orchestrator is not None