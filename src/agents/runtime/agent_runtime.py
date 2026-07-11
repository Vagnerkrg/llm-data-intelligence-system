from typing import Optional

from src.agents.runtime.execution_context import ExecutionContext
from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.execution_planner import ExecutionPlanner
from src.agents.controller.agent_controller import AgentController
from src.agents.execution.execution_engine import ExecutionEngine
from src.agents.reasoning.reasoning_engine import ReasoningEngine
from src.agents.reasoning.reasoning_result import ReasoningResult


class AgentRuntime:
    """
    Runtime execution layer for AI agents.

    Responsible for coordinating:

    - execution context;
    - reasoning layer;
    - planning layer;
    - execution engine;
    - agent lifecycle.

    The runtime does not execute steps directly.
    Execution responsibility is delegated to
    the ExecutionEngine.
    """

    def __init__(
        self,
        controller: Optional[AgentController] = None,
        execution_engine=None,
        planner=None,
        reasoning_engine=None
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

        self.reasoning_engine = (
            reasoning_engine
            if reasoning_engine
            else ReasoningEngine()
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
        Create a new execution context.
        """

        return ExecutionContext(
            question=question
        )



    def create_reasoning(
        self,
        question: str
    ) -> ReasoningResult:
        """
        Generate reasoning result
        before planning.
        """

        return self.reasoning_engine.reason(
            question
        )



    def create_initial_plan(
        self,
        question: str,
        reasoning_result: Optional[ReasoningResult] = None
    ) -> ExecutionPlan:
        """
        Create an execution plan.

        Supports planners with and without
        reasoning awareness.

        V1.11 planners can consume
        reasoning_result.

        Legacy planners remain compatible.
        """

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

        The runtime flow is:

        Question
            |
        Reasoning
            |
        Planning
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
        Execute an agent workflow.

        Delegates execution to
        the ExecutionEngine.
        """

        context = self.prepare(
            question
        )


        return self.execution_engine.execute(
            context
        )