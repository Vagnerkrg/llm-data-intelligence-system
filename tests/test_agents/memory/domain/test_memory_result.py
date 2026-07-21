from src.agents.memory.domain.memory_result import (
    MemoryResult
)

from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


def test_should_create_memory_result():

    result = MemoryResult(
        success=True,
        status=MemoryStatus.STORED,
        message="memória salva"
    )


    assert result.success is True

    assert result.status == (
        MemoryStatus.STORED
    )

    assert result.message == (
        "memória salva"
    )