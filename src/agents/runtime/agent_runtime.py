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


# Cognitive Improvement
from src.agents.cognitive_improvement.services.cognitive_improvement_engine import (
    CognitiveImprovementEngine
)

from src.agents.cognitive_improvement.domain.improvement_context import (
    ImprovementContext
)

from src.agents.cognitive_improvement.contracts.improvement_request import (
    ImprovementRequest
)


class AgentRuntime:
    """
    Runtime execution layer for AI agents.

    Coordinates:

    - execution context;
    - reasoning;
    - goal generation;
    - goal driven planning;
    - execution;
    - cognitive improvement cycle;
    - memory intelligence integration.
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
        memory_adapter=None
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


        # V1.20 Memory Intelligence
        self.memory_adapter = memory_adapter



    def create_context(
        self,
        question: str
    ) -> ExecutionContext:

        return ExecutionContext(
            question=question
        )



    def load_memory_context(
        self,
        context: ExecutionContext
    ):
        """
        Attach memory context to execution.

        V1.20:
        Connects runtime lifecycle
        with memory intelligence.
        """

        if not self.memory_adapter:
            return


        memory_context = {
            "enabled": True,
            "source": "runtime_memory_adapter"
        }


        context.set_memory_context(
            memory_context
        )



    def create_reasoning(
        self,
        question: str
    ) -> ReasoningResult:

        return self.reasoning_engine.reason(
            question
        )



    def create_goal(
        self,
        reasoning_result: ReasoningResult
    ) -> Goal:

        return self.goal_builder.build(
            reasoning_result
        )



    def create_goal_plan(
        self,
        goal: Goal
    ) -> ExecutionPlan:

        return self.goal_planner.create_plan(
            goal
        )



    def create_initial_plan(
        self,
        question: str,
        reasoning_result: Optional[ReasoningResult] = None,
        goal: Optional[Goal] = None
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



    def prepare(
        self,
        question: str
    ) -> ExecutionContext:


        context = self.create_context(
            question
        )


        # V1.20 Memory Integration
        self.load_memory_context(
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


        if goal:

            plan = self.create_goal_plan(
                goal
            )

        else:

            plan = self.create_initial_plan(
                question,
                reasoning_result
            )


        context.set_plan(
            plan
        )


        context.update_current_step()


        return context



    def execute(
        self,
        question: str
    ) -> ExecutionContext:


        context = self.prepare(
            question
        )


        execution_result = self.execution_engine.execute(
            context
        )


        #
        # Cognitive Improvement Loop
        #
        # Executed after main execution cycle.
        #

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


        return execution_result