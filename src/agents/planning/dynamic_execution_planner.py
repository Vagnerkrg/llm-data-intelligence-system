from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep
from src.agents.planning.planner_strategy import PlannerStrategy


class DynamicExecutionPlanner:
    """
    Creates dynamic execution plans
    based on user intent analysis.
    """

    def __init__(
        self,
        strategy=None
    ):

        self.strategy = (
            strategy
            if strategy
            else PlannerStrategy()
        )


    def create_plan(
        self,
        question: str
    ) -> ExecutionPlan:
        """
        Create execution plan based
        on PlannerStrategy analysis.
        """


        analysis = (
            self.strategy.analyze(
                question
            )
        )


        request_type = (
            analysis.get(
                "type",
                "unknown"
            )
        )


        steps = [

            PlanStep(
                step_id=1,
                description="Route user request",
                action="route_request"
            ),

            PlanStep(
                step_id=2,
                description=f"Execute {request_type} operation",
                action="execute_tool"
            ),

            PlanStep(
                step_id=3,
                description="Generate final response",
                action="generate_response"
            )

        ]


        return ExecutionPlan(
            objective=question,
            steps=steps
        )