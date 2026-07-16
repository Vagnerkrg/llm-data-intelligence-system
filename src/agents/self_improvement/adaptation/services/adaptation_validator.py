from src.agents.self_improvement.adaptation.domain.adaptation_action import (
    AdaptationAction,
)


class AdaptationValidator:
    """
    Validates adaptation actions before execution.
    """

    VALID_PRIORITIES = {
        "low",
        "medium",
        "high",
    }

    def validate(
        self,
        action: AdaptationAction,
    ) -> bool:

        if not action.target.strip():
            return False

        if not action.description.strip():
            return False

        if action.priority not in self.VALID_PRIORITIES:
            return False

        if action.adaptation_type is None:
            return False

        return True