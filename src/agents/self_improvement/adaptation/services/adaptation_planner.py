from ..domain.adaptation_action import AdaptationAction
from ..domain.adaptation_type import AdaptationType
from ..domain.adaptation_context import AdaptationContext


class AdaptationPlanner:
    """
    Creates adaptation actions based on evaluation context.
    """

    def plan(
        self,
        context: AdaptationContext,
        target: str,
    ) -> AdaptationAction:

        return AdaptationAction(
            adaptation_type=AdaptationType.BEHAVIOR,
            target=target,
            description=context.reason,
        )