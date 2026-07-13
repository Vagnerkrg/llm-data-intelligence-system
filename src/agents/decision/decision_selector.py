from uuid import uuid4

from src.agents.decision.decision import Decision
from src.agents.decision.decision_alternative import DecisionAlternative
from src.agents.decision.alternative_evaluation import AlternativeEvaluation
from src.agents.decision.decision_status import DecisionStatus
from src.agents.decision.decision_trace import DecisionTrace


class DecisionSelector:
    """
    Selects the best decision alternative based on evaluations.
    """

    def select(
        self,
        alternatives: list[DecisionAlternative],
        evaluations: list[AlternativeEvaluation]
    ) -> Decision:
        """
        Select highest scored alternative
        and create a cognitive decision.
        """

        best_evaluation = max(
            evaluations,
            key=lambda evaluation: evaluation.score
        )

        selected_alternative = next(
            alternative
            for alternative in alternatives
            if alternative.name == best_evaluation.alternative_id
        )

        decision_id = str(uuid4())

        trace = DecisionTrace(
            decision_id=decision_id,
            alternatives=alternatives
        )

        trace.select_alternative(
            selected_alternative.name
        )

        return Decision(
            decision_id=decision_id,
            status=DecisionStatus.SELECTED,
            strategy=selected_alternative.name,
            trace=trace
        )