from src.cognitive.evaluation.feedback.feedback_analyzer import (
    FeedbackAnalyzer,
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)


def build_result(score: float) -> EvaluationResult:

    return EvaluationResult(
        score=score,
        passed=score >= 0.80,
        evaluator="feedback",
    )


def test_feedback_analyzer_success():

    analyzer = FeedbackAnalyzer()

    analysis = analyzer.analyze(
        build_result(0.95)
    )

    assert analysis["feedback_type"] == "success"

    assert analysis["confidence"] > 0.9


def test_feedback_analyzer_critical():

    analyzer = FeedbackAnalyzer()

    analysis = analyzer.analyze(
        build_result(0.20)
    )

    assert analysis["feedback_type"] == "critical"

    assert analysis["confidence"] > 0.9