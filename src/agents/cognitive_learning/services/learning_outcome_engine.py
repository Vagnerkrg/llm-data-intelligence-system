from collections.abc import Sequence
from numbers import Real
from typing import Any

from src.agents.cognitive_learning.domain import (
    LearningExperience,
    LearningOutcome,
)


class LearningOutcomeEngine:
    """
    Transforms cognitive learning experiences into structured outcomes.

    The engine evaluates the quality and completeness of learning
    experiences, identifies the learned pattern, classifies the type
    of learning, calculates confidence, and produces deterministic
    learning outcomes.

    The engine does not mutate experiences or execute recommendations.
    """

    MIN_CONFIDENCE = 0.0
    MAX_CONFIDENCE = 1.0

    VALID_IMPACTS = {
        "low",
        "medium",
        "high",
    }

    EFFECTIVE_IMPACTS = {
        "high",
        "medium",
    }

    INEFFECTIVE_PATTERNS = {
        "ineffective",
        "failure",
        "failed",
        "error",
        "poor",
        "weak",
        "unsuccessful",
    }

    def evaluate(
        self,
        experiences: Sequence[LearningExperience],
    ) -> list[LearningOutcome]:
        """
        Transform valid learning experiences into learning outcomes.

        Invalid or incomplete experiences are ignored.
        Processing order is preserved and deterministic.
        """

        outcomes: list[LearningOutcome] = []

        for experience in experiences:
            if not self._is_valid_experience(experience):
                continue

            outcome = self._build_outcome(experience)

            if outcome is not None:
                outcomes.append(outcome)

        return outcomes

    def _build_outcome(
        self,
        experience: LearningExperience,
    ) -> LearningOutcome | None:
        pattern = self._normalize_text(experience.pattern)

        signal_type = self._normalize_text(experience.signal_type)

        if not pattern or not signal_type:
            return None

        confidence = self._calculate_confidence(experience)

        learning_type = self._classify_learning(experience)

        learned_pattern = self._build_learned_pattern(
            learning_type=learning_type,
            pattern=pattern,
        )

        knowledge_candidate = f"{signal_type}: {learned_pattern}"

        recommendation = self._build_recommendation(
            learning_type=learning_type,
            experience=experience,
        )

        return LearningOutcome(
            experience_id=experience.experience_id,
            learned_pattern=learned_pattern,
            knowledge_candidate=knowledge_candidate,
            confidence=confidence,
            recommendation=recommendation,
            metadata={
                "learning_type": learning_type,
                "impact": experience.impact,
                "source": experience.source,
            },
        )

    @classmethod
    def _is_valid_experience(
        cls,
        experience: Any,
    ) -> bool:
        if not isinstance(
            experience,
            LearningExperience,
        ):
            return False

        if not cls._normalize_text(experience.experience_id):
            return False

        if not cls._normalize_text(experience.signal_type):
            return False

        if not cls._normalize_text(experience.pattern):
            return False

        if not cls._normalize_text(experience.source):
            return False

        if not cls._normalize_text(experience.impact):
            return False

        return cls._is_valid_confidence(experience.confidence)

    @classmethod
    def _is_valid_confidence(
        cls,
        confidence: Any,
    ) -> bool:
        if isinstance(confidence, bool):
            return False

        if not isinstance(confidence, Real):
            return False

        numeric = float(confidence)

        return cls.MIN_CONFIDENCE <= numeric <= cls.MAX_CONFIDENCE

    @classmethod
    def _calculate_confidence(
        cls,
        experience: LearningExperience,
    ) -> float:
        """
        Calculate learning confidence deterministically.

        High-impact learning keeps the original confidence.
        Medium-impact learning keeps 90% of the confidence.
        Low-impact learning keeps 75% of the confidence.
        """

        confidence = float(experience.confidence)

        impact = cls._normalize_text(experience.impact).lower()

        if impact == "high":
            factor = 1.0
        elif impact == "medium":
            factor = 0.90
        else:
            factor = 0.75

        return round(
            confidence * factor,
            4,
        )

    @classmethod
    def _classify_learning(
        cls,
        experience: LearningExperience,
    ) -> str:
        """
        Classify the learning represented by an experience.
        """

        pattern = cls._normalize_text(experience.pattern).lower()

        if any(marker in pattern for marker in cls.INEFFECTIVE_PATTERNS):
            return "ineffective_behavior"

        impact = cls._normalize_text(experience.impact).lower()

        if impact in cls.EFFECTIVE_IMPACTS:
            return "effective_behavior"

        return "improvement_opportunity"

    @staticmethod
    def _build_learned_pattern(
        learning_type: str,
        pattern: str,
    ) -> str:
        prefixes = {
            "effective_behavior": "effective",
            "ineffective_behavior": "ineffective",
            "improvement_opportunity": "improvement",
        }

        prefix = prefixes[learning_type]

        return f"{prefix}: {pattern}"

    @staticmethod
    def _build_recommendation(
        learning_type: str,
        experience: LearningExperience,
    ) -> str:
        if learning_type == "effective_behavior":
            return "Reinforce this behavior in future executions."

        if learning_type == "ineffective_behavior":
            return "Avoid repeating this behavior and evaluate alternative strategies."

        return "Monitor this pattern and evaluate opportunities for improvement."

    @staticmethod
    def _normalize_text(
        value: Any,
    ) -> str:
        if not isinstance(value, str):
            return ""

        return value.strip()
