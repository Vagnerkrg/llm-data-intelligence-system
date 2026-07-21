from src.agents.memory.services.memory_validator import (
    MemoryValidator
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_type import (
    MemoryType
)



def test_should_validate_memory():

    validator = MemoryValidator()


    memory = MemoryEntry(
        memory_id="001",
        content="User prefers technical explanations.",
        memory_type=MemoryType.LONG_TERM
    )


    result = validator.validate(
        memory
    )


    assert result.success is True



def test_should_reject_invalid_memory():

    validator = MemoryValidator()


    result = validator.validate(
        None
    )


    assert result.success is False



def test_should_reject_memory_without_content():

    validator = MemoryValidator()


    memory = MemoryEntry(
        memory_id="001",
        content="",
        memory_type=MemoryType.LONG_TERM
    )


    result = validator.validate(
        memory
    )


    assert result.success is False