from src.agents.memory.services.memory_validator import (
    MemoryValidator
)

from src.agents.memory.services.memory_writer import (
    MemoryWriter
)

from src.agents.memory.services.memory_retriever import (
    MemoryRetriever
)

from src.agents.memory.services.memory_ranker import (
    MemoryRanker
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


class MemoryManager:
    """
    Coordinates memory operations.
    """


    def __init__(
        self,
        writer: MemoryWriter,
        retriever: MemoryRetriever,
        validator: MemoryValidator,
        ranker: MemoryRanker
    ):

        self.writer = writer

        self.retriever = retriever

        self.validator = validator

        self.ranker = ranker



    def store(
        self,
        memory: MemoryEntry
    ) -> MemoryResult:
        """
        Validate and store memory.
        """


        validation = self.validator.validate(
            memory
        )


        if not validation.success:

            return validation


        return self.writer.write(
            memory
        )



    def retrieve(
        self,
        memory_id: str
    ) -> RetrievalResult:
        """
        Retrieve and rank memory.
        """


        result = self.retriever.retrieve(
            memory_id
        )


        if not result.success:

            return result


        return self.ranker.rank(
            result
        )