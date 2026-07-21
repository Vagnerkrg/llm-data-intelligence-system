from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)



class MemoryMapper:
    """
    Maps memory objects into
    transport representations.
    """


    @staticmethod
    def to_dict(
        memory: MemoryEntry
    ):

        return {
            "memory_id": memory.memory_id,
            "content": memory.content,
            "memory_type": memory.memory_type.value,
            "status": memory.status.value,
            "source": memory.source,
            "metadata": memory.metadata
        }