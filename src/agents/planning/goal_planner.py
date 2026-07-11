from typing import Optional

from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep
from src.agents.planning.goal import Goal


class GoalPlanner:
    """
    Generates execution plans based on goals.
    """


    def create_plan(
        self,
        goal: Goal
    ) -> ExecutionPlan:
        """
        Create execution plan from goal.
        """


        steps = [

            PlanStep(
                step_id=1,
                action="route_request",
                description=(
                    "Analyze goal and select "
                    "the best execution capability."
                )
            ),


            PlanStep(
                step_id=2,
                action="execute_tool",
                description=(
                    "Execute selected capability."
                )
            ),


            PlanStep(
                step_id=3,
                action="generate_response",
                description=(
                    "Generate final response "
                    "aligned with the goal."
                )
            )

        ]


        return ExecutionPlan(

            objective=goal.objective,

            steps=steps,

            metadata={

                "goal": goal.objective,

                "intent": goal.intent,

                "required_capabilities":
                    goal.required_capabilities

            }

        )