from src.agents.memory.storage.storage_adapter import (
    StorageAdapter
)

from src.agents.memory.storage.in_memory_store import (
    InMemoryStore
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_should_save_using_adapter():

    adapter = StorageAdapter(
        InMemoryStore()
    )


    memory = MemoryEntry(
        memory_id="001",
        content="Adapter test",
        memory_type=MemoryType.LONG_TERM
    )


    adapter.save(
        memory
    )


    result = adapter.get(
        "001"
    )


    assert result == memory



def test_should_list_using_adapter():

    adapter = StorageAdapter(
        InMemoryStore()
    )


    result = adapter.list_all()


    assert result == []