from src.agents.memory.domain.memory_context import (
    MemoryContext
)


def test_should_create_memory_context():

    context = MemoryContext(
        agent_id="agent-001",
        query="buscar histórico"
    )


    assert context.agent_id == (
        "agent-001"
    )

    assert context.query == (
        "buscar histórico"
    )

    assert context.memories == []