from src.agents.self_improvement.evaluation.domain.evaluation_result import (
    EvaluationResult,
)


def test_evaluation_result_creation():

    result = EvaluationResult(
        evaluation_id="eval-001",
        score=0.9,
        quality_level="high",
    )

    assert result.evaluation_id == "eval-001"
    assert result.score == 0.9
    assert result.quality_level == "high"


def test_evaluation_result_default_lists():

    result = EvaluationResult(
        evaluation_id="eval-002",
        score=1.0,
        quality_level="high",
    )

    assert result.findings == []
    assert result.signals == []