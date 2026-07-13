from src.agents.decision.alternative_evaluation import AlternativeEvaluation


class ConfidenceAnalyzer:
    """
    Calculates overall confidence for a decision process.
    """

    def calculate(
        self,
        evaluations: list[AlternativeEvaluation]
    ) -> float:
        """
        Calculate confidence based on the
        highest evaluated alternative.
        """

        if not evaluations:
            return 0.0

        return max(
            evaluation.confidence
            for evaluation in evaluations
        )