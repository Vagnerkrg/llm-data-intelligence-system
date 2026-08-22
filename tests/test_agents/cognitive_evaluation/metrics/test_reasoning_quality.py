import pytest

from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.metrics.reasoning_quality import (
    ReasoningQualityMetric,
)


def test_should_calculate_reasoning_quality():
    context = EvaluationContext(
        reasoning_information={
            "completeness": 0.8,
            "confidence": 0.9,
            "strategy": 0.7,
            "conclusion_quality": 1.0,
        }
    )

    result = ReasoningQualityMetric().evaluate(context)

    assert result.name == "reasoning_quality"
    assert result.category == "reasoning"
    assert result.score == pytest.approx(0.85)
    assert result.metadata["factors_evaluated"] == 4
    assert result.metadata["factors_available"] == 4


def test_should_calculate_reasoning_quality_with_partial_information():
    context = EvaluationContext(
        reasoning_information={
            "completeness": 0.8,
            "confidence": None,
            "strategy": 0.6,
            "conclusion_quality": None,
        }
    )

    result = ReasoningQualityMetric().evaluate(context)

    assert result.score == pytest.approx(0.7)
    assert result.metadata["factors_evaluated"] == 2
    assert result.metadata["factors_available"] == 4


def test_should_return_zero_when_reasoning_information_is_missing():
    context = EvaluationContext()

    result = ReasoningQualityMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Reasoning information is unavailable."


def test_should_return_zero_for_invalid_reasoning_information():
    context = EvaluationContext(reasoning_information="invalid")

    result = ReasoningQualityMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Invalid reasoning information."


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
def test_should_normalize_reasoning_factor(value, expected):
    result = ReasoningQualityMetric._normalize_value(value)

    assert result == expected
