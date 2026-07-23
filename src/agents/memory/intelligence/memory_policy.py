from src.agents.memory.domain.memory_type import (
    MemoryType
)


class MemoryPolicy:
    """
    Defines rules for memory management.

    Responsible for determining:
    - retention priority
    - memory importance
    - lifecycle decisions
    """


    def get_priority(
        self,
        memory_type: MemoryType
    ) -> float:
        """
        Returns priority score based
        on memory type.
        """


        priorities = {

            MemoryType.LONG_TERM: 1.0,

            MemoryType.SHORT_TERM: 0.5,

        }


        return priorities.get(
            memory_type,
            0.0
        )



    def should_retain(
        self,
        priority: float
    ) -> bool:
        """
        Determines if memory
        should be retained.
        """


        return priority >= 0.5