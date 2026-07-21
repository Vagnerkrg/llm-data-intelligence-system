from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_result import (
    MemoryResult
)

from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


class MemoryWriter:
    """
    Responsible for writing
    new memories into storage.
    """


    def __init__(
        self,
        storage
    ):
        self.storage = storage



    def write(
        self,
        memory: MemoryEntry
    ) -> MemoryResult:
        """
        Persist a memory entry.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):
            return MemoryResult(
                success=False,
                status=MemoryStatus.FAILED,
                message=(
                    "Invalid memory entry."
                )
            )


        self.storage.save(
            memory
        )


        return MemoryResult(
            success=True,
            status=MemoryStatus.STORED,
            message=(
                "Memory stored successfully."
            ),
            data=memory
        )