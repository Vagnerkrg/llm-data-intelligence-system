from src.agents.memory.contracts.memory_request import (
    MemoryRequest
)


def test_should_create_memory_request():

    request = MemoryRequest(
        query="buscar histórico do agente"
    )

    assert request.query == (
        "buscar histórico do agente"
    )

    assert request.limit == 10


def test_should_create_memory_request_with_metadata():

    request = MemoryRequest(
        query="consultar memória",
        agent_id="agent-001",
        memory_type="episodic",
        metadata={
            "source": "runtime"
        }
    )

    assert request.agent_id == "agent-001"

    assert request.memory_type == "episodic"

    assert request.metadata["source"] == "runtime"