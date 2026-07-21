from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


def test_should_have_expected_status_values():

    assert MemoryStatus.CREATED.value == "created"

    assert MemoryStatus.STORED.value == "stored"

    assert MemoryStatus.RETRIEVED.value == "retrieved"

    assert MemoryStatus.FAILED.value == "failed"