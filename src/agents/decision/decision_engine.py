from dataclasses import dataclass

from .decision import Decision
from .decision_alternative import DecisionAlternative
from .decision_context import DecisionContext
from .decision_reason import DecisionReason
from .decision_status import DecisionStatus
from .decision_strategy import DecisionStrategy
from .decision_trace import DecisionTrace


@dataclass(slots=True)
class DecisionEngine:
    """
    Responsible for producing cognitive decisions.

    The DecisionEngine connects context, strategies,
    alternatives and reasoning into an explainable decision flow.
    """

    def decide(
        self,
        context: DecisionContext,
        strategy: DecisionStrategy,
        alternatives: list[DecisionAlternative],
    ) -> Decision:
        """
        Creates a decision based on available context
        and selected strategy.
        """

        selected = strategy.select(alternatives)

        reason = DecisionReason(
            justification=(
                f"Selected strategy '{selected.name}' "
                "based on evaluation criteria."
            ),
            confidence=selected.confidence,
            evidence=[
                context.objective
            ],
        )

        trace = DecisionTrace(
            decision_id=context.request_id
        )

        trace.add_reason(reason)
        trace.add_alternative(selected)

        trace.select_alternative(
            selected.name
        )

        return Decision(
            decision_id=context.request_id,
            status=DecisionStatus.COMPLETED,
            strategy=selected.name,
            trace=trace,
        )