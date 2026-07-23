from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.storage.memory_store import (
    MemoryStore
)



class StorageAdapter:
    """
    Adapter between memory services
    and storage implementations.
    """


    def __init__(
        self,
        store: MemoryStore
    ):

        self.store = store



    def save(
        self,
        memory: MemoryEntry
    ):

        return self.store.save(
            memory
        )



    def get(
        self,
        memory_id: str
    ):

        return self.store.get(
            memory_id
        )



    def delete(
        self,
        memory_id: str
    ):

        return self.store.delete(
            memory_id
        )



    def list_all(
        self
    ):

        return self.store.list_all()