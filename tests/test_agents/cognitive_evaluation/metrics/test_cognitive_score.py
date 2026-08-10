import pytest

from src.agents.cognitive_evaluation.domain.evaluation_metric import (
    EvaluationMetric,
)
from src.agents.cognitive_evaluation.metrics.cognitive_score import (
    CognitiveScoreCalculator,
)


def test_should_calculate_consolidated_cognitive_score():
    metrics = [
        EvaluationMetric(
            name="reasoning_quality",
            category="reasoning",
            score=0.8,
        ),
        EvaluationMetric(
            name="planning_quality",
            category="planning",
            score=0.9,
        ),
        EvaluationMetric(
            name="execution_quality",
            category="execution",
            score=0.7,
        ),
        EvaluationMetric(
            name="memory_effectiveness",
            category="memory",
            score=1.0,
        ),
    ]

    result = CognitiveScoreCalculator().calculate(metrics)

    assert result.name == "cognitive_score"
    assert result.category == "cognitive"
    assert result.score == pytest.approx(0.85)
    assert result.metadata["metrics_evaluated"] == 4
    assert result.metadata["metric_names"] == [
        "reasoning_quality",
        "planning_quality",
        "execution_quality",
        "memory_effectiveness",
    ]


def test_should_return_zero_when_no_metrics_are_available():
    result = CognitiveScoreCalculator().calculate([])

    assert result.score == 0.0
    assert result.metadata["metrics_evaluated"] == 0
    assert result.description == "No cognitive metrics available."


def test_should_calculate_score_with_single_metric():
    metric = EvaluationMetric(
        name="reasoning_quality",
        category="reasoning",
        score=0.75,
    )

    result = CognitiveScoreCalculator().calculate([metric])

    assert result.score == pytest.approx(0.75)
    assert result.metadata["metrics_evaluated"] == 1


def test_should_accept_any_iterable_of_metrics():
    metrics = (
        EvaluationMetric(
            name="reasoning_quality",
            category="reasoning",
            score=0.6,
        ),
        EvaluationMetric(
            name="planning_quality",
            category="planning",
            score=0.8,
        ),
    )

    result = CognitiveScoreCalculator().calculate(iter(metrics))

    assert result.score == pytest.approx(0.7)
    assert result.metadata["metrics_evaluated"] == 2


def test_should_reject_invalid_metric_type():
    with pytest.raises(
        TypeError,
        match="All metrics must be EvaluationMetric instances",
    ):
        CognitiveScoreCalculator().calculate(
            [
                EvaluationMetric(
                    name="valid_metric",
                    category="test",
                    score=0.8,
                ),
                "invalid",
            ]
        )


def test_should_produce_deterministic_results():
    metrics = [
        EvaluationMetric(
            name="reasoning_quality",
            category="reasoning",
            score=0.8,
        ),
        EvaluationMetric(
            name="planning_quality",
            category="planning",
            score=0.6,
        ),
    ]

    calculator = CognitiveScoreCalculator()

    first = calculator.calculate(metrics)
    second = calculator.calculate(metrics)

    assert first.to_dict() == second.to_dict()