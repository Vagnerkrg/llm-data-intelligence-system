from src.agents.memory.services.memory_engine import (
    MemoryEngine
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


class MemoryOrchestrator:
    """
    Coordinates high-level memory workflows.
    """


    def __init__(
        self,
        engine: MemoryEngine
    ):

        self.engine = engine



    def remember(
        self,
        memory: MemoryEntry
    ) -> MemoryResult:
        """
        Execute memory storage workflow.
        """

        return self.engine.remember(
            memory
        )



    def recall(
        self,
        memory_id: str
    ) -> RetrievalResult:
        """
        Execute memory retrieval workflow.
        """

        return self.engine.recall(
            memory_id
        )