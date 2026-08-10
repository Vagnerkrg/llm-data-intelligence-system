import pytest

from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.metrics.planning_quality import (
    PlanningQualityMetric,
)


def test_should_calculate_planning_quality():
    context = EvaluationContext(
        planning_information={
            "execution_steps": 0.8,
            "step_consistency": 0.9,
            "dependency_resolution": 0.7,
            "plan_completeness": 1.0,
        }
    )

    result = PlanningQualityMetric().evaluate(context)

    assert result.name == "planning_quality"
    assert result.category == "planning"
    assert result.score == pytest.approx(0.85)
    assert result.metadata["factors_evaluated"] == 4
    assert result.metadata["factors_available"] == 4


def test_should_calculate_planning_quality_with_partial_information():
    context = EvaluationContext(
        planning_information={
            "execution_steps": 0.8,
            "step_consistency": None,
            "dependency_resolution": 0.6,
            "plan_completeness": None,
        }
    )

    result = PlanningQualityMetric().evaluate(context)

    assert result.score == pytest.approx(0.7)
    assert result.metadata["factors_evaluated"] == 2


def test_should_return_zero_when_planning_information_is_missing():
    context = EvaluationContext()

    result = PlanningQualityMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Planning information is unavailable."


def test_should_return_zero_for_invalid_planning_information():
    context = EvaluationContext(
        planning_information="invalid"
    )

    result = PlanningQualityMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Invalid planning information."


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (-1.0, 0.0),
        (0.5, 0.5),
        (2.0, 1.0),
        (True, 1.0),
        (False, 0.0),
        ("invalid", None),
        (None, None),
    ],
)
def test_should_normalize_planning_factor(value, expected):
    result = PlanningQualityMetric._normalize_value(value)

    assert result == expected