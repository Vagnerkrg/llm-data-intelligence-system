from src.agents.cognitive_improvement.integration.reflection_adapter import (
    ReflectionAdapter,
)


def test_should_create_reflection_adapter():
    adapter = ReflectionAdapter()

    assert adapter is not None