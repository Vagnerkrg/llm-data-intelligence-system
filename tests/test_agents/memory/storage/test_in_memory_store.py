from src.agents.memory.storage.in_memory_store import (
    InMemoryStore
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def create_memory():

    return MemoryEntry(
        memory_id="001",
        content="Stored memory.",
        memory_type=MemoryType.LONG_TERM
    )



def test_should_save_memory():

    store = InMemoryStore()


    memory = create_memory()


    result = store.save(
        memory
    )


    assert result is None

    assert store.get(
        "001"
    ) == memory



def test_should_delete_memory():

    store = InMemoryStore()


    memory = create_memory()


    store.save(
        memory
    )


    result = store.delete(
        "001"
    )


    assert result is True

    assert store.get(
        "001"
    ) is None



def test_should_list_all_memories():

    store = InMemoryStore()


    store.save(
        create_memory()
    )


    result = store.list_all()


    assert len(result) == 1

    assert result[0].memory_id == "001"