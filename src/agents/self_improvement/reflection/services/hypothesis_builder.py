from src.agents.self_improvement.reflection.domain import ReflectionFinding


class HypothesisBuilder:
    """
    Builds hypotheses from reflection findings.
    """

    def __init__(self):
        pass

    def build(self, pattern):
        """
        Generate a hypothesis from a pattern.

        Supports dictionary based patterns
        and ReflectionFinding objects.
        """

        if isinstance(pattern, dict):
            return ReflectionFinding(
                title=pattern.get(
                    "type",
                    "Generated Hypothesis",
                ),
                description=pattern.get(
                    "description",
                    "",
                ),
                confidence=0.8,
                reflection_type="hypothesis",
            )

        if isinstance(pattern, ReflectionFinding):
            return ReflectionFinding(
                title=pattern.title,
                description=(
                    f"Hypothesis generated from "
                    f"{pattern.title}"
                ),
                confidence=pattern.confidence,
                reflection_type="hypothesis",
            )

        return ReflectionFinding(
            title="Unknown Hypothesis",
            description="No pattern information available.",
            confidence=0.0,
            reflection_type="hypothesis",
        )