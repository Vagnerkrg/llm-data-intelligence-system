from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)


class RelevanceAnalyzer:
    """
    Responsible for evaluating
    memory relevance.
    """


    def analyze(
        self,
        memory: MemoryEntry
    ) -> RelevanceResult:
        """
        Calculate memory relevance.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):
            return RelevanceResult(
                memory_id="",
                score=0.0,
                explanation=(
                    "Invalid memory."
                )
            )


        score = 1.0


        factors = {
            "content_quality": score
        }


        return RelevanceResult(
            memory_id=memory.memory_id,
            score=score,
            factors=factors,
            explanation=(
                "Memory relevance calculated."
            )
        )