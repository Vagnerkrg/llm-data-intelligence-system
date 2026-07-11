from typing import Optional, List


from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep
from src.agents.planning.goal import Goal


from src.agents.reasoning.reasoning_result import (
    ReasoningResult
)


from src.agents.planning.planner_strategy import (
    PlannerStrategy
)


class DynamicExecutionPlanner:
    """
    Creates execution plans dynamically
    based on user goals and detected strategy.
    """


    def __init__(
        self,
        strategy=None
    ):
        """
        Initialize planner.
        """

        self.strategy = (
            strategy
            if strategy
            else PlannerStrategy()
        )


    def create_plan(
        self,
        question: str,
        reasoning_result: Optional[ReasoningResult] = None
    ) -> ExecutionPlan:
        """
        Create execution plan based
        on goal and strategy analysis.
        """


        analysis = self.strategy.analyze(
            question
        )


        request_type = (
            analysis.get(
                "type",
                "general"
            )
        )


        goal = Goal(

            objective=question,

            intent=request_type,

            required_capabilities=(

                reasoning_result.required_capabilities

                if reasoning_result

                else analysis.get(
                    "required_capabilities",
                    []
                )

            ),

            metadata={

                "strategy": analysis.get(
                    "strategy",
                    "default"
                )

            }

        )


        steps = self.generate_steps(
            analysis
        )


        return ExecutionPlan(

            goal=goal,

            steps=steps

        )


    def generate_steps(
        self,
        analysis: dict
    ) -> List[PlanStep]:
        """
        Generate execution steps
        according to detected strategy.
        """


        plan_type = analysis.get(
            "type",
            "general"
        )


        steps = []


        #
        # Step 1
        # Routing
        #

        steps.append(

            PlanStep(

                step_id=1,

                action="route_request",

                description=(
                    "Route user request "
                    "according to detected intent"
                ),

                tool="router_tool"

            )

        )


        #
        # Step 2
        # Tool execution
        #

        steps.append(

            PlanStep(

                step_id=2,

                action="execute_tool",

                description=(
                    "Execute selected capability "
                    "for user request"
                ),

                tool=(
                    "analytics_tool"
                    if plan_type == "analytics"
                    else
                    "retrieval_tool"
                    if plan_type == "document"
                    else
                    "reasoning_tool"
                )

            )

        )


        #
        # Intermediate reasoning
        #

        if plan_type == "analytics":

            steps.append(

                PlanStep(

                    step_id=3,

                    action="generate_insights",

                    description=(
                        "Generate analytical insights "
                        "from processed data"
                    ),

                    tool="reasoning_tool"

                )

            )


        elif plan_type == "document":

            steps.append(

                PlanStep(

                    step_id=3,

                    action="summarize_content",

                    description=(
                        "Summarize document content"
                    ),

                    tool="reasoning_tool"

                )

            )


        else:

            steps.append(

                PlanStep(

                    step_id=3,

                    action="general_reasoning",

                    description=(
                        "Perform general reasoning "
                        "for user request"
                    ),

                    tool="reasoning_tool"

                )

            )


        #
        # Final response generation
        #

        steps.append(

            PlanStep(

                step_id=4,

                action="generate_response",

                description=(
                    "Generate final response "
                    "for the user"
                ),

                tool="response_generator"

            )

        )


        return steps