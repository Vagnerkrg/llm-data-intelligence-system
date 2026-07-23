from src.agents.memory.services.memory_retriever import (
    MemoryRetriever
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



class FakeMemoryStore:

    def __init__(self):
        self.memory = None


    def get(
        self,
        memory_id
    ):
        if self.memory and self.memory.memory_id == memory_id:
            return self.memory

        return None



def test_should_retrieve_memory():


    store = FakeMemoryStore()


    memory = MemoryEntry(
        memory_id="001",
        content="Previous user preference",
        memory_type=MemoryType.LONG_TERM
    )


    store.memory = memory


    retriever = MemoryRetriever(
        store
    )


    result = retriever.retrieve(
        "001"
    )


    assert result.success is True
    assert result.memory == memory



def test_should_return_failure_when_memory_not_found():


    store = FakeMemoryStore()


    retriever = MemoryRetriever(
        store
    )


    result = retriever.retrieve(
        "999"
    )


    assert result.success is False