from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)

from .feedback_analyzer import FeedbackAnalyzer
from .feedback_generator import FeedbackGenerator

from .models.feedback_result import FeedbackResult


class FeedbackEngine:
    """
    Main orchestration service responsible
    for generating cognitive feedback.
    """

    def __init__(self):

        self.analyzer = FeedbackAnalyzer()

        self.generator = FeedbackGenerator()

    def generate_feedback(
        self,
        evaluation: EvaluationResult,
    ) -> FeedbackResult:

        analysis = self.analyzer.analyze(
            evaluation
        )

        return self.generator.generate(
            analysis
        )