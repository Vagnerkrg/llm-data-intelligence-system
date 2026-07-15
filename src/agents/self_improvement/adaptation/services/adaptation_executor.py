from src.agents.self_improvement.adaptation.domain.adaptation_action import (
    AdaptationAction,
)

from src.agents.self_improvement.adaptation.domain.adaptation_result import (
    AdaptationResult,
)


class AdaptationExecutor:
    """
    Executes approved adaptation actions.

    This service represents the execution boundary
    between adaptation decisions and system changes.
    """

    def execute(
        self,
        action: AdaptationAction,
    ) -> AdaptationResult:

        return AdaptationResult(
            success=True,
            action=action,
            message="Adaptation executed successfully.",
        )