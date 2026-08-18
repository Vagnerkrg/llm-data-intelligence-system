from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from src.agents.autonomous_evolution.domain.optimization_signal import (
    OptimizationSignal,
)
from src.agents.autonomous_evolution.services.experience_driven_optimizer import (
    ExperienceDrivenOptimizer,
)
from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.domain.evaluation_result import (
    EvaluationResult,
)
from src.agents.cognitive_evaluation.services.cognitive_evaluator import (
    CognitiveEvaluator,
)
from src.agents.cognitive_learning.domain import (
    LearningExperience,
    LearningOutcome,
)
from src.agents.cognitive_learning.integration.learning_evolution_bridge import (
    LearningEvolutionBridge,
    LearningEvolutionResult,
)
from src.agents.cognitive_learning.integration.learning_knowledge_integrator import (
    LearningKnowledgeIntegrator,
    LearningKnowledgeResult,
)
from src.agents.cognitive_learning.integration.learning_memory_bridge import (
    LearningMemoryBridge,
    LearningMemoryResult,
)
from src.agents.cognitive_learning.services.learning_outcome_engine import (
    LearningOutcomeEngine,
)
from src.agents.cognitive_learning.services.learning_signal_processor import (
    LearningSignalProcessor,
)
from src.agents.autonomous_evolution.domain.experience_optimization_context import (
    ExperienceOptimizationContext,
)


@dataclass
class CognitiveLearningLoopResult:
    """State produced by the complete cognitive learning loop."""

    success: bool = False
    evaluation_result: EvaluationResult | None = None
    learning_experiences: list[LearningExperience] = field(
        default_factory=list
    )
    learning_outcomes: list[LearningOutcome] = field(
        default_factory=list
    )
    knowledge_results: list[LearningKnowledgeResult] = field(
        default_factory=list
    )
    memory_results: list[LearningMemoryResult] = field(
        default_factory=list
    )
    optimization_signals: list[OptimizationSignal] = field(
        default_factory=list
    )
    evolution_result: LearningEvolutionResult | None = None
    failed_stage: str | None = None
    error: str | None = None


class CognitiveLearningLoop:
    """
    Orchestrates the complete cognitive learning cycle.

    Each layer is injected independently. The loop coordinates the
    flow but does not contain the internal rules of evaluation,
    learning, knowledge, memory, optimization, or evolution.
    """

    def __init__(
        self,
        cognitive_evaluator: CognitiveEvaluator | None = None,
        learning_signal_processor: LearningSignalProcessor | None = None,
        learning_outcome_engine: LearningOutcomeEngine | None = None,
        knowledge_integrator: LearningKnowledgeIntegrator | None = None,
        memory_bridge: LearningMemoryBridge | None = None,
        experience_optimizer: ExperienceDrivenOptimizer | None = None,
        evolution_bridge: LearningEvolutionBridge | None = None,
    ) -> None:
        self.cognitive_evaluator = (
            cognitive_evaluator
            if cognitive_evaluator is not None
            else CognitiveEvaluator()
        )
        self.learning_signal_processor = (
            learning_signal_processor
            if learning_signal_processor is not None
            else LearningSignalProcessor()
        )
        self.learning_outcome_engine = (
            learning_outcome_engine
            if learning_outcome_engine is not None
            else LearningOutcomeEngine()
        )
        self.knowledge_integrator = (
            knowledge_integrator
            if knowledge_integrator is not None
            else LearningKnowledgeIntegrator()
        )
        self.memory_bridge = memory_bridge
        self.experience_optimizer = (
            experience_optimizer
            if experience_optimizer is not None
            else ExperienceDrivenOptimizer()
        )
        self.evolution_bridge = (
            evolution_bridge
            if evolution_bridge is not None
            else LearningEvolutionBridge()
        )

    def run(
        self,
        evaluation_context: EvaluationContext,
        *,
        learning_signals: Sequence[Any] = (),
        execution_history: Sequence[Any] = (),
    ) -> CognitiveLearningLoopResult:
        """
        Execute the complete cognitive learning loop.

        Components fail in isolation: a failure in one stage is captured
        in the returned result without hiding the failing stage.
        """

        result = CognitiveLearningLoopResult()

        evaluation = self._run_stage(
            result,
            "evaluation",
            lambda: self.cognitive_evaluator.evaluate(
                evaluation_context
            ),
        )

        if evaluation is None:
            return result

        result.evaluation_result = evaluation

        signals = [
            {
                "signal_type": "cognitive_evaluation",
                "pattern": "cognitive evaluation completed",
                "confidence": evaluation.overall_score,
                "impact": self._resolve_evaluation_impact(
                    evaluation.overall_score
                ),
                "recommendation": (
                    "Use cognitive evaluation as learning evidence."
                ),
            },
            *list(learning_signals),
        ]

        experiences = self._run_stage(
            result,
            "learning_signal_processing",
            lambda: self.learning_signal_processor.process(
                signals
            ),
        )

        if experiences is None:
            return result

        result.learning_experiences = experiences

        outcomes = self._run_stage(
            result,
            "learning_outcome",
            lambda: self.learning_outcome_engine.evaluate(
                experiences
            ),
        )

        if outcomes is None:
            return result

        result.learning_outcomes = outcomes

        knowledge_results = self._run_stage(
            result,
            "knowledge",
            lambda: self.knowledge_integrator.integrate_many(
                outcomes
            ),
        )

        if knowledge_results is None:
            return result

        result.knowledge_results = knowledge_results

        if self.memory_bridge is not None:
            memory_results = self._run_stage(
                result,
                "memory",
                lambda: self.memory_bridge.store_many(
                    outcomes
                ),
            )

            if memory_results is None:
                return result

            result.memory_results = memory_results

        optimization_context = ExperienceOptimizationContext(
            execution_history=list(
                execution_history
            )
        )

        optimization_signals = self._run_stage(
            result,
            "optimization",
            lambda: self.experience_optimizer.optimize(
                optimization_context
            ),
        )

        if optimization_signals is None:
            return result

        result.optimization_signals = optimization_signals

        evolution_result = self._run_stage(
            result,
            "evolution",
            lambda: self.evolution_bridge.evaluate(
                learning_outcomes=outcomes,
                learning_signals=experiences,
                optimization_signals=optimization_signals,
            ),
        )

        if evolution_result is None:
            return result

        result.evolution_result = evolution_result
        result.success = True

        return result

    @staticmethod
    def _run_stage(
        result: CognitiveLearningLoopResult,
        stage: str,
        operation: Any,
    ) -> Any:
        try:
            return operation()
        except Exception as error:
            result.failed_stage = stage
            result.error = str(error)
            return None

    @staticmethod
    def _resolve_evaluation_impact(
        score: float,
    ) -> str:
        if score >= 0.8:
            return "high"

        if score >= 0.6:
            return "medium"

        return "low"