from src.agents.self_improvement.evaluation.domain.evaluation_result import (
    EvaluationResult,
)

from .evaluation_interpretation import (
    EvaluationInterpretation,
)


class EvaluationInterpreter:
    """
    Converts evaluation results into cognitive interpretation.
    """


    def interpret(
        self,
        result: EvaluationResult
    ) -> EvaluationInterpretation:


        areas = []


        for signal in result.signals:

            if signal.impact == "high":

                areas.append(
                    signal.signal_type
                )


        requires_improvement = (
            result.score < 0.7
            or len(areas) > 0
        )


        if result.score >= 0.8:

            severity = "low"

        elif result.score >= 0.5:

            severity = "medium"

        else:

            severity = "high"



        return EvaluationInterpretation(

            severity=severity,

            requires_improvement=requires_improvement,

            areas=areas

        )