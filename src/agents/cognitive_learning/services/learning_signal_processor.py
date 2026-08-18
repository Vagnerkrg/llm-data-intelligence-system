from collections.abc import Sequence
from uuid import uuid4

from src.agents.cognitive_learning.domain import LearningExperience


class LearningSignalProcessor:
    """Transforms cognitive signals into structured learning experiences."""

    def process(
        self,
        signals: Sequence,
    ) -> list[LearningExperience]:
        experiences: list[LearningExperience] = []

        for signal in signals:
            signal_type = getattr(signal, "signal_type", None)
            pattern = getattr(signal, "pattern", None)
            confidence = getattr(signal, "confidence", 0.0)
            impact = getattr(signal, "impact", "unknown")

            if not signal_type or not pattern:
                continue

            experiences.append(
                LearningExperience(
                    experience_id=str(uuid4()),
                    source="cognitive_evaluation",
                    signal_type=str(signal_type),
                    pattern=str(pattern),
                    outcome="observed",
                    confidence=float(confidence),
                    impact=str(impact),
                )
            )

        return experiences
