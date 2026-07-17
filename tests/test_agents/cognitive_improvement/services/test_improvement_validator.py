from src.agents.cognitive_improvement.services.improvement_validator import (
    ImprovementValidator,
)


def test_should_create_improvement_validator():
    validator = ImprovementValidator()

    assert validator is not None