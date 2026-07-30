from src.cognitive.evaluation.intelligence.evaluation_interpretation import (
    EvaluationInterpretation,
)

from .evaluation_decision import (
    EvaluationDecision,
)


class EvaluationDecisionEngine:
    """
    Converts cognitive interpretation into action decisions.
    """


    def decide(
        self,
        interpretation: EvaluationInterpretation
    ) -> EvaluationDecision:


        if interpretation.requires_improvement:

            action = "adapt"

        else:

            action = "maintain"



        if interpretation.severity == "high":

            priority = "high"

        elif interpretation.severity == "medium":

            priority = "medium"

        else:

            priority = "low"



        target = (
            interpretation.areas[0]
            if interpretation.areas
            else "general"
        )


        return EvaluationDecision(
            action=action,
            priority=priority,
            target=target,
        )