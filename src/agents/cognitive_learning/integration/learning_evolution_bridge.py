from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from src.agents.autonomous_evolution.domain.evolution_context import (
    EvolutionContext,
)
from src.agents.autonomous_evolution.domain.evolution_decision import (
    EvolutionDecision,
)
from src.agents.autonomous_evolution.domain.optimization_signal import (
    OptimizationSignal,
)
from src.agents.autonomous_evolution.services.evolution_decision_engine import (
    EvolutionDecisionEngine,
)
from src.agents.cognitive_learning.domain.learning_outcome import (
    LearningOutcome,
)
from src.agents.self_improvement.evaluation.domain.learning_signal import (
    LearningSignal,
)


@dataclass(frozen=True)
class LearningEvolutionResult:
    """Result of integrating learning information with evolution."""

    context: EvolutionContext
    decision: EvolutionDecision
    learning_evidence_count: int
    optimization_signal_count: int

    @property
    def should_evolve(self) -> bool:
        return self.decision.should_evolve


class LearningEvolutionBridge:
    """
    Integrates Cognitive Learning with Autonomous Evolution.

    The bridge converts learning outcomes, learning signals, and
    optimization signals into generic EvolutionContext information.
    The EvolutionDecisionEngine remains independent from learning.
    """

    def __init__(
        self,
        evolution_decision_engine: EvolutionDecisionEngine | None = None,
    ) -> None:
        self.evolution_decision_engine = (
            evolution_decision_engine
            if evolution_decision_engine is not None
            else EvolutionDecisionEngine()
        )

    def evaluate(
        self,
        learning_outcomes: Sequence[LearningOutcome] = (),
        learning_signals: Sequence[LearningSignal] = (),
        optimization_signals: Sequence[OptimizationSignal] = (),
        base_context: EvolutionContext | None = None,
    ) -> LearningEvolutionResult:
        """Evaluate learning information through autonomous evolution."""

        context = self.build_context(
            learning_outcomes=learning_outcomes,
            learning_signals=learning_signals,
            optimization_signals=optimization_signals,
            base_context=base_context,
        )

        decision = self.evolution_decision_engine.decide(context)

        return LearningEvolutionResult(
            context=context,
            decision=decision,
            learning_evidence_count=(len(learning_outcomes) + len(learning_signals)),
            optimization_signal_count=len(optimization_signals),
        )

    def build_context(
        self,
        learning_outcomes: Sequence[LearningOutcome] = (),
        learning_signals: Sequence[LearningSignal] = (),
        optimization_signals: Sequence[OptimizationSignal] = (),
        base_context: EvolutionContext | None = None,
    ) -> EvolutionContext:
        """Build an EvolutionContext with learning information."""

        if base_context is not None and not isinstance(
            base_context,
            EvolutionContext,
        ):
            raise TypeError("base_context must be an EvolutionContext instance.")

        learning_information = self._build_learning_information(
            learning_outcomes=learning_outcomes,
            learning_signals=learning_signals,
        )

        optimization_information = self._build_optimization_information(
            optimization_signals
        )

        if base_context is None:
            return EvolutionContext(
                learning_information=learning_information,
                improvement_information=optimization_information,
            )

        return EvolutionContext(
            execution_information=base_context.execution_information,
            evaluation_information=base_context.evaluation_information,
            learning_information=learning_information,
            knowledge_information=base_context.knowledge_information,
            memory_information=base_context.memory_information,
            improvement_information=(
                self._merge_improvement_information(
                    base_context.improvement_information,
                    optimization_information,
                )
            ),
            metadata=dict(base_context.metadata),
        )

    @staticmethod
    def _build_learning_information(
        learning_outcomes: Sequence[LearningOutcome],
        learning_signals: Sequence[LearningSignal],
    ) -> list[dict[str, Any]]:
        information: list[dict[str, Any]] = []

        for outcome in learning_outcomes:
            if not isinstance(
                outcome,
                LearningOutcome,
            ):
                raise TypeError(
                    "learning_outcomes must contain only LearningOutcome instances."
                )

            information.append(
                {
                    "score": outcome.confidence,
                    "confidence": outcome.confidence,
                    "source": "learning_outcome",
                    "experience_id": outcome.experience_id,
                    "pattern": outcome.learned_pattern,
                }
            )

        for signal in learning_signals:
            if not isinstance(
                signal,
                LearningSignal,
            ):
                raise TypeError(
                    "learning_signals must contain only LearningSignal instances."
                )

            information.append(
                {
                    "score": signal.confidence,
                    "confidence": signal.confidence,
                    "source": "learning_signal",
                    "signal_type": signal.signal_type,
                    "pattern": signal.pattern,
                    "impact": signal.impact,
                }
            )

        return information

    @staticmethod
    def _build_optimization_information(
        optimization_signals: Sequence[OptimizationSignal],
    ) -> list[dict[str, Any]]:
        information: list[dict[str, Any]] = []

        for signal in optimization_signals:
            if not isinstance(
                signal,
                OptimizationSignal,
            ):
                raise TypeError(
                    "optimization_signals must contain only "
                    "OptimizationSignal instances."
                )

            information.append(
                {
                    "score": signal.strength,
                    "confidence": signal.confidence,
                    "source": "optimization_signal",
                    "signal_type": signal.signal_type,
                    "target": signal.target,
                    "direction": signal.direction,
                    "reason": signal.reason,
                }
            )

        return information

    @staticmethod
    def _merge_improvement_information(
        existing: Any,
        optimization_information: list[dict[str, Any]],
    ) -> Any:
        if existing is None:
            return optimization_information

        if not optimization_information:
            return existing

        if isinstance(existing, list):
            return [
                *existing,
                *optimization_information,
            ]

        return {
            "existing": existing,
            "optimization_signals": optimization_information,
        }
