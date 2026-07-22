from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)

from src.agents.memory.intelligence.memory_policy import (
    MemoryPolicy
)



class RelevanceScoring:
    """
    Calculates cognitive relevance
    score for memories.
    """


    def __init__(
        self,
        policy: MemoryPolicy = None
    ):

        self.policy = (
            policy
            if policy
            else MemoryPolicy()
        )



    def calculate(
        self,
        memory: MemoryEntry
    ) -> RelevanceResult:
        """
        Calculate relevance score
        based on memory characteristics.
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



        factors = {}


        type_score = self.policy.get_priority(
            memory.memory_type
        )


        factors["memory_type"] = (
            type_score
        )


        content_score = 0.0


        if memory.content:

            content_score = min(
                len(memory.content) / 100,
                1.0
            )


        factors["content"] = (
            content_score
        )



        metadata_score = (
            1.0
            if memory.metadata
            else 0.0
        )


        factors["metadata"] = (
            metadata_score
        )



        score = (
            type_score * 0.5
            +
            content_score * 0.3
            +
            metadata_score * 0.2
        )



        return RelevanceResult(
            memory_id=memory.memory_id,
            score=round(
                score,
                2
            ),
            factors=factors,
            explanation=(
                "Memory relevance calculated."
            )
        )