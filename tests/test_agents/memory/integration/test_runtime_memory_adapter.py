from src.agents.memory.integration.runtime_memory_adapter import (
    RuntimeMemoryAdapter
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



class FakeStorage:

    def __init__(self):

        self.memory = None


    def save(
        self,
        memory
    ):

        self.memory = memory

        return memory



    def get(
        self,
        memory_id
    ):

        return self.memory



def create_adapter():

    return RuntimeMemoryAdapter(
        FakeStorage()
    )



def test_should_remember_memory_from_runtime():

    adapter = create_adapter()


    memory = MemoryEntry(
        memory_id="001",
        content="Runtime context information.",
        memory_type=MemoryType.LONG_TERM
    )


    result = adapter.remember(
        memory
    )


    assert result.memory_id == "001"



def test_should_recall_memory_from_runtime():

    adapter = create_adapter()


    memory = MemoryEntry(
        memory_id="001",
        content="Stored runtime memory.",
        memory_type=MemoryType.LONG_TERM
    )


    adapter.remember(
        memory
    )


    result = adapter.recall(
        "001"
    )


    assert result.memory_id == "001"