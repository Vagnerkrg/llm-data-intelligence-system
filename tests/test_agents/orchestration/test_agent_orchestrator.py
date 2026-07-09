from src.agents.orchestration.agent_orchestrator import (
    AgentOrchestrator
)



def test_agent_orchestrator_creation():

    orchestrator = AgentOrchestrator()


    assert orchestrator is not None



def test_agent_orchestrator_run():

    orchestrator = AgentOrchestrator()


    result = orchestrator.run(

        "How many customers exist?"

    )


    assert result.status == "completed"



def test_agent_orchestrator_reasoning():

    orchestrator = AgentOrchestrator()


    result = orchestrator.run(

        "Analyze sales data."

    )


    assert result.reasoning is not None



def test_agent_orchestrator_metadata():

    orchestrator = AgentOrchestrator()


    result = orchestrator.run(

        "Test request."

    )


    assert (
        result.metadata["component"]
        ==
        "agent_orchestrator"
    )