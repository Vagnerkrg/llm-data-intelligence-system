"""Learning analyzer service."""

from ..domain import LearningContext, LearningPattern


class LearningAnalyzer:
    """Analyzes experiences and detects learning patterns."""

    def analyze(
        self,
        context: LearningContext,
    ) -> list[LearningPattern]:
        """Analyze context and extract patterns."""

        patterns: list[LearningPattern] = []

        if context.experiences:
            patterns.append(
                LearningPattern(
                    name="experience_learning_pattern",
                    description=(
                        "Pattern detected from accumulated experiences."
                    ),
                    frequency=len(context.experiences),
                    confidence=0.8,
                )
            )

        return patterns