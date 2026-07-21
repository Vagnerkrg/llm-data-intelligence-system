from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.storage.storage_adapter import (
    StorageAdapter
)



class CognitiveMemoryAdapter:
    """
    Adapter responsible for connecting
    cognitive systems with memory.
    """


    def __init__(
        self,
        storage: StorageAdapter
    ):

        self.storage = storage



    def store_learning(
        self,
        memory: MemoryEntry
    ):

        return self.storage.save(
            memory
        )



    def retrieve_learning(
        self,
        memory_id: str
    ):

        return self.storage.get(
            memory_id
        )