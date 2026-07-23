from src.agents.memory.services.memory_manager import (
    MemoryManager
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_result import (
    MemoryResult
)

from src.agents.memory.domain.retrieval_result import (
    RetrievalResult
)


class MemoryEngine:
    """
    Public interface for agent memory operations.
    """


    def __init__(
        self,
        manager: MemoryManager
    ):

        self.manager = manager



    def remember(
        self,
        memory: MemoryEntry
    ) -> MemoryResult:
        """
        Store a new memory.
        """

        return self.manager.store(
            memory
        )



    def recall(
        self,
        memory_id: str
    ) -> RetrievalResult:
        """
        Retrieve an existing memory.
        """

        return self.manager.retrieve(
            memory_id
        )