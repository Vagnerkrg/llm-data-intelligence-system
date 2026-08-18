from collections.abc import Sequence

from src.agents.cognitive_learning.domain import (
    LearningExperience,
    LearningOutcome,
)


class LearningOutcomeEngine:
    """Derives deterministic learning outcomes from experiences."""

    def evaluate(
        self,
        experiences: Sequence[LearningExperience],
    ) -> list[LearningOutcome]:
        outcomes: list[LearningOutcome] = []

        for experience in experiences:
            outcomes.append(
                LearningOutcome(
                    experience_id=experience.experience_id,
                    learned_pattern=experience.pattern,
                    knowledge_candidate=(
                        f"{experience.signal_type}: "
                        f"{experience.pattern}"
                    ),
                    confidence=experience.confidence,
                    recommendation=self._recommend(experience),
                )
            )

        return outcomes

    @staticmethod
    def _recommend(
        experience: LearningExperience,
    ) -> str:
        if experience.impact == "high":
            return (
                "Prioritize this pattern in future evolution decisions."
            )

        if experience.impact == "medium":
            return (
                "Consider this pattern during future optimization."
            )

        return "Monitor this pattern in future executions."
