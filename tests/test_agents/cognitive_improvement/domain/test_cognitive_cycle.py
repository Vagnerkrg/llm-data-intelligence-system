from src.agents.cognitive_improvement.domain.cognitive_cycle import (
    CognitiveCycle,
)


def test_should_create_cognitive_cycle():
    cycle = CognitiveCycle.EVALUATION

    assert cycle is not None
    assert cycle.value == "evaluation"