from src.agents.cognitive_improvement.services.cognitive_improvement_engine import (
    CognitiveImprovementEngine,
)
from src.agents.cognitive_improvement.services.improvement_orchestrator import (
    ImprovementOrchestrator,
)
from src.agents.cognitive_improvement.services.cycle_executor import (
    CycleExecutor,
)
from src.agents.cognitive_improvement.services.improvement_validator import (
    ImprovementValidator,
)


def test_should_build_cognitive_improvement_pipeline():
    engine = CognitiveImprovementEngine()
    orchestrator = ImprovementOrchestrator()
    executor = CycleExecutor()
    validator = ImprovementValidator()

    assert engine is not None
    assert orchestrator is not None
    assert executor is not None
    assert validator is not None