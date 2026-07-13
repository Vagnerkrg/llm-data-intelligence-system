from src.agents.decision.alternative_evaluation import AlternativeEvaluation
from src.agents.decision.decision_alternative import DecisionAlternative
from src.agents.decision.decision_context import DecisionContext


class AlternativeEvaluator:
    """
    Evaluates decision alternatives.
    """

    def evaluate(
        self,
        alternatives: list[DecisionAlternative],
        context: DecisionContext
    ) -> list[AlternativeEvaluation]:

        evaluations = []

        for alternative in alternatives:

            evaluations.append(
                AlternativeEvaluation(
                    alternative_id=alternative.name,
                    score=0.5,
                    confidence=alternative.confidence,
                    risk_level="low",
                    evaluation_reason=(
                        "Initial rule based evaluation"
                    )
                )
            )

        return evaluations