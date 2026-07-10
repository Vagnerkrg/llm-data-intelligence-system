from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep


class ExecutionPlanner:
    """
    Responsible for creating execution plans.

    The planner defines the sequence of actions
    required to execute an agent workflow.

    Future versions may introduce:
    - LLM based planning;
    - dynamic tool selection;
    - adaptive execution strategies.
    """

    def create_plan(
        self,
        question: str
    ) -> ExecutionPlan:
        """
        Create an execution plan
        for the given request.
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
                    "for the request."
                )
            )
        )


        plan.add_step(
            PlanStep(
                step_id=2,
                action="execute_tool",
                description=(
                    "Execute selected tool."
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