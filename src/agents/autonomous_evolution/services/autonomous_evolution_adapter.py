from typing import Any

from src.agents.autonomous_evolution.domain.evolution_context import (
    EvolutionContext,
)
from src.agents.autonomous_evolution.domain.evolution_decision import (
    EvolutionDecision,
)
from src.agents.autonomous_evolution.domain.evolution_action import (
    EvolutionAction,
)
from src.agents.autonomous_evolution.domain.evolution_result import (
    EvolutionResult,
)
from src.agents.autonomous_evolution.services.adaptive_behavior_policy import (
    AdaptiveBehaviorPolicy,
)
from src.agents.autonomous_evolution.services.evolution_decision_engine import (
    EvolutionDecisionEngine,
)
from src.agents.runtime.execution_context import ExecutionContext
from src.agents.self_improvement.adaptation.domain.adaptation_action import (
    AdaptationAction,
)


class AutonomousEvolutionAdapter:
    """
    Integrates autonomous evolution with runtime state.

    The adapter translates ExecutionContext into EvolutionContext,
    delegates evolution decisions to the decision engine, validates
    potential behavioral adaptations through the policy, and translates
    the approved adaptation into the Autonomous Evolution domain.

    It does not execute adaptations.
    """

    def __init__(
        self,
        evolution_decision_engine: EvolutionDecisionEngine | None = None,
        adaptive_behavior_policy: AdaptiveBehaviorPolicy | None = None,
    ) -> None:
        self.evolution_decision_engine = (
            evolution_decision_engine
            if evolution_decision_engine is not None
            else EvolutionDecisionEngine()
        )

        self.adaptive_behavior_policy = (
            adaptive_behavior_policy
            if adaptive_behavior_policy is not None
            else AdaptiveBehaviorPolicy()
        )

    def evaluate(
        self,
        execution_context: ExecutionContext,
        target: str = "agent",
    ) -> EvolutionResult:
        """
        Evaluate runtime state for autonomous evolution.

        The resulting EvolutionResult belongs to the Autonomous Evolution
        domain. Any AdaptationAction produced by the policy is translated
        into an EvolutionAction before being stored in the result.
        """

        evolution_context = self.build_context(
            execution_context
        )

        decision = self.evolution_decision_engine.decide(
            evolution_context
        )

        execution_context.set_evolution_decision(
            decision
        )

        adaptation_action = self._build_adaptation_action(
            decision=decision,
            target=target,
        )

        execution_context.set_adaptation_action(
            adaptation_action
        )

        evolution_action = self._build_evolution_action(
            adaptation_action
        )

        if evolution_action is not None:
            decision.action = evolution_action

        result = EvolutionResult(
            status=decision.status,
            success=adaptation_action is not None,
            action=evolution_action,
            message=self._build_result_message(
                decision=decision,
                adaptation_action=adaptation_action,
            ),
            metadata={
                "source": self.__class__.__name__,
                "evidence_count": len(decision.evidence),
                "should_evolve": decision.should_evolve,
                "has_adaptation_action": (
                    adaptation_action is not None
                ),
            },
        )

        execution_context.set_evolution_result(
            result
        )

        return result

    def build_context(
        self,
        execution_context: ExecutionContext,
    ) -> EvolutionContext:
        """
        Convert runtime state into an autonomous evolution context.
        """

        if not isinstance(
            execution_context,
            ExecutionContext,
        ):
            raise TypeError(
                "execution_context must be an ExecutionContext instance."
            )

        return EvolutionContext(
            execution_information=(
                self._build_execution_information(
                    execution_context
                )
            ),
            evaluation_information=(
                execution_context.cognitive_evaluation
            ),
            learning_information=(
                self._build_learning_information(
                    execution_context
                )
            ),
            knowledge_information=(
                self._build_knowledge_information(
                    execution_context
                )
            ),
            memory_information=(
                execution_context.memory_context
            ),
            improvement_information=(
                self._build_improvement_information(
                    execution_context
                )
            ),
            metadata={
                "question": execution_context.question,
                "status": execution_context.status,
            },
        )

    @staticmethod
    def _build_execution_information(
        context: ExecutionContext,
    ) -> dict[str, Any]:
        """
        Build normalized execution evidence.
        """

        execution_score = (
            1.0
            if context.status == "completed"
            else 0.0
        )

        return {
            "score": execution_score,
            "confidence": 1.0,
            "execution_status": context.status,
            "results_count": len(context.results),
        }

    @staticmethod
    def _build_learning_information(
        context: ExecutionContext,
    ) -> Any:
        improvement = context.cognitive_improvement

        if improvement is None:
            return None

        insights = getattr(
            improvement,
            "insights",
            None,
        )

        if insights is None:
            return None

        return insights

    @staticmethod
    def _build_knowledge_information(
        context: ExecutionContext,
    ) -> Any:
        improvement = context.cognitive_improvement

        if improvement is None:
            return None

        knowledge = getattr(
            improvement,
            "knowledge",
            None,
        )

        if knowledge is None:
            return None

        return knowledge

    @staticmethod
    def _build_improvement_information(
        context: ExecutionContext,
    ) -> Any:
        improvement = context.cognitive_improvement

        if improvement is None:
            return None

        adaptations = getattr(
            improvement,
            "adaptations",
            None,
        )

        if adaptations is None:
            return None

        return adaptations

    def _build_adaptation_action(
        self,
        decision: EvolutionDecision,
        target: str,
    ) -> AdaptationAction | None:
        """
        Validate whether a proposed evolution can become a controlled
        adaptation action.
        """

        return self.adaptive_behavior_policy.evaluate(
            decision=decision,
            target=target,
        )

    @staticmethod
    def _build_evolution_action(
        adaptation_action: AdaptationAction | None,
    ) -> EvolutionAction | None:
        """
        Translate an Adaptation Layer action into the Autonomous Evolution
        domain representation.
        """

        if adaptation_action is None:
            return None

        return EvolutionAction(
            action_type=adaptation_action.adaptation_type.value,
            target=adaptation_action.target,
            parameters={
                "priority": adaptation_action.priority,
            },
            reason=adaptation_action.description,
            metadata={
                "source": "adaptation_layer",
            },
        )

    @staticmethod
    def _build_result_message(
        decision: EvolutionDecision,
        adaptation_action: AdaptationAction | None,
    ) -> str:
        if adaptation_action is not None:
            return (
                "Evolution approved and behavioral adaptation "
                "action proposed."
            )

        if decision.should_evolve:
            return (
                "Evolution decision produced no eligible "
                "behavioral adaptation."
            )

        return "No autonomous evolution was approved."