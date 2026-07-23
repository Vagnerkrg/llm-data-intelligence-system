from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.relevance_result import (
    RelevanceResult
)

from src.agents.memory.intelligence.relevance_scoring import (
    RelevanceScoring
)


class MemoryRelevanceScorer:
    """
    Cognitive memory relevance evaluator.

    Responsible for evaluating:
    - memory importance
    - contextual value
    - cognitive priority
    - experience relevance
    """

    def __init__(
        self,
        scorer: RelevanceScoring = None
    ):
        self.scorer = (
            scorer
            if scorer
            else RelevanceScoring()
        )


    def evaluate(
        self,
        memory: MemoryEntry
    ) -> RelevanceResult:
        """
        Evaluate cognitive relevance
        of a memory.
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


        result = self.scorer.calculate(
            memory
        )


        factors = result.factors.copy()


        factors["cognitive_value"] = (
            result.score
        )


        return RelevanceResult(
            memory_id=memory.memory_id,
            score=result.score,
            factors=factors,
            explanation=(
                "Cognitive memory relevance evaluated."
            )
        )