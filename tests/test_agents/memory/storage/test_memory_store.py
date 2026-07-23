from src.agents.memory.storage.memory_store import (
    MemoryStore
)


def test_memory_store_should_be_abstract():

    assert MemoryStore.__abstractmethods__