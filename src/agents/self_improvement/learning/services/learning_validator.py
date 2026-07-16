"""Learning validator service."""


class LearningValidator:
    """Validates learning results."""

    def validate(self, outcomes) -> bool:
        """Validate learning input."""

        if isinstance(outcomes, bool):
            return outcomes

        if not outcomes:
            return False

        return all(
            getattr(outcome, "confidence", 0) >= 0.0
            for outcome in outcomes
        )