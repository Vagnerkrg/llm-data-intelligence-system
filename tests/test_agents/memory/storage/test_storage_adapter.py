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



def create_adapter():

    store = InMemoryStore()

    return StorageAdapter(
        store
    )



def create_memory():

    return MemoryEntry(
        memory_id="001",
        content="Memory through adapter.",
        memory_type=MemoryType.LONG_TERM
    )



def test_should_save_memory_through_adapter():

    adapter = create_adapter()


    memory = create_memory()


    result = adapter.save(
        memory
    )


    assert result is None

    assert adapter.get(
        "001"
    ) == memory



def test_should_get_memory_through_adapter():

    adapter = create_adapter()


    memory = create_memory()


    adapter.save(
        memory
    )


    result = adapter.get(
        "001"
    )


    assert result.memory_id == "001"



def test_should_delete_memory_through_adapter():

    adapter = create_adapter()


    memory = create_memory()


    adapter.save(
        memory
    )


    result = adapter.delete(
        "001"
    )


    assert result is True



def test_should_list_memories_through_adapter():

    adapter = create_adapter()


    adapter.save(
        create_memory()
    )


    result = adapter.list_all()


    assert len(result) == 1