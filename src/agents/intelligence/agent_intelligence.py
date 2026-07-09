from typing import Optional

from src.agents.reasoning.reasoning_engine import ReasoningEngine
from src.agents.orchestration.agent_orchestrator import AgentOrchestrator

from src.agents.intelligence.intelligence_result import IntelligenceResult



class AgentIntelligence:
    """
    High level intelligence layer.

    Coordinates:

    - reasoning;
    - orchestration;
    - final intelligence generation.

    This represents the cognitive layer
    of the agent architecture.
    """



    def __init__(
        self,
        reasoning_engine: Optional[ReasoningEngine] = None,
        orchestrator: Optional[AgentOrchestrator] = None
    ):

        self.reasoning_engine = (
            reasoning_engine
            if reasoning_engine
            else ReasoningEngine()
        )


        self.orchestrator = (
            orchestrator
            if orchestrator
            else AgentOrchestrator()
        )



    def process(
        self,
        question: str
    ) -> IntelligenceResult:
        """
        Process a user request
        through the intelligence pipeline.
        """


        reasoning_result = self.reasoning_engine.reason(
            question
        )


        orchestration_result = self.orchestrator.execute(
            question
        )


        return IntelligenceResult(

            answer=(
                orchestration_result.result
                if hasattr(
                    orchestration_result,
                    "result"
                )
                else str(orchestration_result)
            ),

            confidence=(
                reasoning_result.confidence
            ),

            reasoning=(
                reasoning_result.reasoning
            ),

            metadata={

                "component": "agent_intelligence"

            }

        )