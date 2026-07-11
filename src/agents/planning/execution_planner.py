from typing import Optional

from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep
from src.agents.planning.goal import Goal

from src.agents.reasoning.reasoning_result import ReasoningResult


class ExecutionPlanner:
    """
    Responsible for creating execution plans.

    The planner defines the sequence of actions
    required to execute an agent workflow.

    Evolution:

    V1.11:
        Reasoning aware planning.

    V1.12:
        Goal driven planning foundation.
    """


    def create_plan(
        self,
        question: str,
        reasoning_result: Optional[ReasoningResult] = None,
        goal: Optional[Goal] = None
    ) -> ExecutionPlan:
        """
        Create an execution plan.

        Supports:

        - question only;
        - reasoning aware planning;
        - goal driven planning.

        Backward compatible with
        previous planners.
        """


        plan = ExecutionPlan(
            objective=question
        )


        metadata = {}


        if reasoning_result:

            metadata.update(

                {

                    "reasoning": (
                        reasoning_result.reasoning
                    ),

                    "conclusion": (
                        reasoning_result.conclusion
                    ),

                    "confidence": (
                        reasoning_result.confidence
                    ),

                    "strategy": (
                        reasoning_result.strategy
                        if hasattr(
                            reasoning_result,
                            "strategy"
                        )
                        else "default"
                    ),

                    "required_capabilities": (
                        reasoning_result.required_capabilities
                        if hasattr(
                            reasoning_result,
                            "required_capabilities"
                        )
                        else []
                    )

                }

            )


        if goal:

            metadata.update(

                {

                    "goal": goal.description,

                    "goal_type": (
                        goal.goal_type
                    ),

                    "goal_priority": (
                        goal.priority
                        if hasattr(
                            goal,
                            "priority"
                        )
                        else None
                    )

                }

            )


        if metadata:

            plan.metadata = metadata



        #
        # V1.12:
        # Goal can influence future
        # planning decisions.
        #
        # Current stage keeps
        # execution contract stable.
        #


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

                    "Execute selected tool "
                    "according to the goal."

                )

            )

        )



        plan.add_step(

            PlanStep(

                step_id=3,

                action="generate_response",

                description=(

                    "Prepare final response "
                    "aligned with execution goal."

                )

            )

        )



        return plan