from src.agents.self_improvement.adaptation.domain.adaptation_result import (
    AdaptationResult,
)


class AdaptationHistory:
    """
    Stores adaptation execution history.

    Future versions may replace this in-memory
    storage with persistent memory.
    """

    def __init__(self):
        self.entries: list[AdaptationResult] = []

    def record(
        self,
        result: AdaptationResult,
    ) -> None:

        self.entries.append(result)

    def get_all(
        self,
    ) -> list[AdaptationResult]:

        return self.entries