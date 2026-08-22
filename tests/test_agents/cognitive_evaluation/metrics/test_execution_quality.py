import pytest

from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.metrics.execution_quality import (
    ExecutionQualityMetric,
)


def test_should_calculate_execution_quality():
    context = EvaluationContext(
        execution_result={
            "execution_status": "completed",
            "completed_steps": 0.8,
            "failed_steps": 0.1,
            "execution_efficiency": 0.9,
        }
    )

    result = ExecutionQualityMetric().evaluate(context)

    assert result.name == "execution_quality"
    assert result.category == "execution"
    assert result.score == pytest.approx(0.9)
    assert result.metadata["factors_evaluated"] == 4


def test_should_convert_failed_steps_into_quality_score():
    context = EvaluationContext(
        execution_result={
            "failed_steps": 0.2,
        }
    )

    result = ExecutionQualityMetric().evaluate(context)

    assert result.score == pytest.approx(0.8)


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("completed", 1.0),
        ("success", 1.0),
        ("successful", 1.0),
        ("succeeded", 1.0),
        ("partial", 0.5),
        ("partially_completed", 0.5),
        ("in_progress", 0.5),
        ("failed", 0.0),
        ("error", 0.0),
        ("cancelled", 0.0),
        ("canceled", 0.0),
        (True, 1.0),
        (False, 0.0),
        (None, None),
        ("unknown", None),
    ],
)
def test_should_normalize_execution_status(status, expected):
    result = ExecutionQualityMetric._status_score(status)

    assert result == expected


def test_should_return_zero_when_execution_information_is_missing():
    context = EvaluationContext()

    result = ExecutionQualityMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Execution information is unavailable."


def test_should_return_zero_for_invalid_execution_information():
    context = EvaluationContext(execution_result="invalid")

    result = ExecutionQualityMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Invalid execution information."


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
def test_should_normalize_execution_value(value, expected):
    result = ExecutionQualityMetric._normalize_value(value)

    assert result == expected
