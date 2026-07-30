from src.agents.runtime.agent_runtime import (
    AgentRuntime
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)


def test_runtime_memory_intelligence_adapter():


    runtime = AgentRuntime()


    memory = MemoryEntry(
        memory_id="memory_runtime_001",
        content="Successful customer decision pattern",
        memory_type=MemoryType.SEMANTIC
    )


    result = runtime.analyze_memory(
        memory
    )


    assert result is not None

    assert result["memory_id"] == (
        "memory_runtime_001"
    )


    assert result["status"] == (
        "analyzed"
    )