from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)

from src.agents.memory.intelligence.memory_relevance_scorer import (
    MemoryRelevanceScorer
)

from src.agents.memory.services.memory_lifecycle_manager import (
    MemoryLifecycleManager
)


class MemoryIntelligencePipeline:
    """
    Executes the complete memory intelligence flow.

    Pipeline:

    Memory
      ↓
    Relevance Evaluation
      ↓
    Lifecycle Processing
      ↓
    Intelligence Result
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
            else None
        )


    def process(
        self,
        memory: MemoryEntry
    ):
        """
        Process memory intelligence.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):

            return RelevanceResult(
                memory_id="",
                score=0.0,
                explanation="Invalid memory."
            )


        relevance = (
            self.relevance_scorer.evaluate(
                memory
            )
        )


        lifecycle = None


        if self.lifecycle_manager:

            lifecycle = (
                self.lifecycle_manager.process(
                    memory
                )
            )


        return {

            "memory_id": memory.memory_id,

            "relevance_score": (
                relevance.score
            ),

            "relevance": relevance,

            "lifecycle": lifecycle,

            "status": "analyzed"
        }