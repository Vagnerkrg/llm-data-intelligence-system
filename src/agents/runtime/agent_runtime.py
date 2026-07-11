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


class AgentRuntime:
    """
    Runtime execution layer for AI agents.

    Coordinates:

    - execution context;
    - reasoning;
    - goal generation;
    - goal driven planning;
    - execution.

    V1.12 introduces
    goal driven planning flow.
    """


    def __init__(
        self,
        controller: Optional[AgentController] = None,
        execution_engine=None,
        planner=None,
        reasoning_engine=None,
        goal_builder=None,
        goal_planner=None
    ):


        self.controller = (
            controller
            if controller
            else AgentController()
        )


        # Legacy planner support
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



    def create_context(
        self,
        question: str
    ) -> ExecutionContext:
        """
        Create execution context.
        """

        return ExecutionContext(
            question=question
        )



    def create_reasoning(
        self,
        question: str
    ) -> ReasoningResult:
        """
        Generate reasoning before planning.
        """

        return self.reasoning_engine.reason(
            question
        )



    def create_goal(
        self,
        reasoning_result: ReasoningResult
    ) -> Goal:
        """
        Build execution goal from reasoning.
        """

        return self.goal_builder.build(
            reasoning_result
        )



    def create_goal_plan(
        self,
        goal: Goal
    ) -> ExecutionPlan:
        """
        Create execution plan from goal.

        V1.12:
        Goal driven planning path.
        """

        return self.goal_planner.create_plan(
            goal
        )



    def create_initial_plan(
        self,
        question: str,
        reasoning_result: Optional[ReasoningResult] = None,
        goal: Optional[Goal] = None
    ) -> ExecutionPlan:
        """
        Legacy planning fallback.

        Supports:

        - reasoning aware planners;
        - old execution planners.
        """


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
        """
        Prepare execution lifecycle.

        V1.12 Flow:

        Question
            |
        Reasoning
            |
        Goal Builder
            |
        Goal
            |
        Goal Planner
            |
        Execution Plan
            |
        Execution Context
        """


        context = self.create_context(
            question
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


        #
        # V1.12 Goal Driven Planning
        #

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
        """
        Execute agent workflow.

        Delegates execution
        to ExecutionEngine.
        """


        context = self.prepare(
            question
        )


        return self.execution_engine.execute(
            context
        )