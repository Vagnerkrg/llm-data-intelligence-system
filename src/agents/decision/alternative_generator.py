from src.agents.decision.decision_alternative import DecisionAlternative
from src.agents.decision.decision_context import DecisionContext


class AlternativeGenerator:
    """
    Generates possible decision alternatives based on context.
    """

    def generate(
        self,
        context: DecisionContext
    ) -> list[DecisionAlternative]:
        """
        Generate candidate alternatives.

        Initial implementation provides deterministic
        alternatives as a foundation for future
        intelligent generation.
        """

        return [
            DecisionAlternative(
                name="analysis_optimization",
                description=f"Analyze goal: {context.goal}",
                expected_outcome="Improved decision quality",
                estimated_cost=0.0,
                confidence=0.5,
                metadata={
                    "generated_by": "alternative_generator"
                }
            )
        ]