from typing import Dict, List

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)

from src.agents.memory.storage.memory_store import (
    MemoryStore
)


class InMemoryStore(MemoryStore):
    """
    In-memory implementation of memory storage.
    """


    def __init__(self):

        self._memory: Dict[str, MemoryEntry] = {}



    def save(
        self,
        memory: MemoryEntry
    ):

        self._memory[
            memory.memory_id
        ] = memory



    def get(
        self,
        memory_id: str
    ):

        return self._memory.get(
            memory_id
        )



    def delete(
        self,
        memory_id: str
    ):

        if memory_id in self._memory:

            del self._memory[memory_id]

            return True


        return False



    def list_all(
        self
    ) -> List[MemoryEntry]:

        return list(
            self._memory.values()
        )