from typing import Optional, Dict, Any

from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.goal import Goal

from src.agents.reasoning.reasoning_result import ReasoningResult


class ExecutionContext:
    """
    Stores runtime information during
    an agent execution.

    The context keeps the current state
    shared between:

    - reasoning layer;
    - goal layer;
    - planning layer;
    - execution layer.

    V1.12 introduces goal driven
    execution context support.
    """

    def __init__(
        self,
        question: str,
        plan: Optional[ExecutionPlan] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):

        self.question = question

        self.plan = plan


        # V1.10 compatibility
        self.reasoning_result = None


        # V1.11 reasoning flow
        self.reasoning = None


        # V1.12 goal driven planning
        self.goal = None


        self.current_step = None

        self.results = []


        self.metadata = (
            metadata
            if metadata
            else {}
        )


        self.status = "initialized"



    def set_reasoning(
        self,
        reasoning_result: ReasoningResult
    ):
        """
        Store reasoning output
        generated before planning.
        """

        self.reasoning_result = reasoning_result

        self.reasoning = reasoning_result



    def set_goal(
        self,
        goal: Goal
    ):
        """
        Store execution goal
        generated from reasoning.

        V1.12:
        Goal becomes an explicit
        runtime state.
        """

        self.goal = goal



    def set_plan(
        self,
        plan: ExecutionPlan
    ):

        self.plan = plan

        self.status = "planned"



    def update_current_step(
        self
    ):
        """
        Update current runtime step
        from execution plan.
        """

        if not self.plan:

            self.current_step = None

            return


        self.current_step = (
            self.plan.next_step()
        )



    def clear_current_step(
        self
    ):
        """
        Clear current runtime step.
        """

        self.current_step = None



    def add_result(
        self,
        result: Any
    ):

        self.results.append(
            result
        )



    def complete(
        self
    ):

        self.status = "completed"



    def fail(
        self,
        error: str
    ):

        self.status = "failed"

        self.metadata["error"] = error



    def summary(
        self
    ) -> Dict[str, Any]:

        return {

            "question": self.question,


            "status": self.status,


            "has_reasoning": (
                self.reasoning is not None
            ),


            "has_goal": (
                self.goal is not None
            ),


            "goal_type": (
                self.goal.goal_type
                if self.goal
                else None
            ),


            "current_step": (
                self.current_step.action
                if self.current_step
                else None
            ),


            "results_count": len(
                self.results
            ),


            "has_plan": (
                self.plan is not None
            )

        }