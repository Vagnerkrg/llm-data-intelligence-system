from dataclasses import dataclass

from .decision import Decision
from .decision_context import DecisionContext
from .decision_engine import DecisionEngine
from .decision_strategy import DecisionStrategy
from .decision_alternative import DecisionAlternative


@dataclass(slots=True)
class DecisionIntegration:
    """
    Integration layer between agent runtime
    and cognitive decision capabilities.
    """

    engine: DecisionEngine

    def evaluate(
        self,
        context: DecisionContext,
        strategy: DecisionStrategy,
        alternatives: list[DecisionAlternative],
    ) -> Decision:
        """
        Executes the decision process and returns
        an explainable decision object.
        """

        return self.engine.decide(
            context=context,
            strategy=strategy,
            alternatives=alternatives,
        )