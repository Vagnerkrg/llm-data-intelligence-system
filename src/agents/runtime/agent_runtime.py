from typing import Optional

from src.agents.runtime.execution_context import ExecutionContext

from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.execution_planner import ExecutionPlanner

from src.agents.planning.goal import Goal
from src.agents.planning.goal_builder import GoalBuilder
from src.agents.planning.goal_planner import GoalPlanner

from src.agents.controller.agent_controller import AgentController

from src.agents.execution.execution_engine import ExecutionEngine

from src.agents.reasoning.reasoning_engine import ReasoningEngine
from src.agents.reasoning.reasoning_result import ReasoningResult

from src.agents.cognitive_improvement.services.cognitive_improvement_engine import (
    CognitiveImprovementEngine
)

from src.agents.cognitive_improvement.domain.improvement_context import (
    ImprovementContext
)

from src.agents.cognitive_improvement.contracts.improvement_request import (
    ImprovementRequest
)

from src.agents.memory.intelligence.memory_relevance_scorer import (
    MemoryRelevanceScorer
)

from src.agents.memory.services.memory_intelligence import (
    MemoryIntelligence
)

from src.agents.cognitive_evaluation.services.cognitive_evaluation_adapter import (
    CognitiveEvaluationAdapter
)

from src.agents.cognitive_evaluation.services.cognitive_evaluator import (
    CognitiveEvaluator
)

from src.agents.autonomous_evolution.services.autonomous_evolution_adapter import (
    AutonomousEvolutionAdapter
)


class AgentRuntime:
    """
    Runtime execution layer for AI agents.
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
    ):

        self.controller = (
            controller
            if controller
            else AgentController()
        )

        self.execution_planner = (
            planner
            if planner
            else ExecutionPlanner()
        )

        self.goal_planner = (
            goal_planner
            if goal_planner
            else GoalPlanner()
        )

        self.reasoning_engine = (
            reasoning_engine
            if reasoning_engine
            else ReasoningEngine()
        )

        self.goal_builder = (
            goal_builder
            if goal_builder
            else GoalBuilder()
        )

        self.execution_engine = (
            execution_engine
            if execution_engine
            else ExecutionEngine(
                controller=self.controller
            )
        )

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
            else MemoryIntelligence(
                relevance_analyzer=MemoryRelevanceScorer()
            )
        )

        self.cognitive_evaluation_adapter = (
            cognitive_evaluation_adapter
            if cognitive_evaluation_adapter
            else CognitiveEvaluationAdapter()
        )

        self.cognitive_evaluator = (
            cognitive_evaluator
            if cognitive_evaluator
            else CognitiveEvaluator()
        )

        self.autonomous_evolution_adapter = (
            autonomous_evolution_adapter
            if autonomous_evolution_adapter
            else AutonomousEvolutionAdapter()
        )

    # CONTEXT

    def create_context(
        self,
        question: str
    ) -> ExecutionContext:

        return ExecutionContext(
            question=question
        )

    # REASONING

    def create_reasoning(
        self,
        question: str
    ) -> ReasoningResult:

        return self.reasoning_engine.reason(
            question
        )

    # GOAL

    def create_goal(
        self,
        reasoning_result
    ) -> Goal:

        goal = self.goal_builder.build(
            reasoning_result
        )

        if goal and not hasattr(
            goal,
            "description"
        ):

            goal.description = (
                getattr(
                    goal,
                    "name",
                    None
                )
                or getattr(
                    goal,
                    "objective",
                    None
                )
                or ""
            )

        return goal

    # PLANNING

    def create_initial_plan(
        self,
        question: str,
        reasoning_result=None,
        goal=None
    ) -> ExecutionPlan:

        try:

            return self.execution_planner.create_plan(
                question,
                reasoning_result,
                goal
            )

        except TypeError:

            try:

                return self.execution_planner.create_plan(
                    question,
                    reasoning_result
                )

            except TypeError:

                return self.execution_planner.create_plan(
                    question
                )

    # MEMORY INTELLIGENCE

    def analyze_memory(
        self,
        memory
    ):

        result = (
            self.memory_intelligence.analyze(
                memory
            )
        )

        return {
            "memory_id": memory.memory_id,
            "content": memory.content,
            "memory_type": memory.memory_type,
            "relevance_score": (
                result.score
                if hasattr(
                    result,
                    "score"
                )
                else None
            ),
            "status": "analyzed"
        }

    # MEMORY

    def attach_memory_context(
        self,
        context: ExecutionContext
    ):

        if self.memory_adapter:

            context.set_memory_context(
                {
                    "enabled": True,
                    "source": "runtime_memory_adapter",
                    "adapter": self.memory_adapter
                }
            )

        elif self.memory_orchestrator:

            context.set_memory_context(
                {
                    "enabled": True,
                    "source": "memory_orchestrator",
                    "orchestrator": self.memory_orchestrator
                }
            )

    def remember_memory(
        self,
        memory
    ):

        if not self.memory_orchestrator:
            return None

        return self.memory_orchestrator.remember(
            memory
        )

    def recall_memory(
        self,
        memory_id: str
    ):

        if not self.memory_orchestrator:
            return None

        return self.memory_orchestrator.recall(
            memory_id
        )

    # PREPARE

    def prepare(
        self,
        question: str
    ) -> ExecutionContext:

        context = self.create_context(
            question
        )

        self.attach_memory_context(
            context
        )

        reasoning_result = self.create_reasoning(
            question
        )

        context.set_reasoning(
            reasoning_result
        )

        goal = self.create_goal(
            reasoning_result
        )

        context.set_goal(
            goal
        )

        plan = self.create_initial_plan(
            question,
            reasoning_result,
            goal
        )

        context.set_plan(
            plan
        )

        context.update_current_step()

        return context

    # COGNITIVE EVALUATION

    def evaluate_cognition(
        self,
        context: ExecutionContext
    ):

        evaluation_context = (
            self.cognitive_evaluation_adapter.adapt(
                context
            )
        )

        evaluation_result = (
            self.cognitive_evaluator.evaluate(
                evaluation_context
            )
        )

        context.set_cognitive_evaluation(
            evaluation_result
        )

        return evaluation_result

    # AUTONOMOUS EVOLUTION

    def evaluate_evolution(
        self,
        context: ExecutionContext
    ):
        """
        Evaluate whether the completed execution provides sufficient
        evidence for autonomous evolution.

        The method only orchestrates the adapter. It does not contain
        evolution criteria or adaptation rules.
        """

        return self.autonomous_evolution_adapter.evaluate(
            context
        )

    # EXECUTE

    def execute(
        self,
        question: str
    ):

        context = self.prepare(
            question
        )

        execution_result = (
            self.execution_engine.execute(
                context
            )
        )

        improvement_context = ImprovementContext(
            experience=execution_result,
            objective=question,
            metadata={
                "source": "agent_runtime",
                "execution_status": execution_result.status
            }
        )

        improvement_request = ImprovementRequest(
            context=improvement_context
        )

        improvement_response = (
            self.cognitive_improvement_engine.execute(
                improvement_request
            )
        )

        execution_result.set_cognitive_improvement(
            improvement_response.result
        )

        self.evaluate_cognition(
            execution_result
        )

        self.evaluate_evolution(
            execution_result
        )

        return execution_result