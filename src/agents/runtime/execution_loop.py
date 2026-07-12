from typing import Dict, Any


from src.agents.runtime.replanning_controller import (
    ReplanningController
)


class ExecutionLoop:
    """
    Coordinates execution lifecycle.

    Responsible for processing execution feedback
    and triggering replanning when required.
    """


    def __init__(
        self,
        replanning_controller=None
    ):

        self.replanning_controller = (
            replanning_controller
            if replanning_controller
            else ReplanningController()
        )


    def process(
        self,
        plan,
        execution_state: Dict[str, Any],
        feedback: Dict[str, Any],
        evaluation: Dict[str, Any]
    ):
        """
        Process current execution cycle.

        Returns execution decision and
        possible updated plan.
        """


        result = self.replanning_controller.evaluate_execution(
            plan=plan,
            execution_state=execution_state,
            feedback=feedback,
            evaluation=evaluation
        )


        return {
            "plan": result["plan"],

            "replanned": result["replanned"],

            "decision": result["decision"]
        }
    