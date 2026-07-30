"""
Execution Planner

Responsible for creating execution plans
for AgentRuntime.

Generates ExecutionPlan composed by
ExecutionStep objects.
"""


from typing import Optional


from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.execution_step import ExecutionStep


try:
    from src.agents.reasoning.reasoning_result import ReasoningResult
except Exception:
    ReasoningResult = object


try:
    from src.agents.planning.goal import Goal
except Exception:
    Goal = object



class ExecutionPlanner:
    """
    Creates execution plans for agent execution.
    """



    def __init__(self):
        pass



    def create_plan(
        self,
        question: str,
        reasoning_result: Optional[ReasoningResult] = None,
        goal: Optional[Goal] = None
    ) -> ExecutionPlan:
        """
        Creates an execution plan.

        Supports:

        - simple question planning
        - reasoning aware planning
        - goal driven planning
        """



        plan = ExecutionPlan(
            objective=question
        )



        metadata = {}



        #
        # Reasoning metadata
        #

        if reasoning_result:


            metadata.update(

                {

                    "reasoning": getattr(
                        reasoning_result,
                        "reasoning",
                        None
                    ),


                    "conclusion": getattr(
                        reasoning_result,
                        "conclusion",
                        None
                    ),


                    "confidence": getattr(
                        reasoning_result,
                        "confidence",
                        None
                    ),


                    "strategy": getattr(
                        reasoning_result,
                        "strategy",
                        "default"
                    ),


                    "required_capabilities": getattr(
                        reasoning_result,
                        "required_capabilities",
                        []
                    )

                }

            )



        #
        # Goal metadata
        #

        if goal:


            metadata.update(

                {


                    "goal": getattr(
                        goal,
                        "description",
                        getattr(
                            goal,
                            "objective",
                            None
                        )
                    ),


                    "goal_type": getattr(
                        goal,
                        "goal_type",
                        "general"
                    ),


                    "intent": getattr(
                        goal,
                        "intent",
                        "general"
                    ),


                    "goal_priority": getattr(
                        goal,
                        "priority",
                        None
                    )

                }

            )



        plan.metadata = metadata



        #
        # Default execution pipeline
        #

        if not plan.steps:



            plan.add_step(

                ExecutionStep(

                    step_id="step_1",

                    action="route_request",

                    description=(
                        "Route user request"
                    )

                )

            )



            plan.add_step(

                ExecutionStep(

                    step_id="step_2",

                    action="execute_tool",

                    description=(
                        "Execute required tools"
                    ),

                    dependencies=[
                        "step_1"
                    ]

                )

            )



            plan.add_step(

                ExecutionStep(

                    step_id="step_3",

                    action="generate_response",

                    description=(
                        "Generate final response"
                    ),

                    dependencies=[
                        "step_2"
                    ]

                )

            )



        return plan