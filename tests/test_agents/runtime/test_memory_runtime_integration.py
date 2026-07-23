from src.agents.runtime.agent_runtime import (
    AgentRuntime
)

from src.agents.memory.integration.runtime_memory_adapter import (
    RuntimeMemoryAdapter
)

from src.agents.memory.storage.storage_adapter import (
    StorageAdapter
)

from src.agents.memory.storage.in_memory_store import (
    InMemoryStore
)



def test_runtime_should_attach_memory_context():

    adapter = RuntimeMemoryAdapter(
        StorageAdapter(
            InMemoryStore()
        )
    )


    runtime = AgentRuntime(
        memory_adapter=adapter
    )


    context = runtime.prepare(
        "Analyze previous customer interactions."
    )


    assert context.memory_context is not None


    assert context.memory_context["enabled"] is True


    assert context.memory_context["source"] == (
        "runtime_memory_adapter"
    )