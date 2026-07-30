from src.cognitive.evaluation.models.evaluation_result import EvaluationResult


def test_evaluation_result_creation():

    result = EvaluationResult(
        score=0.95,
        passed=True,
        evaluator="reasoning_evaluator"
    )

    assert result.score == 0.95
    assert result.passed is True
    assert result.evaluator == "reasoning_evaluator"


def test_evaluation_result_details():

    result = EvaluationResult(
        score=0.80,
        passed=True,
        evaluator="memory_evaluator"
    )

    result.add_detail(
        "latency",
        120
    )

    assert result.details["latency"] == 120


def test_evaluation_result_success():

    result = EvaluationResult(
        score=0.90,
        passed=True,
        evaluator="planner_evaluator"
    )

    assert result.is_successful() is True


def test_evaluation_result_failure():

    result = EvaluationResult(
        score=0.90,
        passed=False,
        evaluator="planner_evaluator"
    )

    assert result.is_successful() is False