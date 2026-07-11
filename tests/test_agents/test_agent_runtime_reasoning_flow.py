from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.reasoning.reasoning_result import ReasoningResult


class MockReasoningEngine:
    """
    Mock reasoning engine used
    to validate runtime integration.
    """

    def reason(
        self,
        question: str
    ) -> ReasoningResult:

        return ReasoningResult(
            reasoning="Test reasoning",
            conclusion="Test conclusion",
            confidence=0.95,
            metadata={
                "source": "test"
            }
        )



def test_agent_runtime_stores_reasoning_result():

    runtime = AgentRuntime(
        reasoning_engine=MockReasoningEngine()
    )


    context = runtime.prepare(
        "Analyze customer sales"
    )


    assert context.reasoning_result is not None

    assert (
        context.reasoning_result.reasoning
        == "Test reasoning"
    )


    assert (
        context.reasoning_result.confidence
        == 0.95
    )