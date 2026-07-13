from typing import Dict, Any


from src.agents.runtime.execution_loop import (
    ExecutionLoop
)


from src.agents.autonomy.autonomy_engine import (
    AutonomyEngine
)



class AutonomousExecutionRuntime:
    """
    Runtime layer responsible for autonomous
    execution adaptation.

    Coordinates execution cycles,
    replanning decisions and
    autonomy learning feedback.

    V1.16 adds:
    - observation;
    - reflection;
    - learning;
    - adaptation.
    """


    def __init__(
        self,
        execution_loop=None,
        autonomy_engine=None
    ):

        self.execution_loop = (
            execution_loop
            if execution_loop
            else ExecutionLoop()
        )


        self.autonomy_engine = (
            autonomy_engine
            if autonomy_engine
            else AutonomyEngine()
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

        V1.16:
        After execution evaluation,
        generates autonomy feedback.
        """


        result = self.execution_loop.process(
            plan=plan,
            execution_state=execution_state,
            feedback=feedback,
            evaluation=evaluation
        )


        autonomy_result = (
            self.autonomy_engine.evaluate_execution(
                execution_id="runtime-cycle",
                result=str(result),
                success=not evaluation.get(
                    "failed",
                    False
                ),
                metrics={}
            )
        )


        return {

            "plan": result["plan"],

            "replanned": result["replanned"],

            "decision": result["decision"],

            "autonomy": autonomy_result
        }