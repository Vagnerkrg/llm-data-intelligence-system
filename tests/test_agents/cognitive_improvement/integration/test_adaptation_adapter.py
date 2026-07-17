from src.agents.cognitive_improvement.integration.adaptation_adapter import (
    AdaptationAdapter,
)


def test_should_create_adaptation_adapter():
    adapter = AdaptationAdapter()

    assert adapter is not None