from typing import Optional, Dict, Any

from src.agents.planning.execution_plan import ExecutionPlan


class ExecutionContext:
    """
    Stores runtime information during
    an agent execution.

    The context keeps the current state
    shared between planning and execution layers.
    """


    def __init__(
        self,
        question: str,
        plan: Optional[ExecutionPlan] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):

        self.question = question

        self.plan = plan

        self.current_step = None

        self.results = []

        self.metadata = (
            metadata
            if metadata
            else {}
        )

        self.status = "initialized"



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
        Update current step from
        the execution plan.

        Always retrieves the next pending step.
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
        Clear current runtime step
        after execution.
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

            "current_step": (
                self.current_step.action
                if self.current_step
                else None
            ),

            "results_count": len(
                self.results
            ),

            "has_plan": self.plan is not None

        }