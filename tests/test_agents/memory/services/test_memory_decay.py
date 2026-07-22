from src.agents.memory.services.memory_decay import (
    MemoryDecay
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_should_apply_memory_decay():


    decay = MemoryDecay(
        decay_rate=0.2
    )


    memory = MemoryEntry(
        memory_id="001",
        content="Old technical preference.",
        memory_type=MemoryType.LONG_TERM,
        metadata={
            "relevance_score": 1.0
        }
    )


    result = decay.apply(
        memory
    )


    assert result["memory_id"] == "001"

    assert result["score"] == 0.8

    assert result["decayed"] is True



def test_should_fail_with_invalid_memory():


    decay = MemoryDecay()


    result = decay.apply(
        None
    )


    assert result["score"] == 0.0

    assert result["decayed"] is False