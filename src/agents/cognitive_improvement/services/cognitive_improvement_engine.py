from ..contracts.improvement_request import ImprovementRequest
from ..contracts.improvement_response import ImprovementResponse

from .improvement_orchestrator import ImprovementOrchestrator
from .improvement_validator import ImprovementValidator


class CognitiveImprovementEngine:
    """
    Entry point for the cognitive improvement capability.

    Coordinates execution of improvement cycles
    and validates generated improvements.

    V1.18 implementation:
    - receives improvement request;
    - executes cognitive improvement workflow;
    - validates improvement result;
    - returns improvement response.
    """


    def __init__(
        self,
        orchestrator: ImprovementOrchestrator | None = None,
        validator: ImprovementValidator | None = None,
    ):

        self.orchestrator = (
            orchestrator
            if orchestrator
            else ImprovementOrchestrator()
        )

        self.validator = (
            validator
            if validator
            else ImprovementValidator()
        )


    def execute(
        self,
        request: ImprovementRequest
    ) -> ImprovementResponse:
        """
        Execute cognitive improvement cycle.

        Args:
            request:
                Improvement request containing context.

        Returns:
            ImprovementResponse
        """

        result = self.orchestrator.execute(
            request.context
        )


        is_valid = self.validator.validate(
            result
        )


        return ImprovementResponse(
            result=result
        )