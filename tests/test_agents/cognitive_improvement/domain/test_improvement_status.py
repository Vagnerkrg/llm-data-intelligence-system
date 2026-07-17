from src.agents.cognitive_improvement.domain.improvement_status import (
    ImprovementStatus,
)


def test_should_have_expected_status_values():
    assert ImprovementStatus.PENDING is not None
    assert ImprovementStatus.RUNNING is not None
    assert ImprovementStatus.COMPLETED is not None