"""Learning extractor service."""

from ..domain import (
    LearningExperience,
    LearningOutcome,
)


class LearningExtractor:
    """Extracts learning outcomes from experiences."""

    def extract(
        self,
        experiences: list[LearningExperience],
    ) -> list[LearningOutcome]:
        """Generate learning outcomes."""

        outcomes: list[LearningOutcome] = []

        for experience in experiences:
            outcomes.append(
                LearningOutcome(
                    improvement=experience.description,
                    confidence=experience.confidence,
                    success=experience.success,
                    improvement_detected=experience.success,
                    impact=experience.outcome,
                )
            )

        return outcomes