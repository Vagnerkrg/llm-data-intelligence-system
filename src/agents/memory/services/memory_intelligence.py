from src.agents.memory.services.relevance_analyzer import (
    RelevanceAnalyzer
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)


class MemoryIntelligence:
    """
    Coordinates cognitive memory analysis.
    """


    def __init__(
        self,
        relevance_analyzer: RelevanceAnalyzer
    ):

        self.relevance_analyzer = (
            relevance_analyzer
        )



    def analyze(
        self,
        memory: MemoryEntry
    ) -> RelevanceResult:
        """
        Analyze memory intelligence signals.
        """


        return self.relevance_analyzer.analyze(
            memory
        )