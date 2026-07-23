from abc import ABC, abstractmethod

from src.agents.memory.domain.memory_entry import (
    MemoryEntry
)


class MemoryStore(ABC):
    """
    Contract for memory persistence.
    """


    @abstractmethod
    def save(
        self,
        memory: MemoryEntry
    ):
        pass



    @abstractmethod
    def get(
        self,
        memory_id: str
    ):
        pass



    @abstractmethod
    def delete(
        self,
        memory_id: str
    ):
        pass



    @abstractmethod
    def list_all(
        self
    ):
        pass