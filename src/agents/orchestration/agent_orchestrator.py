from typing import Optional


from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.reasoning.reasoning_engine import ReasoningEngine
from src.agents.orchestration.orchestration_result import OrchestrationResult



class AgentOrchestrator:
    """
    High level coordination layer
    for intelligent agents.

    Responsible for coordinating:

    - reasoning;
    - runtime execution;
    - final orchestration result.
    """



    def __init__(
        self,
        runtime: Optional[AgentRuntime] = None,
        reasoning_engine: Optional[ReasoningEngine] = None
    ):


        self.runtime = (
            runtime
            if runtime
            else AgentRuntime()
        )


        self.reasoning_engine = (
            reasoning_engine
            if reasoning_engine
            else ReasoningEngine()
        )



    def run(
        self,
        question: str
    ) -> OrchestrationResult:
        """
        Execute complete agent flow.
        """


        try:


            reasoning = (
                self.reasoning_engine.reason(
                    question
                )
            )


            context = (
                self.runtime.execute(
                    question
                )
            )


            return OrchestrationResult(

                status="completed",

                result=context,

                reasoning=reasoning.reasoning,

                metadata={

                    "component":
                        "agent_orchestrator",

                    "confidence":
                        reasoning.confidence

                }

            )


        except Exception as error:


            return OrchestrationResult(

                status="failed",

                result=None,

                reasoning=None,

                metadata={

                    "error": str(error)

                }

            )