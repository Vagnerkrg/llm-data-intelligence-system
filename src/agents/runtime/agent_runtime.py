from datetime import datetime, timezone
from typing import Optional

from src.agents.runtime.execution_context import (
    ExecutionContext,
)

from src.agents.planning.execution_plan import (
    ExecutionPlan,
)
from src.agents.planning.execution_planner import (
    ExecutionPlanner,
)

from src.agents.planning.goal import (
    Goal,
)
from src.agents.planning.goal_builder import (
    GoalBuilder,
)
from src.agents.planning.goal_planner import (
    GoalPlanner,
)

from src.agents.controller.agent_controller import (
    AgentController,
)

from src.agents.execution.execution_engine import (
    ExecutionEngine,
)

from src.agents.reasoning.reasoning_engine import (
    ReasoningEngine,
)
from src.agents.reasoning.reasoning_result import (
    ReasoningResult,
)

from src.agents.cognitive_improvement.services.cognitive_improvement_engine import (
    CognitiveImprovementEngine,
)

from src.agents.cognitive_improvement.domain.improvement_context import (
    ImprovementContext,
)

from src.agents.cognitive_improvement.contracts.improvement_request import (
    ImprovementRequest,
)

from src.agents.memory.intelligence.memory_relevance_scorer import (
    MemoryRelevanceScorer,
)

from src.agents.memory.services.memory_intelligence import (
    MemoryIntelligence,
)

from src.agents.cognitive_evaluation.services.cognitive_evaluation_adapter import (
    CognitiveEvaluationAdapter,
)

from src.agents.cognitive_evaluation.services.cognitive_evaluator import (
    CognitiveEvaluator,
)

from src.agents.autonomous_evolution.services.autonomous_evolution_adapter import (
    AutonomousEvolutionAdapter,
)

from src.agents.cognitive_learning.services.cognitive_learning_loop import (
    CognitiveLearningLoop,
)

from src.observability.domain.enums import (
    ExecutionStatus,
)

from src.observability.services.agent_runtime_observability import (
    AgentRuntimeObservability,
)


