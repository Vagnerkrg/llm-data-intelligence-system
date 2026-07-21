from typing import List

from src.agents.memory.domain.retrieval_result import (
    RetrievalResult
)


class MemoryRanker:
    """
    Responsible for ranking retrieved memories
    based on relevance score.
    """

    def rank(
        self,
        result: RetrievalResult
    ) -> RetrievalResult:
        """
        Sort memories by score descending.
        """

        if not isinstance(
            result,
            RetrievalResult
        ):
            return RetrievalResult(
                success=False,
                message="Invalid retrieval result."
            )

        result.memories = sorted(
            result.memories,
            key=lambda memory: getattr(
                memory,
                "score",
                0.0
            ),
            reverse=True
        )

        if result.memories:
            result.score = getattr(
                result.memories[0],
                "score",
                0.0
            )

        result.success = True

        result.message = (
            "Memories ranked successfully."
        )

        return result