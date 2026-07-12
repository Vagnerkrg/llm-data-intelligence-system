from dataclasses import dataclass
from typing import List


from src.agents.execution.execution_feedback import (
    ExecutionFeedback
)



@dataclass
class ReplanningDecision:
    """
    Represents the decision about whether
    an agent should replan execution.
    """

    should_replan: bool

    reason: str

    strategy: str = "continue"

    issues: List[str] = None


    def __post_init__(self):
        """
        Ensure issues always has
        a valid list structure.
        """

        if self.issues is None:
            self.issues = []



class ReplanningDecisionEngine:
    """
    Analyzes execution feedback and decides
    whether replanning is required.
    """


    def decide(
        self,
        feedback: ExecutionFeedback
    ) -> ReplanningDecision:
        """
        Evaluate execution feedback and
        generate replanning decision.
        """


        if not feedback.success:

            return ReplanningDecision(
                should_replan=True,

                reason=(
                    "Execution failure detected"
                ),

                strategy="recovery",

                issues=(
                    feedback.issues
                    if feedback.issues
                    else []
                )
            )


        return ReplanningDecision(
            should_replan=False,

            reason=(
                "Execution completed successfully"
            ),

            strategy="continue",

            issues=[]
        )