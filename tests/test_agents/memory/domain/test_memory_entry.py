from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)

from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


def test_should_create_memory_entry():

    entry = MemoryEntry(
        memory_id="001",
        content="informação importante",
        memory_type=MemoryType.SEMANTIC
    )


    assert entry.memory_id == "001"

    assert entry.content == (
        "informação importante"
    )

    assert entry.memory_type == (
        MemoryType.SEMANTIC
    )

    assert entry.status == (
        MemoryStatus.CREATED
    )