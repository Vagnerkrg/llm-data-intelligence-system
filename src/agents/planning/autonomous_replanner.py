from copy import deepcopy

from src.agents.planning.execution_plan import (
    ExecutionPlan,
)

from src.agents.planning.plan_step import (
    PlanStep,
)

from src.agents.planning.replanning_decision import (
    ReplanningDecision,
)


class AutonomousReplanner:
    """
    Responsible for adapting execution plans
    based on replanning decisions.
    """

    def replan(
        self,
        plan: ExecutionPlan,
        decision: ReplanningDecision,
    ) -> ExecutionPlan:
        """
        Create an updated execution plan
        when replanning is required.
        """

        updated_plan = deepcopy(plan)

        if not decision.should_replan:
            return updated_plan


        recovery_step = PlanStep(
            step_id=len(updated_plan.steps) + 1,
            action="adaptive_recovery",
            description=(
                "Execute recovery strategy "
                "after execution failure"
            ),
            metadata={
                "reason": decision.reason,
                "issues": decision.issues,
            }
        )


        updated_plan.add_step(
            recovery_step
        )


        return updated_plan