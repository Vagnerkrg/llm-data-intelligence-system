from typing import Optional, List

from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep
from src.agents.planning.planner_strategy import PlannerStrategy
from src.agents.reasoning.reasoning_result import ReasoningResult


class DynamicExecutionPlanner:
    """
    Creates dynamic execution plans
    based on intent analysis and reasoning.

    V1.12:
    Adds goal-driven planning while
    preserving execution workflow compatibility.
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
        question: str,
        reasoning_result: Optional[ReasoningResult] = None
    ) -> ExecutionPlan:
        """
        Create execution plan using:

        - question intent
        - planner strategy
        - reasoning information
        """


        analysis = self.strategy.analyze(
            question
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
                action="route_request",
                description=(
                    "Route user request "
                    "to appropriate capability."
                )
            ),

            PlanStep(
                step_id=2,
                action="execute_tool",
                description=(
                    self._execution_description(
                        request_type
                    )
                ),
                tool=(
                    self._select_tool(
                        request_type
                    )
                )
            ),

            PlanStep(
                step_id=3,
                action="generate_response",
                description=(
                    "Generate final response."
                )
            )

        ]


        plan = ExecutionPlan(
            objective=question,
            steps=steps
        )


        plan.metadata = {

            "request_type": request_type

        }


        if reasoning_result:

            plan.metadata.update(

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

                    "intent": (
                        reasoning_result.intent
                        if hasattr(
                            reasoning_result,
                            "intent"
                        )
                        else None
                    ),

                    "goal": (
                        reasoning_result.goal
                        if hasattr(
                            reasoning_result,
                            "goal"
                        )
                        else None
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


        return plan



    def _select_tool(
        self,
        request_type: str
    ) -> str:
        """
        Select preferred tool based
        on reasoning strategy.
        """


        mapping = {

            "analytics": "analytics_tool",

            "document": "document_tool",

            "unknown": "default_tool"

        }


        return mapping.get(
            request_type,
            "default_tool"
        )



    def _execution_description(
        self,
        request_type: str
    ) -> str:
        """
        Generate execution description
        without changing execution contract.
        """


        descriptions = {

            "analytics":
                "Execute analytics capability.",

            "document":
                "Execute document processing capability.",

            "unknown":
                "Execute selected tool."

        }


        return descriptions.get(
            request_type,
            "Execute selected tool."
        )