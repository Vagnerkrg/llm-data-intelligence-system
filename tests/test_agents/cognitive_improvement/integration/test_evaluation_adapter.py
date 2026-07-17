from src.agents.cognitive_improvement.integration.evaluation_adapter import (
    EvaluationAdapter,
)


def test_should_create_evaluation_adapter():
    adapter = EvaluationAdapter()

    assert adapter is not None