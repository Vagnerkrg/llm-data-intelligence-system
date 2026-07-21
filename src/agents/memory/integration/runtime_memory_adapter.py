from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.storage.storage_adapter import (
    StorageAdapter
)



class RuntimeMemoryAdapter:
    """
    Adapter responsible for connecting
    Agent Runtime with Memory Layer.
    """


    def __init__(
        self,
        storage: StorageAdapter
    ):

        self.storage = storage



    def remember(
        self,
        memory: MemoryEntry
    ):

        return self.storage.save(
            memory
        )



    def recall(
        self,
        memory_id: str
    ):

        return self.storage.get(
            memory_id
        )