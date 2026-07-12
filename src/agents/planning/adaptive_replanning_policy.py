from dataclasses import dataclass, field
from typing import Dict, Any, List



@dataclass
class ReplanningDecision:
    """
    Represents the decision produced by
    the adaptive replanning policy.
    """

    should_replan: bool

    reason: str

    strategy: str

    issues: List[str] = field(
        default_factory=list
    )



class AdaptiveReplanningPolicy:
    """
    Determines whether an execution plan
    should be adapted during runtime.
    """


    def evaluate(
        self,
        execution_state: Dict[str, Any],
        feedback: Dict[str, Any],
        evaluation: Dict[str, Any]
    ) -> ReplanningDecision:


        if evaluation.get("failed"):

            return ReplanningDecision(
                should_replan=True,
                reason="execution_failure_detected",
                strategy="recovery",
                issues=[
                    "execution_failed"
                ]
            )


        if feedback.get(
            "requires_adjustment"
        ):

            return ReplanningDecision(
                should_replan=True,
                reason="feedback_requires_adjustment",
                strategy="adaptation",
                issues=[
                    "feedback_adjustment_required"
                ]
            )


        if execution_state.get(
            "blocked"
        ):

            return ReplanningDecision(
                should_replan=True,
                reason="execution_blocked",
                strategy="alternative_path",
                issues=[
                    "execution_blocked"
                ]
            )


        return ReplanningDecision(
            should_replan=False,
            reason="execution_progress_normal",
            strategy="continue"
        )