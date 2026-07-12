from typing import Dict, Any


from src.agents.planning.adaptive_replanning_policy import (
    AdaptiveReplanningPolicy
)

from src.agents.planning.autonomous_replanner import (
    AutonomousReplanner
)


class ReplanningController:
    """
    Coordinates autonomous replanning decisions.

    Responsible for connecting execution feedback,
    adaptive policy and replanning generation.
    """


    def __init__(
        self,
        policy=None,
        replanner=None
    ):

        self.policy = (
            policy
            if policy
            else AdaptiveReplanningPolicy()
        )

        self.replanner = (
            replanner
            if replanner
            else AutonomousReplanner()
        )


    def evaluate_execution(
        self,
        plan,
        execution_state: Dict[str, Any],
        feedback: Dict[str, Any],
        evaluation: Dict[str, Any]
    ):
        """
        Evaluate execution status and decide
        whether replanning is necessary.
        """


        decision = self.policy.evaluate(
            execution_state=execution_state,
            feedback=feedback,
            evaluation=evaluation
        )


        if not decision.should_replan:

            return {
                "decision": decision,
                "plan": plan,
                "replanned": False
            }


        updated_plan = self.replanner.replan(
            plan=plan,
            decision=decision
        )


        return {
            "decision": decision,
            "plan": updated_plan,
            "replanned": True
        }