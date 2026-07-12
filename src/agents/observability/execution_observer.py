from typing import Dict, Any, List


class ExecutionObserver:
    """
    Observes autonomous execution cycles.

    Responsible for collecting execution signals,
    events and state transitions that can be used
    by evaluation and replanning layers.
    """


    def __init__(self):

        self.events: List[Dict[str, Any]] = []


    def observe(
        self,
        execution_state: Dict[str, Any],
        feedback: Dict[str, Any] = None,
        evaluation: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Collect execution information
        and generate an observation snapshot.
        """


        observation = {

            "execution_state": execution_state,

            "feedback": (
                feedback
                if feedback
                else {}
            ),

            "evaluation": (
                evaluation
                if evaluation
                else {}
            ),

            "status": (
                execution_state.get(
                    "status",
                    "unknown"
                )
            )

        }


        self.events.append(
            observation
        )


        return observation



    def last_observation(
        self
    ) -> Dict[str, Any]:
        """
        Return latest execution observation.
        """


        if not self.events:

            return {}


        return self.events[-1]



    def has_failures(
        self
    ) -> bool:
        """
        Check whether latest observation
        detected execution failure.
        """


        if not self.events:

            return False


        latest = self.events[-1]


        return (
            latest["status"]
            ==
            "failed"
        )