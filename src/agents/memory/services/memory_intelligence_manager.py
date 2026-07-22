from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)

from src.agents.memory.services.memory_lifecycle_manager import (
    MemoryLifecycleManager
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

from src.agents.memory.intelligence.memory_relevance_scorer import (
    MemoryRelevanceScorer
)


class MemoryIntelligenceManager:
    """
    Coordinates memory intelligence operations.

    Responsible for:

    - cognitive relevance evaluation
    - lifecycle execution
    - memory intelligence processing
    """


    def __init__(
        self,
        relevance_scorer: MemoryRelevanceScorer = None,
        lifecycle_manager: MemoryLifecycleManager = None
    ):


        self.relevance_scorer = (
            relevance_scorer
            if relevance_scorer
            else MemoryRelevanceScorer()
        )


        self.lifecycle_manager = (
            lifecycle_manager
            if lifecycle_manager
            else self._create_lifecycle_manager()
        )



    def _create_lifecycle_manager(
        self
    ) -> MemoryLifecycleManager:
        """
        Creates default lifecycle pipeline.
        """


        relevance_analyzer = (
            RelevanceAnalyzer()
        )


        consolidator = (
            MemoryConsolidator(
                relevance_analyzer
            )
        )


        decay = (
            MemoryDecay()
        )


        return MemoryLifecycleManager(
            consolidator=consolidator,
            decay=decay
        )



    def analyze(
        self,
        memory: MemoryEntry
    ) -> RelevanceResult:
        """
        Execute memory intelligence analysis.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):

            result = RelevanceResult(
                memory_id="",
                score=0.0,
                explanation="Invalid memory."
            )

            result.relevance_score = 0.0

            return result



        relevance = (
            self.relevance_scorer.evaluate(
                memory
            )
        )


        lifecycle = (
            self.lifecycle_manager.process(
                memory
            )
        )


        relevance.lifecycle = lifecycle


        relevance.relevance_score = (
            relevance.score
        )


        return relevance