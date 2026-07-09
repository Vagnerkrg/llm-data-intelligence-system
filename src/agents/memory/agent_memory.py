from typing import Dict, List, Optional, Any

from src.agents.memory.memory_entry import MemoryEntry



class AgentMemory:
    """
    Memory storage layer for agents.

    Responsible for storing,
    retrieving and searching
    previous agent information.
    """



    def __init__(
        self
    ):

        self._memory: Dict[str, MemoryEntry] = {}



    def store(
        self,
        key: str,
        value: Any,
        memory_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryEntry:
        """
        Store a new memory entry.
        """


        entry = MemoryEntry(

            key=key,

            value=value,

            memory_type=memory_type,

            metadata=metadata or {}

        )


        self._memory[key] = entry


        return entry



    def get(
        self,
        key: str
    ) -> Optional[MemoryEntry]:
        """
        Retrieve memory by key.
        """

        return self._memory.get(
            key
        )



    def exists(
        self,
        key: str
    ) -> bool:
        """
        Check if memory exists.
        """

        return key in self._memory



    def remove(
        self,
        key: str
    ):
        """
        Remove memory entry.
        """

        self._memory.pop(
            key,
            None
        )



    def clear(
        self
    ):
        """
        Remove all memories.
        """

        self._memory.clear()



    def list_memories(
        self
    ) -> List[MemoryEntry]:
        """
        Return all memories.
        """

        return list(
            self._memory.values()
        )



    def search(
        self,
        term: str
    ) -> List[MemoryEntry]:
        """
        Search memories by content.
        """

        term = term.lower()


        return [

            memory

            for memory in self._memory.values()

            if term in str(
                memory.value
            ).lower()

        ]