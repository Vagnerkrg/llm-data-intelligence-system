from src.agents.memory.utils.memory_mapper import (
    MemoryMapper
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_should_map_memory_to_dict():

    memory = MemoryEntry(
        memory_id="001",
        content="mapper test",
        memory_type=MemoryType.LONG_TERM
    )


    result = MemoryMapper.to_dict(
        memory
    )


    assert result["memory_id"] == "001"

    assert result["content"] == "mapper test"

    assert result["memory_type"] == "long_term"