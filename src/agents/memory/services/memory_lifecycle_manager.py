from src.agents.memory.services.memory_consolidator import (
    MemoryConsolidator
)

from src.agents.memory.services.memory_decay import (
    MemoryDecay
)

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)



class MemoryLifecycleResult:
    """
    Represents the result
    of a memory lifecycle operation.
    """


    def __init__(
        self,
        memory_id: str = "",
        consolidated: bool = False,
        decayed: bool = False
    ):

        self.memory_id = memory_id

        self.consolidated = consolidated

        self.decayed = decayed



class MemoryLifecycleManager:
    """
    Coordinates memory lifecycle operations.
    """


    def __init__(
        self,
        consolidator: MemoryConsolidator,
        decay: MemoryDecay
    ):

        self.consolidator = consolidator

        self.decay = decay



    def process(
        self,
        memory: MemoryEntry
    ) -> MemoryLifecycleResult:
        """
        Execute complete memory lifecycle.
        """


        if not isinstance(
            memory,
            MemoryEntry
        ):

            return MemoryLifecycleResult()



        consolidation = self.consolidator.consolidate(
            memory
        )


        decay_result = self.decay.apply(
            memory
        )


        if isinstance(
            decay_result,
            dict
        ):

            decayed = decay_result.get(
                "decayed",
                True
            )

        else:

            decayed = getattr(
                decay_result,
                "decayed",
                False
            )



        return MemoryLifecycleResult(
            memory_id=memory.memory_id,
            consolidated=consolidation.consolidated,
            decayed=decayed
        )