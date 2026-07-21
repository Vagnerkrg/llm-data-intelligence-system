from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_result import (
    MemoryResult
)

from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


class MemoryValidator:
    """
    Responsible for validating
    memory entries.
    """


    def validate(
        self,
        memory: MemoryEntry
    ) -> MemoryResult:
        """
        Validate memory integrity.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):
            return MemoryResult(
                success=False,
                status=MemoryStatus.FAILED,
                message=(
                    "Invalid memory object."
                )
            )


        if not memory.memory_id:

            return MemoryResult(
                success=False,
                status=MemoryStatus.FAILED,
                message=(
                    "Memory id is required."
                )
            )


        if not memory.content:

            return MemoryResult(
                success=False,
                status=MemoryStatus.FAILED,
                message=(
                    "Memory content is required."
                )
            )


        return MemoryResult(
            success=True,
            status=MemoryStatus.CREATED,
            message=(
                "Memory validation successful."
            ),
            data=memory
        )