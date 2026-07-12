from typing import Dict, Any


from src.agents.runtime.autonomous_execution_runtime import (
    AutonomousExecutionRuntime
)

from src.agents.observability.execution_monitor import (
    ExecutionMonitor
)



class ObservedExecutionRuntime:
    """
    Runtime extension with execution observation.

    Combines autonomous execution cycles with
    monitoring and observation capabilities.
    """


    def __init__(
        self,
        runtime=None,
        monitor=None
    ):

        self.runtime = (
            runtime
            if runtime
            else AutonomousExecutionRuntime()
        )


        self.monitor = (
            monitor
            if monitor
            else ExecutionMonitor()
        )



    def run_cycle(
        self,
        plan,
        execution_state: Dict[str, Any],
        feedback: Dict[str, Any],
        evaluation: Dict[str, Any]
    ):
        """
        Execute an observed autonomous cycle.
        """


        observation = self.monitor.monitor_cycle(
            execution_state=execution_state,
            feedback=feedback,
            evaluation=evaluation
        )


        result = self.runtime.run_cycle(
            plan=plan,
            execution_state=execution_state,
            feedback=feedback,
            evaluation=evaluation
        )


        return {

            "plan": result["plan"],

            "replanned": result["replanned"],

            "decision": result["decision"],

            "observation": observation

        }