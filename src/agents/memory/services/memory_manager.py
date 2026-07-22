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

from src.agents.memory.services.memory_consolidator import (
    MemoryConsolidator
)

from src.agents.memory.services.memory_decay import (
    MemoryDecay
)

from src.agents.memory.services.relevance_analyzer import (
    RelevanceAnalyzer
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

from src.agents.memory.domain.consolidation_result import (
    ConsolidationResult
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


        self.consolidator = MemoryConsolidator(
            RelevanceAnalyzer()
        )


        self.decay_engine = MemoryDecay()



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



    def consolidate(
        self,
        memory: MemoryEntry
    ) -> ConsolidationResult:
        """
        Consolidate memory information.
        """


        return self.consolidator.consolidate(
            memory
        )



    def decay(
        self,
        memory: MemoryEntry
    ):
        """
        Apply memory decay.
        """


        return self.decay_engine.apply(
            memory
        )