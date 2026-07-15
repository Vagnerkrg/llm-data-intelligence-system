from src.agents.self_improvement.adaptation.contracts.adaptation_request import (
    AdaptationRequest,
)

from src.agents.self_improvement.adaptation.contracts.adaptation_response import (
    AdaptationResponse,
)

from src.agents.self_improvement.adaptation.services.adaptation_engine import (
    AdaptationEngine,
)

from src.agents.self_improvement.adaptation.services.adaptation_executor import (
    AdaptationExecutor,
)

from src.agents.self_improvement.adaptation.services.adaptation_history import (
    AdaptationHistory,
)


class AdaptationManager:
    """
    High-level orchestrator for the Adaptation Capability.
    """

    def __init__(self):

        self.engine = AdaptationEngine()
        self.executor = AdaptationExecutor()
        self.history = AdaptationHistory()

    def adapt(
        self,
        request: AdaptationRequest,
    ) -> AdaptationResponse:

        response = self.engine.adapt(request)

        result = self.executor.execute(
            response.result.action
        )

        self.history.record(result)

        return response