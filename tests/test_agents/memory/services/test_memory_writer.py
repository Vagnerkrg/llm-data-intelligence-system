from src.agents.memory.services.memory_writer import (
    MemoryWriter
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)


class FakeMemoryStore:

    def __init__(self):
        self.saved = None


    def save(
        self,
        memory
    ):
        self.saved = memory



def test_should_write_memory():

    store = FakeMemoryStore()

    writer = MemoryWriter(
        store
    )


    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations.",
        memory_type=MemoryType.LONG_TERM
    )


    result = writer.write(
        memory
    )


    assert result.success is True
    assert store.saved == memory



def test_should_reject_invalid_memory():

    store = FakeMemoryStore()

    writer = MemoryWriter(
        store
    )


    result = writer.write(
        "invalid"
    )


    assert result.success is False