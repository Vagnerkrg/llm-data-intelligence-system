from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Any

from src.agents.autonomous_evolution.domain.optimization_pattern import (
    OptimizationPattern,
)
from src.agents.autonomous_evolution.domain.optimization_signal import (
    OptimizationSignal,
)
from src.agents.autonomous_evolution.domain.experience_optimization_context import (
    ExperienceOptimizationContext,
)


class ExperienceDrivenOptimizer:
    """
    Analyzes accumulated agent experiences and produces deterministic
    optimization signals.

    The optimizer detects recurring patterns but does not directly
    change strategies, execute adaptations, or mutate runtime state.
    """

    DEFAULT_MIN_EXPERIENCES = 2
    DEFAULT_MIN_CONFIDENCE = 0.60
    DEFAULT_EFFECTIVE_THRESHOLD = 0.75
    DEFAULT_INEFFECTIVE_THRESHOLD = 0.45

    def __init__(
        self,
        min_experiences: int = DEFAULT_MIN_EXPERIENCES,
        min_confidence: float = DEFAULT_MIN_CONFIDENCE,
        effective_threshold: float = DEFAULT_EFFECTIVE_THRESHOLD,
        ineffective_threshold: float = DEFAULT_INEFFECTIVE_THRESHOLD,
    ) -> None:
        self._validate_configuration(
            min_experiences=min_experiences,
            min_confidence=min_confidence,
            effective_threshold=effective_threshold,
            ineffective_threshold=ineffective_threshold,
        )

        self.min_experiences = min_experiences
        self.min_confidence = min_confidence
        self.effective_threshold = effective_threshold
        self.ineffective_threshold = ineffective_threshold

    def optimize(
        self,
        context: ExperienceOptimizationContext,
    ) -> list[OptimizationSignal]:
        """
        Analyze past experiences and produce optimization signals.
        """

        if not isinstance(
            context,
            ExperienceOptimizationContext,
        ):
            raise TypeError(
                "context must be an ExperienceOptimizationContext instance."
            )

        if len(context.execution_history) < self.min_experiences:
            return []

        patterns = self.detect_patterns(context)

        return self.generate_signals(patterns)

    def detect_patterns(
        self,
        context: ExperienceOptimizationContext,
    ) -> list[OptimizationPattern]:
        """
        Detect recurring effective and ineffective execution patterns.
        """

        scores = self._extract_scores(context.execution_history)

        if len(scores) < self.min_experiences:
            return []

        average_score = sum(score for score, _ in scores) / len(scores)

        average_confidence = sum(confidence for _, confidence in scores) / len(scores)

        strategies = self._extract_strategies(context.execution_history)

        strategy_name = strategies[0] if len(set(strategies)) == 1 else None

        patterns: list[OptimizationPattern] = []

        if (
            average_score >= self.effective_threshold
            and average_confidence >= self.min_confidence
        ):
            patterns.append(
                OptimizationPattern(
                    name="effective_execution_pattern",
                    category="strategy",
                    occurrence_count=len(scores),
                    average_score=average_score,
                    average_confidence=average_confidence,
                    strategy=strategy_name,
                    evidence=[item for item in context.execution_history],
                )
            )

        elif (
            average_score <= self.ineffective_threshold
            and average_confidence >= self.min_confidence
        ):
            patterns.append(
                OptimizationPattern(
                    name="ineffective_execution_pattern",
                    category="strategy",
                    occurrence_count=len(scores),
                    average_score=average_score,
                    average_confidence=average_confidence,
                    strategy=strategy_name,
                    evidence=[item for item in context.execution_history],
                )
            )

        return patterns

    def generate_signals(
        self,
        patterns: list[OptimizationPattern],
    ) -> list[OptimizationSignal]:
        """
        Convert detected patterns into deterministic optimization signals.
        """

        signals: list[OptimizationSignal] = []

        for pattern in patterns:
            if (
                pattern.category == "strategy"
                and pattern.name == "effective_execution_pattern"
            ):
                signals.append(
                    OptimizationSignal(
                        signal_type="strategy_preference",
                        target=pattern.strategy or "execution_strategy",
                        direction="reinforce",
                        strength=pattern.average_score,
                        confidence=pattern.average_confidence,
                        reason=(
                            "Repeated execution outcomes indicate that "
                            "the observed strategy is effective."
                        ),
                        supporting_patterns=[pattern.name],
                    )
                )

            elif (
                pattern.category == "strategy"
                and pattern.name == "ineffective_execution_pattern"
            ):
                signals.append(
                    OptimizationSignal(
                        signal_type="strategy_preference",
                        target=pattern.strategy or "execution_strategy",
                        direction="avoid",
                        strength=1.0 - pattern.average_score,
                        confidence=pattern.average_confidence,
                        reason=(
                            "Repeated execution outcomes indicate that "
                            "the observed strategy is ineffective."
                        ),
                        supporting_patterns=[pattern.name],
                    )
                )

        return signals

    @staticmethod
    def _extract_scores(
        experiences: list[Any],
    ) -> list[tuple[float, float]]:
        results: list[tuple[float, float]] = []

        for experience in experiences:
            score = ExperienceDrivenOptimizer._extract_score(experience)

            if score is None:
                continue

            confidence = ExperienceDrivenOptimizer._extract_confidence(experience)

            results.append(
                (
                    score,
                    confidence,
                )
            )

        return results

    @staticmethod
    def _extract_score(
        value: Any,
    ) -> float | None:
        if isinstance(value, bool):
            return None

        if isinstance(value, Real):
            numeric = float(value)

            if 0.0 <= numeric <= 1.0:
                return numeric

            return None

        if isinstance(value, Mapping):
            for key in (
                "overall_score",
                "score",
                "quality_score",
                "performance_score",
            ):
                candidate = value.get(key)

                if isinstance(candidate, Real) and not isinstance(
                    candidate,
                    bool,
                ):
                    numeric = float(candidate)

                    if 0.0 <= numeric <= 1.0:
                        return numeric

        for attribute_name in (
            "overall_score",
            "score",
            "quality_score",
            "performance_score",
        ):
            candidate = getattr(
                value,
                attribute_name,
                None,
            )

            if isinstance(candidate, Real) and not isinstance(
                candidate,
                bool,
            ):
                numeric = float(candidate)

                if 0.0 <= numeric <= 1.0:
                    return numeric

        return None

    @staticmethod
    def _extract_confidence(
        value: Any,
    ) -> float:
        if isinstance(value, Mapping):
            candidate = value.get(
                "confidence",
                1.0,
            )
        else:
            candidate = getattr(
                value,
                "confidence",
                1.0,
            )

        if isinstance(candidate, bool):
            return 1.0

        if isinstance(candidate, Real):
            numeric = float(candidate)

            if 0.0 <= numeric <= 1.0:
                return numeric

        return 0.0

    @staticmethod
    def _extract_strategies(
        experiences: Sequence[Any],
    ) -> list[str]:
        strategies: list[str] = []

        for experience in experiences:
            strategy: Any = None

            if isinstance(experience, Mapping):
                strategy = experience.get("strategy")
            else:
                strategy = getattr(
                    experience,
                    "strategy",
                    None,
                )

            if (
                isinstance(
                    strategy,
                    str,
                )
                and strategy.strip()
            ):
                strategies.append(strategy.strip())

        return strategies

    @staticmethod
    def _validate_configuration(
        min_experiences: int,
        min_confidence: float,
        effective_threshold: float,
        ineffective_threshold: float,
    ) -> None:
        if min_experiences < 1:
            raise ValueError("min_experiences must be greater than or equal to 1.")

        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError("min_confidence must be between 0.0 and 1.0.")

        if not 0.0 <= ineffective_threshold <= 1.0:
            raise ValueError("ineffective_threshold must be between 0.0 and 1.0.")

        if not 0.0 <= effective_threshold <= 1.0:
            raise ValueError("effective_threshold must be between 0.0 and 1.0.")

        if ineffective_threshold >= effective_threshold:
            raise ValueError(
                "ineffective_threshold must be lower than effective_threshold."
            )
