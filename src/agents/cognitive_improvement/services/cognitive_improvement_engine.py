from ..contracts.improvement_request import ImprovementRequest
from ..contracts.improvement_response import ImprovementResponse

from .improvement_orchestrator import ImprovementOrchestrator
from .improvement_validator import ImprovementValidator


class CognitiveImprovementEngine:
    """
    Public entry point for the Cognitive Improvement capability.

    Responsibilities:
    - receive an improvement request;
    - execute the cognitive improvement workflow;
    - validate the generated result;
    - return the improvement response.
    """

    def __init__(
        self,
        orchestrator: ImprovementOrchestrator | None = None,
        validator: ImprovementValidator | None = None,
    ) -> None:

        self.orchestrator = (
            orchestrator
            if orchestrator is not None
            else ImprovementOrchestrator()
        )

        self.validator = (
            validator
            if validator is not None
            else ImprovementValidator()
        )

    def execute(
        self,
        request: ImprovementRequest,
    ) -> ImprovementResponse:
        """
        Execute a complete cognitive improvement cycle.
        """

        result = self.orchestrator.execute(
            request.context
        )

        self.validator.validate(result)

        return ImprovementResponse(
            result=result
        )