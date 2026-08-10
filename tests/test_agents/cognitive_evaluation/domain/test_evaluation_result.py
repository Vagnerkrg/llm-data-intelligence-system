import pytest

from src.agents.cognitive_evaluation.domain.evaluation_metric import (
    EvaluationMetric,
)
from src.agents.cognitive_evaluation.domain.evaluation_result import (
    EvaluationResult,
)


def test_should_create_evaluation_result():
    result = EvaluationResult(
        overall_score=0.82,
        status="completed",
    )

    assert result.overall_score == 0.82
    assert result.metrics == []
    assert result.status == "completed"
    assert result.metadata == {}


def test_should_use_default_values():
    result = EvaluationResult()

    assert result.overall_score == 0.0
    assert result.metrics == []
    assert result.status == "pending"
    assert result.metadata == {}


def test_should_add_metric():
    result = EvaluationResult()

    metric = EvaluationMetric(
        name="reasoning_quality",
        category="reasoning",
        score=0.85,
    )

    result.add_metric(metric)

    assert len(result.metrics) == 1
    assert result.metrics[0] is metric


def test_should_reject_invalid_metric_type():
    result = EvaluationResult()

    with pytest.raises(
        TypeError,
        match="metric must be an EvaluationMetric instance",
    ):
        result.add_metric("invalid")


def test_should_serialize_result():
    metric = EvaluationMetric(
        name="reasoning_quality",
        category="reasoning",
        score=0.85,
    )

    result = EvaluationResult(
        overall_score=0.85,
        metrics=[metric],
        status="completed",
        metadata={"agent_id": "agent-001"},
    )

    data = result.to_dict()

    assert data == {
        "overall_score": 0.85,
        "metrics": [
            {
                "name": "reasoning_quality",
                "category": "reasoning",
                "score": 0.85,
                "metadata": {},
                "description": "",
            }
        ],
        "status": "completed",
        "metadata": {"agent_id": "agent-001"},
    }


def test_should_reject_invalid_overall_score():
    with pytest.raises(
        ValueError,
        match="Overall score must be between 0.0 and 1.0",
    ):
        EvaluationResult(overall_score=1.5)


def test_should_reject_empty_status():
    with pytest.raises(
        ValueError,
        match="Evaluation status cannot be empty",
    ):
        EvaluationResult(status="")