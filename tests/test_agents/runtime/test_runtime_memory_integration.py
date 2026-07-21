from src.agents.runtime.agent_runtime import AgentRuntime

from src.agents.memory.services.memory_orchestrator import (
    MemoryOrchestrator
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)


class FakeMemoryOrchestrator:

    def __init__(self):

        self.storage = {}


    def remember(
        self,
        memory
    ):

        self.storage[memory.memory_id] = memory

        return memory



    def recall(
        self,
        memory_id
    ):

        return self.storage.get(
            memory_id
        )



def test_runtime_should_store_memory():

    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations.",
        memory_type=MemoryType.LONG_TERM
    )


    orchestrator = FakeMemoryOrchestrator()


    runtime = AgentRuntime(
        memory_orchestrator=orchestrator
    )


    result = runtime.remember_memory(
        memory
    )


    assert result == memory



def test_runtime_should_recall_memory():

    memory = MemoryEntry(
        memory_id="002",
        content="Previous decision stored.",
        memory_type=MemoryType.LONG_TERM
    )


    orchestrator = FakeMemoryOrchestrator()


    orchestrator.remember(
        memory
    )


    runtime = AgentRuntime(
        memory_orchestrator=orchestrator
    )


    result = runtime.recall_memory(
        "002"
    )


    assert result == memory