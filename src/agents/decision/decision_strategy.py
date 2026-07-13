from dataclasses import dataclass

from .decision_alternative import DecisionAlternative


@dataclass(slots=True)
class DecisionStrategy:
    """
    Defines how an agent selects an alternative.

    This abstraction allows different decision
    policies to be implemented in the future.
    """

    def select(
        self,
        alternatives: list[DecisionAlternative],
    ) -> DecisionAlternative:
        """
        Select the best available alternative.

        Current policy:
        choose the alternative with highest confidence.
        """

        if not alternatives:
            raise ValueError(
                "At least one alternative is required."
            )

        return max(
            alternatives,
            key=lambda alternative: alternative.confidence,
        )