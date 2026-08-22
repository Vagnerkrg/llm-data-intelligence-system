import pytest

from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.metrics.memory_effectiveness import (
    MemoryEffectivenessMetric,
)


def test_should_calculate_memory_effectiveness():
    context = EvaluationContext(
        memory_information={
            "memory_usage": 0.8,
            "relevance_score": 0.9,
            "retrieved_context_quality": 0.7,
            "memory_contribution": 1.0,
        }
    )

    result = MemoryEffectivenessMetric().evaluate(context)

    assert result.name == "memory_effectiveness"
    assert result.category == "memory"
    assert result.score == pytest.approx(0.85)
    assert result.metadata["factors_evaluated"] == 4
    assert result.metadata["factors_available"] == 4


def test_should_calculate_memory_effectiveness_with_partial_information():
    context = EvaluationContext(
        memory_information={
            "memory_usage": 0.8,
            "relevance_score": None,
            "retrieved_context_quality": 0.6,
            "memory_contribution": None,
        }
    )

    result = MemoryEffectivenessMetric().evaluate(context)

    assert result.score == pytest.approx(0.7)
    assert result.metadata["factors_evaluated"] == 2


def test_should_return_zero_when_memory_information_is_missing():
    context = EvaluationContext()

    result = MemoryEffectivenessMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Memory information is unavailable."


def test_should_return_zero_for_invalid_memory_information():
    context = EvaluationContext(memory_information="invalid")

    result = MemoryEffectivenessMetric().evaluate(context)

    assert result.score == 0.0
    assert result.description == "Invalid memory information."


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
def test_should_normalize_memory_factor(value, expected):
    result = MemoryEffectivenessMetric._normalize_value(value)

    assert result == expected
