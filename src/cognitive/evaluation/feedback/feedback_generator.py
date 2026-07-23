from uuid import uuid4

from .models.feedback_result import FeedbackResult
from .models.feedback_type import FeedbackType


class FeedbackGenerator:
    """
    Generates structured feedback objects.
    """

    def generate(
        self,
        analysis: dict,
    ) -> FeedbackResult:

        return FeedbackResult(

            feedback_id=str(uuid4()),

            feedback_type=FeedbackType(
                analysis["feedback_type"]
            ),

            message=analysis["message"],

            confidence=analysis["confidence"],

            recommendation=analysis["recommendation"],

            source="CognitiveEvaluationSystem",

            metadata={},
        )