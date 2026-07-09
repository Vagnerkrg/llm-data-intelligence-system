from src.application.intelligence_system import IntelligenceSystem
from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.runtime.execution_context import ExecutionContext


def test_intelligence_system_has_agent_runtime():

    system = IntelligenceSystem()

    assert isinstance(
        system.agent_runtime,
        AgentRuntime
    )


def test_execution_context_creation():

    context = ExecutionContext(
        question="How many products exist?"
    )

    assert context.question == "How many products exist?"