class AgentRuntime:
    """
    Runtime execution layer for AI agents.

    Observability is optional and isolated from the business flow.
    """

    def __init__(
        self,
        controller: Optional[AgentController] = None,
        execution_engine=None,
        planner=None,
        reasoning_engine=None,
        goal_builder=None,
        goal_planner=None,
        cognitive_improvement_engine=None,
        memory_orchestrator=None,
        memory_adapter=None,
        memory_intelligence=None,
        cognitive_evaluation_adapter=None,
        cognitive_evaluator=None,
        autonomous_evolution_adapter=None,
        cognitive_learning_loop=None,
        observability=None,
        observability_enabled: bool = True,
    ):
        self.controller = controller if controller else AgentController()

        self.execution_planner = planner if planner else ExecutionPlanner()

        self.goal_planner = goal_planner if goal_planner else GoalPlanner()

        self.reasoning_engine = (
            reasoning_engine if reasoning_engine else ReasoningEngine()
        )

        self.goal_builder = goal_builder if goal_builder else GoalBuilder()

        self.cognitive_improvement_engine = (
            cognitive_improvement_engine
            if cognitive_improvement_engine
            else CognitiveImprovementEngine()
        )

        self.memory_orchestrator = memory_orchestrator
        self.memory_adapter = memory_adapter

        self.memory_intelligence = (
            memory_intelligence
            if memory_intelligence
            else MemoryIntelligence(relevance_analyzer=MemoryRelevanceScorer())
        )

        self.cognitive_evaluation_adapter = (
            cognitive_evaluation_adapter
            if cognitive_evaluation_adapter
            else CognitiveEvaluationAdapter()
        )

        self.cognitive_evaluator = (
            cognitive_evaluator if cognitive_evaluator else CognitiveEvaluator()
        )

        self.autonomous_evolution_adapter = (
            autonomous_evolution_adapter
            if autonomous_evolution_adapter
            else AutonomousEvolutionAdapter()
        )

        self.cognitive_learning_loop = (
            cognitive_learning_loop
            if cognitive_learning_loop is not None
            else CognitiveLearningLoop()
        )

        self.observability = (
            observability
            if observability is not None
            else AgentRuntimeObservability(
                enabled=observability_enabled,
            )
        )

        self.execution_engine = (
            execution_engine
            if execution_engine
            else ExecutionEngine(
                controller=self.controller,
                observability=self.observability,
            )
        )

    # CONTEXT

    def create_context(
        self,
        question: str,
    ) -> ExecutionContext:
        return ExecutionContext(
            question=question,
        )

    # REASONING

    def create_reasoning(
        self,
        question: str,
    ) -> ReasoningResult:
        return self.reasoning_engine.reason(question)

    # GOAL

    def create_goal(
        self,
        reasoning_result,
    ) -> Goal:
        goal = self.goal_builder.build(reasoning_result)

        if goal and not hasattr(
            goal,
            "description",
        ):
            goal.description = (
                getattr(
                    goal,
                    "name",
                    None,
                )
                or getattr(
                    goal,
                    "objective",
                    None,
                )
                or ""
            )

        return goal

    # PLANNING

    def create_initial_plan(
        self,
        question: str,
        reasoning_result=None,
        goal=None,
    ) -> ExecutionPlan:
        try:
            return self.execution_planner.create_plan(
                question,
                reasoning_result,
                goal,
            )

        except TypeError:
            try:
                return self.execution_planner.create_plan(
                    question,
                    reasoning_result,
                )

            except TypeError:
                return self.execution_planner.create_plan(question)

    # MEMORY INTELLIGENCE

    def analyze_memory(
        self,
        memory,
    ):
        result = self.memory_intelligence.analyze(memory)

        return {
            "memory_id": memory.memory_id,
            "content": memory.content,
            "memory_type": memory.memory_type,
            "relevance_score": (
                result.score
                if hasattr(
                    result,
                    "score",
                )
                else None
            ),
            "status": "analyzed",
        }

    # MEMORY

    def attach_memory_context(
        self,
        context: ExecutionContext,
    ):
        if self.memory_adapter:
            context.set_memory_context(
                {
                    "enabled": True,
                    "source": "runtime_memory_adapter",
                    "adapter": self.memory_adapter,
                }
            )

        elif self.memory_orchestrator:
            context.set_memory_context(
                {
                    "enabled": True,
                    "source": "memory_orchestrator",
                    "orchestrator": self.memory_orchestrator,
                }
            )

    def remember_memory(
        self,
        memory,
    ):
        if not self.memory_orchestrator:
            return None

        return self.memory_orchestrator.remember(memory)

    def recall_memory(
        self,
        memory_id: str,
    ):
        if not self.memory_orchestrator:
            return None

        return self.memory_orchestrator.recall(memory_id)

    # PREPARE

    def prepare(
        self,
        question: str,
        context: Optional[ExecutionContext] = None,
    ) -> ExecutionContext:
        context = context if context is not None else self.create_context(question)

        self.attach_memory_context(context)

        self._safe_observability(
            "reasoning_started",
            context.execution_id,
        )

        try:
            reasoning_result = self.create_reasoning(question)

            context.set_reasoning(reasoning_result)

            self._safe_observability(
                "reasoning_completed",
                context.execution_id,
            )

        except Exception as error:
            self._safe_observability(
                "reasoning_failed",
                context.execution_id,
                error,
            )
            raise

        self._safe_observability(
            "planning_started",
            context.execution_id,
        )

        try:
            goal = self.create_goal(reasoning_result)

            context.set_goal(goal)

            plan = self.create_initial_plan(
                question,
                reasoning_result,
                goal,
            )

            context.set_plan(plan)

            context.update_current_step()

            self._safe_observability(
                "planning_completed",
                context.execution_id,
            )

        except Exception as error:
            self._safe_observability(
                "planning_failed",
                context.execution_id,
                error,
            )
            raise

        return context

    # COGNITIVE EVALUATION

    def evaluate_cognition(
        self,
        context: ExecutionContext,
    ):
        self._safe_observability(
            "cognitive_evaluation_started",
            context.execution_id,
        )

        try:
            evaluation_context = self.cognitive_evaluation_adapter.adapt(context)

            evaluation_result = self.cognitive_evaluator.evaluate(evaluation_context)

            context.set_cognitive_evaluation(evaluation_result)

            score = getattr(
                evaluation_result,
                "score",
                None,
            )

            if score is None:
                score = getattr(
                    evaluation_result,
                    "overall_score",
                    None,
                )

            confidence = getattr(
                evaluation_result,
                "confidence",
                None,
            )

            self._safe_observability(
                "cognitive_evaluation_completed",
                context.execution_id,
                score=score,
                result=evaluation_result,
                confidence=confidence,
                provenance="agent_runtime.evaluate_cognition",
            )

            return evaluation_result

        except Exception as error:
            self._safe_observability(
                "error",
                context.execution_id,
                error,
                component="evaluation",
                stage="evaluation",
            )

            raise

    # COGNITIVE LEARNING

    def run_cognitive_learning(
        self,
        context: ExecutionContext,
        learning_signals=None,
        execution_history=None,
    ):
        if not isinstance(
            context,
            ExecutionContext,
        ):
            raise TypeError("context must be an ExecutionContext instance.")

        evaluation_context = self.cognitive_evaluation_adapter.adapt(context)

        result = self.cognitive_learning_loop.run(
            evaluation_context,
            learning_signals=(learning_signals if learning_signals is not None else ()),
            execution_history=(
                execution_history if execution_history is not None else context.results
            ),
        )

        context.set_learning_loop_result(result)

        self._observe_learning_result(
            context,
            result,
        )

        return result

    # AUTONOMOUS EVOLUTION

    def evaluate_evolution(
        self,
        context: ExecutionContext,
    ):
        result = self.autonomous_evolution_adapter.evaluate(context)

        self._observe_evolution_result(
            context,
            result,
        )

        return result

    # EXECUTE

    def execute(
        self,
        question: str,
    ):
        context = self.create_context(question)

        execution_id = self._safe_start_observation()

        self._safe_observability(
            "attach_to_context",
            context,
            execution_id,
        )

        start_time = datetime.now(timezone.utc)

        self._safe_observability(
            "record_state",
            execution_id,
            status=ExecutionStatus.RUNNING,
            component="runtime",
            stage="runtime",
        )

        try:
            context = self.prepare(
                question,
                context=context,
            )

            self._safe_observability(
                "execution_started",
                context.execution_id,
            )

            execution_result = self.execution_engine.execute(context)

            duration_ms = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds() * 1000

            if execution_result.status == "failed":
                self._safe_observability(
                    "execution_failed",
                    execution_result.execution_id,
                    RuntimeError(
                        execution_result.metadata.get(
                            "error",
                            "Execution failed.",
                        )
                    ),
                    duration_ms=duration_ms,
                )

            else:
                self._safe_observability(
                    "execution_completed",
                    execution_result.execution_id,
                    duration_ms=duration_ms,
                )

            improvement_context = ImprovementContext(
                experience=execution_result,
                objective=question,
                metadata={
                    "source": "agent_runtime",
                    "execution_status": (execution_result.status),
                },
            )

            improvement_request = ImprovementRequest(context=improvement_context)

            improvement_response = self.cognitive_improvement_engine.execute(
                improvement_request
            )

            execution_result.set_cognitive_improvement(improvement_response.result)

            self.evaluate_cognition(execution_result)

            self.run_cognitive_learning(execution_result)

            self.evaluate_evolution(execution_result)

            return execution_result

        except Exception as error:
            duration_ms = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds() * 1000

            self._safe_observability(
                "fail_execution",
                execution_id,
                error,
                duration_ms=duration_ms,
            )

            raise

    # COGNITIVE OBSERVABILITY

    def _observe_learning_result(
        self,
        context: ExecutionContext,
        result,
    ) -> None:
        """Observe learning loop outputs without coupling internals."""

        for experience in getattr(
            result,
            "learning_experiences",
            [],
        ):
            confidence = self._extract_numeric(
                experience,
                "confidence",
            )

            signal_type = self._extract_string(
                experience,
                "signal_type",
            )

            self._safe_observability(
                "learning_signal_generated",
                context.execution_id,
                confidence=confidence,
                signal_type=signal_type,
                provenance="cognitive_learning_loop",
            )

        for outcome in getattr(
            result,
            "learning_outcomes",
            [],
        ):
            confidence = self._extract_numeric(
                outcome,
                "confidence",
            )

            outcome_type = self._extract_string(
                outcome,
                "outcome_type",
            )

            self._safe_observability(
                "learning_outcome_created",
                context.execution_id,
                outcome_type=outcome_type,
                confidence=confidence,
                provenance="cognitive_learning_loop",
            )

        for knowledge_result in getattr(
            result,
            "knowledge_results",
            [],
        ):
            self._safe_observability(
                "knowledge_accessed",
                context.execution_id,
                result=knowledge_result,
                provenance="learning_knowledge_integrator",
                confidence=self._extract_numeric(
                    knowledge_result,
                    "confidence",
                ),
            )

            self._safe_observability(
                "knowledge_updated",
                context.execution_id,
                result=knowledge_result,
                provenance="learning_knowledge_integrator",
                confidence=self._extract_numeric(
                    knowledge_result,
                    "confidence",
                ),
            )

        for memory_result in getattr(
            result,
            "memory_results",
            [],
        ):
            self._safe_observability(
                "memory_retrieval_completed",
                context.execution_id,
                memories_retrieved=1,
                relevance_score=self._extract_numeric(
                    memory_result,
                    "relevance_score",
                ),
                provenance="learning_memory_bridge",
            )

        for optimization_signal in getattr(
            result,
            "optimization_signals",
            [],
        ):
            self._safe_observability(
                "optimization_signal_generated",
                context.execution_id,
                signal_type=self._extract_string(
                    optimization_signal,
                    "signal_type",
                ),
                confidence=self._extract_numeric(
                    optimization_signal,
                    "confidence",
                ),
                provenance="experience_driven_optimizer",
            )

        failed_stage = getattr(
            result,
            "failed_stage",
            None,
        )

        error = getattr(
            result,
            "error",
            None,
        )

        if failed_stage:
            self._safe_observability(
                "error",
                context.execution_id,
                RuntimeError(error or f"Cognitive stage failed: {failed_stage}"),
                component="cognitive_learning",
                stage=failed_stage,
            )

        self._safe_observability(
            "learning_completed",
            context.execution_id,
            signals=len(
                getattr(
                    result,
                    "learning_experiences",
                    [],
                )
            ),
            outcomes=len(
                getattr(
                    result,
                    "learning_outcomes",
                    [],
                )
            ),
        )

    def _observe_evolution_result(
        self,
        context: ExecutionContext,
        result,
    ) -> None:
        """Observe autonomous evolution outputs."""

        if result is None:
            return

        decision_created = result is not None

        self._safe_observability(
            "evolution_decision_created",
            context.execution_id,
            decision=result,
            confidence=self._extract_numeric(
                result,
                "confidence",
            ),
            provenance="autonomous_evolution_adapter",
        )

        adaptation_applied = bool(
            getattr(
                result,
                "adapted",
                False,
            )
        )

        if adaptation_applied:
            self._safe_observability(
                "adaptation_applied",
                context.execution_id,
                result=result,
                provenance="autonomous_evolution_adapter",
                confidence=self._extract_numeric(
                    result,
                    "confidence",
                ),
            )

        self._safe_observability(
            "evolution_completed",
            context.execution_id,
            decision_created=decision_created,
            adaptation_applied=adaptation_applied,
        )

    # SAFE OBSERVABILITY

    def _safe_start_observation(
        self,
    ) -> Optional[str]:
        """Start observability without affecting runtime."""
        try:
            return self.observability.start_execution(
                correlation_id=None,
                metadata={
                    "source": "agent_runtime",
                },
            )
        except Exception:
            return None

    def _safe_observability(
        self,
        method_name: str,
        *args,
        **kwargs,
    ):
        """Invoke observability safely without affecting runtime."""
        try:
            method = getattr(
                self.observability,
                method_name,
                None,
            )

            if method is None:
                return None

            return method(
                *args,
                **kwargs,
            )

        except Exception:
            return None

    @staticmethod
    def _extract_numeric(
        value,
        attribute: str,
    ) -> Optional[float]:
        """Extract a numeric field from dicts or objects."""
        if isinstance(value, dict):
            result = value.get(
                attribute,
            )
        else:
            result = getattr(
                value,
                attribute,
                None,
            )

        if result is None:
            return None

        try:
            return float(result)
        except (
            TypeError,
            ValueError,
        ):
            return None

    @staticmethod
    def _extract_string(
        value,
        attribute: str,
    ) -> Optional[str]:
        """Extract a string field from dicts or objects."""
        if isinstance(value, dict):
            result = value.get(
                attribute,
            )
        else:
            result = getattr(
                value,
                attribute,
                None,
            )

        if result is None:
            return None

        return str(result)
