from dataclasses import dataclass

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)


@dataclass
class ConsolidationResult:
    """
    Represents the result
    of a memory consolidation.
    """

    memory_id: str

    score: float = 0.0

    consolidated: bool = False



class MemoryConsolidator:
    """
    Responsible for consolidating
    memory information.
    """


    def __init__(
        self,
        relevance_analyzer
    ):

        self.relevance_analyzer = (
            relevance_analyzer
        )



    def consolidate(
        self,
        memory: MemoryEntry
    ) -> ConsolidationResult:
        """
        Consolidate memory using
        relevance evaluation.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):

            return ConsolidationResult(
                memory_id="",
                score=0.0,
                consolidated=False
            )


        relevance = (
            self.relevance_analyzer.analyze(
                memory
            )
        )


        return ConsolidationResult(
            memory_id=memory.memory_id,
            score=relevance.score,
            consolidated=True
        )