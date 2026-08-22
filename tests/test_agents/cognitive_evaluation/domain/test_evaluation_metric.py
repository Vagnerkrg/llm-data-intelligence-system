import pytest

from src.agents.cognitive_evaluation.domain.evaluation_metric import (
    EvaluationMetric,
)


def test_should_create_evaluation_metric():
    metric = EvaluationMetric(
        name="reasoning_quality",
        category="reasoning",
        score=0.85,
        description="Measures reasoning quality.",
    )

    assert metric.name == "reasoning_quality"
    assert metric.category == "reasoning"
    assert metric.score == 0.85
    assert metric.description == "Measures reasoning quality."
    assert metric.metadata == {}


def test_should_use_default_values():
    metric = EvaluationMetric(
        name="reasoning_quality",
        category="reasoning",
    )

    assert metric.score == 0.0
    assert metric.metadata == {}
    assert metric.description == ""


def test_should_serialize_metric():
    metric = EvaluationMetric(
        name="reasoning_quality",
        category="reasoning",
        score=0.85,
        metadata={"source": "agent"},
        description="Measures reasoning quality.",
    )

    data = metric.to_dict()

    assert data == {
        "name": "reasoning_quality",
        "category": "reasoning",
        "score": 0.85,
        "metadata": {"source": "agent"},
        "description": "Measures reasoning quality.",
    }


def test_should_reject_empty_metric_name():
    with pytest.raises(ValueError, match="Metric name cannot be empty"):
        EvaluationMetric(
            name="",
            category="reasoning",
        )


def test_should_reject_empty_metric_category():
    with pytest.raises(
        ValueError,
        match="Metric category cannot be empty",
    ):
        EvaluationMetric(
            name="reasoning_quality",
            category="",
        )


@pytest.mark.parametrize("score", [-0.1, 1.1])
def test_should_reject_invalid_score(score):
    with pytest.raises(
        ValueError,
        match="Metric score must be between 0.0 and 1.0",
    ):
        EvaluationMetric(
            name="reasoning_quality",
            category="reasoning",
            score=score,
        )
