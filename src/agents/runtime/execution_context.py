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
        """
        Attach an execution plan
        to the current context.
        """

        self.plan = plan

        self.status = "planned"



    def update_current_step(
        self
    ):
        """
        Update current step from
        the execution plan.
        """

        if not self.plan:

            self.current_step = None

            return


        self.current_step = (
            self.plan.next_step()
        )



    def add_result(
        self,
        result: Any
    ):
        """
        Store an execution result.
        """

        self.results.append(
            result
        )



    def complete(
        self
    ):
        """
        Mark execution as completed.
        """

        self.status = "completed"



    def fail(
        self,
        error: str
    ):
        """
        Mark execution as failed.
        """

        self.status = "failed"

        self.metadata["error"] = error



    def summary(
        self
    ) -> Dict[str, Any]:
        """
        Return current execution state.
        """

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