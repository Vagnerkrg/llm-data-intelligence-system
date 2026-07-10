from typing import Optional

from src.agents.runtime.execution_context import ExecutionContext
from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.execution_planner import ExecutionPlanner
from src.agents.controller.agent_controller import AgentController
from src.agents.execution.execution_engine import ExecutionEngine



class AgentRuntime:
    """
    Runtime execution layer for AI agents.

    Responsible for coordinating:

    - execution context;
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
        planner=None
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



    def create_initial_plan(
        self,
        question: str
    ) -> ExecutionPlan:
        """
        Create an execution plan
        using the execution planner.
        """

        return self.execution_planner.create_plan(
            question
        )



    def prepare(
        self,
        question: str
    ) -> ExecutionContext:
        """
        Prepare execution lifecycle.
        """

        context = self.create_context(
            question
        )


        plan = self.create_initial_plan(
            question
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