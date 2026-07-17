from ..contracts.improvement_request import ImprovementRequest
from ..contracts.improvement_response import ImprovementResponse


class CognitiveImprovementEngine:
    def execute(self, request: ImprovementRequest) -> ImprovementResponse:
        raise NotImplementedError