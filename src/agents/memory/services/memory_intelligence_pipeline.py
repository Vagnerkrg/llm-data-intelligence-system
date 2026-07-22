from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)

from src.agents.memory.services.memory_intelligence_manager import (
    MemoryIntelligenceManager
)



class MemoryIntelligencePipeline:
    """
    Cognitive pipeline responsible for
    processing memory intelligence flow.

    Flow:

    Memory
        ↓
    Relevance Evaluation
        ↓
    Lifecycle Processing
        ↓
    Cognitive Decision
    """


    def __init__(
        self,
        intelligence_manager: MemoryIntelligenceManager = None
    ):


        self.intelligence_manager = (
            intelligence_manager
            if intelligence_manager
            else MemoryIntelligenceManager()
        )



    def process(
        self,
        memory: MemoryEntry
    ):


        if not isinstance(
            memory,
            MemoryEntry
        ):


            return RelevanceResult(
                memory_id="",
                score=0.0,
                explanation="Invalid memory."
            )



        result = (
            self.intelligence_manager.analyze(
                memory
            )
        )


        return result