from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)


class MemoryRelevance:

    """
    Responsible for evaluating
    cognitive relevance of memories.
    """


    def evaluate(
        self,
        memory: MemoryEntry
    ) -> RelevanceResult:
        """
        Evaluate memory relevance.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):
            return RelevanceResult(
                memory_id="",
                score=0.0,
                explanation=(
                    "Invalid memory object."
                )
            )


        score = 0.0


        if memory.content:
            score += 0.5


        if len(memory.content) > 20:
            score += 0.5


        return RelevanceResult(
            memory_id=memory.memory_id,
            score=score,
            factors={
                "content_presence": 0.5,
                "content_length": 0.5
            },
            explanation=(
                "Memory relevance evaluated."
            )
        )