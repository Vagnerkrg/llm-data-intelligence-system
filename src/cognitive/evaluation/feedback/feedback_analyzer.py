from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)


class FeedbackAnalyzer:
    """
    Analyzes an EvaluationResult and determines
    which type of feedback should be generated.
    """

    def analyze(
        self,
        evaluation: EvaluationResult,
    ) -> dict:

        score = evaluation.score

        if score >= 0.90:

            return {
                "feedback_type": "success",
                "message": "Execution quality is excellent.",
                "recommendation": "Maintain current strategy.",
                "confidence": 0.98,
            }

        if score >= 0.75:

            return {
                "feedback_type": "optimization",
                "message": "Execution is good but can improve.",
                "recommendation": "Optimize reasoning and planning.",
                "confidence": 0.90,
            }

        if score >= 0.50:

            return {
                "feedback_type": "improvement",
                "message": "Execution requires improvement.",
                "recommendation": "Review planning and execution.",
                "confidence": 0.85,
            }

        return {
            "feedback_type": "critical",
            "message": "Execution quality is unacceptable.",
            "recommendation": "Trigger learning cycle.",
            "confidence": 0.99,
        }