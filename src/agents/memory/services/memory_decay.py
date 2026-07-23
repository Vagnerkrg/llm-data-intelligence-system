from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.domain.memory_status import (
    MemoryStatus
)


class MemoryDecay:
    """
    Responsible for applying memory decay rules.
    """

    def __init__(
        self,
        decay_rate: float = 0.1
    ):

        self.decay_rate = decay_rate



    def apply(
        self,
        memory: MemoryEntry
    ):

        """
        Apply decay calculation
        to memory relevance.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):

            return {
                "memory_id": "",
                "score": 0.0,
                "decayed": False
            }



        current_score = memory.metadata.get(
            "relevance_score",
            1.0
        )


        new_score = max(
            0.0,
            current_score - self.decay_rate
        )


        memory.metadata[
            "relevance_score"
        ] = new_score



        if new_score == 0.0:

            memory.status = (
                MemoryStatus.ARCHIVED
            )



        return {
            "memory_id": memory.memory_id,
            "score": new_score,
            "decayed": True
        }