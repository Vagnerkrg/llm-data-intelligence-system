from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class PlanStep:
    """
    Represents a single execution step
    inside an agent execution plan.

    A plan step describes one action
    that the agent should perform.
    """

    step_id: int

    action: str

    description: str

    tool: Optional[str] = None

    status: str = "pending"

    result: Optional[Any] = None

    metadata: Optional[Dict[str, Any]] = None



    def complete(
        self,
        result: Any
    ):
        """
        Mark the step as completed
        and store execution result.
        """

        self.status = "completed"

        self.result = result



    def fail(
        self,
        error: str
    ):
        """
        Mark the step as failed.
        """

        self.status = "failed"

        self.result = {
            "error": error
        }



    def is_completed(
        self
    ) -> bool:
        """
        Check whether the step
        finished successfully.
        """

        return self.status == "completed"