from src.cognitive.evaluation.feedback.feedback_engine import (
    FeedbackEngine,
)

from src.cognitive.evaluation.feedback.models.feedback_result import (
    FeedbackResult,
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)


def test_feedback_engine_generates_feedback():

    evaluation = EvaluationResult(

        score=0.92,

        passed=True,

        evaluator="feedback",

    )

    engine = FeedbackEngine()

    result = engine.generate_feedback(
        evaluation
    )

    assert isinstance(
        result,
        FeedbackResult,
    )

    assert result.feedback_type.value == "success"

    assert result.confidence > 0