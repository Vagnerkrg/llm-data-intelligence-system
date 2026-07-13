from src.agents.decision.decision import Decision


class DecisionExplainer:
    """
    Generates human-readable explanations
    for cognitive decisions.
    """

    def explain(
        self,
        decision: Decision,
        confidence: float
    ) -> str:
        """
        Explain why a decision was selected.
        """

        selected_alternative = (
            decision.trace.selected_alternative_id
        )

        return (
            f"Decision strategy: {decision.strategy}\n"
            f"Selected alternative: {selected_alternative}\n"
            f"Confidence: {confidence}"
        )