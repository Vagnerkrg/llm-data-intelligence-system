from typing import Dict, Any, List


from src.agents.observability.execution_observer import (
    ExecutionObserver
)



class ExecutionMonitor:
    """
    Monitors autonomous execution lifecycle.

    Coordinates multiple execution observations
    and provides execution insights for
    evaluation and adaptive replanning.
    """


    def __init__(
        self,
        observer=None
    ):

        self.observer = (
            observer
            if observer
            else ExecutionObserver()
        )

        self.cycles: List[Dict[str, Any]] = []



    def monitor_cycle(
        self,
        execution_state: Dict[str, Any],
        feedback: Dict[str, Any] = None,
        evaluation: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Register a new execution monitoring cycle.
        """


        observation = self.observer.observe(
            execution_state=execution_state,
            feedback=feedback,
            evaluation=evaluation
        )


        self.cycles.append(
            observation
        )


        return observation



    def total_cycles(
        self
    ) -> int:
        """
        Return number of monitored cycles.
        """


        return len(
            self.cycles
        )



    def has_failed_cycles(
        self
    ) -> bool:
        """
        Detect whether execution history
        contains failures.
        """


        return any(
            cycle.get("status")
            ==
            "failed"

            for cycle in self.cycles
        )



    def latest_cycle(
        self
    ) -> Dict[str, Any]:
        """
        Return latest monitored cycle.
        """


        if not self.cycles:

            return {}


        return self.cycles[-1]