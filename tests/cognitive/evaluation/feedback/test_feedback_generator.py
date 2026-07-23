from src.cognitive.evaluation.feedback.feedback_generator import (
    FeedbackGenerator,
)

from src.cognitive.evaluation.feedback.models.feedback_result import (
    FeedbackResult,
)


def test_feedback_generator():

    generator = FeedbackGenerator()

    feedback = generator.generate(

        {

            "feedback_type": "success",

            "message": "Excellent.",

            "confidence": 0.98,

            "recommendation": "Continue.",

        }

    )

    assert isinstance(

        feedback,

        FeedbackResult,

    )

    assert feedback.feedback_type.value == "success"