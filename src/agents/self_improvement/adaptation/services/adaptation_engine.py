from ..contracts.adaptation_request import AdaptationRequest
from ..contracts.adaptation_response import AdaptationResponse

from ..domain.adaptation_result import AdaptationResult

from .adaptation_policy import AdaptationPolicy
from .adaptation_planner import AdaptationPlanner


class AdaptationEngine:
    """
    Executes the adaptation decision process.
    """

    def __init__(self):
        self.policy = AdaptationPolicy()
        self.planner = AdaptationPlanner()

    def adapt(
        self,
        request: AdaptationRequest,
    ) -> AdaptationResponse:

        allowed = self.policy.evaluate(
            request.context.confidence
        )

        action = self.planner.plan(
            request.context,
            request.target,
        )

        result = AdaptationResult(
            success=allowed,
            action=action,
            message=(
                "Adaptation approved."
                if allowed
                else "Adaptation rejected."
            ),
        )

        return AdaptationResponse(
            result=result
        )