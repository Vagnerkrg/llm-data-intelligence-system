from src.agents.self_improvement.reflection.domain import ReflectionFinding


class InsightGenerator:
    """
    Generates insights from hypotheses.
    """

    def __init__(self):
        pass

    def generate(self, hypothesis):
        """
        Generate insight from hypothesis.

        Supports:
        - dictionary hypotheses
        - ReflectionFinding objects
        """

        if isinstance(hypothesis, dict):

            return ReflectionFinding(
                title=hypothesis.get(
                    "title",
                    "Generated Insight",
                ),
                description=hypothesis.get(
                    "description",
                    "",
                ),
                confidence=hypothesis.get(
                    "confidence",
                    0.0,
                ),
                reflection_type="insight",
            )


        if isinstance(hypothesis, ReflectionFinding):

            return ReflectionFinding(
                title=hypothesis.title,
                description=(
                    f"Insight generated from "
                    f"{hypothesis.description}"
                ),
                confidence=hypothesis.confidence,
                reflection_type="insight",
            )


        return ReflectionFinding(
            title="Unknown Insight",
            description="No hypothesis available.",
            confidence=0.0,
            reflection_type="insight",
        )