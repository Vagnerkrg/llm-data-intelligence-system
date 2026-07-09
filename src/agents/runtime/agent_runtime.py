from typing import Optional

from src.agents.runtime.execution_context import ExecutionContext
from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep
from src.agents.controller.agent_controller import AgentController



class AgentRuntime:
    """
    Runtime execution layer for AI agents.

    Responsible for coordinating:

    - execution context;
    - planning layer;
    - agent controller;
    - future execution strategies.

    This component represents the
    agent execution lifecycle.
    """



    def __init__(
        self,
        controller: Optional[AgentController] = None
    ):

        self.controller = (
            controller
            if controller
            else AgentController()
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
        Create an initial execution plan.

        The first implementation uses
        a deterministic planning strategy.

        Future versions may introduce
        LLM-based planning.
        """

        plan = ExecutionPlan(

            objective=question

        )


        plan.add_step(

            PlanStep(

                step_id=1,

                action="route_request",

                description=(
                    "Select the best agent tool "
                    "for the user request."
                )

            )

        )


        plan.add_step(

            PlanStep(

                step_id=2,

                action="execute_tool",

                description=(
                    "Execute selected tool "
                    "and collect result."
                )

            )

        )


        plan.add_step(

            PlanStep(

                step_id=3,

                action="generate_response",

                description=(
                    "Prepare final response."
                )

            )

        )


        return plan



    def prepare(
        self,
        question: str
    ) -> ExecutionContext:
        """
        Prepare execution lifecycle.

        Creates context and attaches
        an execution plan.
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