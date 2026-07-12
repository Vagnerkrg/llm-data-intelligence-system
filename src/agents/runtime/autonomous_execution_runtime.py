from typing import Dict, Any


from src.agents.runtime.execution_loop import (
    ExecutionLoop
)



class AutonomousExecutionRuntime:
    """
    Runtime layer responsible for autonomous
    execution adaptation.

    Coordinates execution cycles and
    replanning decisions.
    """


    def __init__(
        self,
        execution_loop=None
    ):

        self.execution_loop = (
            execution_loop
            if execution_loop
            else ExecutionLoop()
        )


    def run_cycle(
        self,
        plan,
        execution_state: Dict[str, Any],
        feedback: Dict[str, Any],
        evaluation: Dict[str, Any]
    ):
        """
        Execute one autonomous execution cycle.
        """


        result = self.execution_loop.process(
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